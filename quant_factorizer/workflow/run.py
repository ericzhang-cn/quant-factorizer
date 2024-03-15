import concurrent
import typing

import pandas as pd
from arrow import Arrow
from loguru import logger
from rich.console import Console
from rich.table import Table

from quant_factorizer.data.base import OHLCVDataLoader, IndicatorWriter
from quant_factorizer.evaluation.evaluators import evaluator_registry
from quant_factorizer.factor.crosses import cross_registry
from quant_factorizer.factor.indicators import technical_indicator_registry
from quant_factorizer.workflow.config import WorkflowConf


def _calculate(
    df: pd.DataFrame, *, symbol: str, conf: WorkflowConf, concurrency: int = 1
) -> pd.DataFrame:
    dfs = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=concurrency
    ) as executor:
        futures = [
            executor.submit(
                technical_indicator_registry[ti.name].func,
                df.loc[symbol],
                **ti.args,
            )
            for ti in conf.factor.indicators
        ]

        for future in futures:
            dfs.append(future.result())

    return pd.concat(dfs, axis=1)


def _cross(
    df: pd.DataFrame, *, conf: WorkflowConf, concurrency: int = 1
) -> pd.DataFrame:
    dfs = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=concurrency
    ) as executor:
        futures = [
            executor.submit(
                cross_registry[cr.name].func,
                df,
                order=o,
                **cr.args,
            )
            for cr in conf.factor.crosses
            for o in cr.orders
        ]

        for future in futures:
            dfs.append(future.result())

    return pd.concat(dfs, axis=1)


def _evaluate(
    df: pd.DataFrame, *, symbol: str, conf: WorkflowConf, concurrency: int = 1
) -> pd.DataFrame:
    dfs = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=concurrency
    ) as executor:
        futures = [
            executor.submit(
                evaluator_registry[e.name].func,
                df.loc[symbol].reset_index(drop=True),
                **e.args,
            )
            for e in conf.factor.evaluators
        ]

        for future in futures:
            dfs.append(future.result())

    return pd.concat(dfs, axis=1)


def run_workflow(
    conf: WorkflowConf,
    *,
    begin: typing.Optional[Arrow] = None,
    end: typing.Optional[Arrow] = None,
    concurrency: int = 1,
    verbose: bool = True,
) -> None:
    """
    Runs a workflow based on the provided configuration.

    :param conf: The WorkflowConf object representing the workflow configuration.
    :param begin: (Optional) The beginning timestamp for the workflow. Defaults to None.
    :param end: (Optional) The ending timestamp for the workflow. Defaults to None.
    :param concurrency: (Optional) The number of concurrent processes to use. Defaults to 1.
    :param verbose: (Optional) Whether to print progress messages. Defaults to True.
    """
    console = Console()

    if concurrency <= 0:
        concurrency = 1

    # Load data.
    if verbose:
        console.print('[bold green]Loading data...')

    loader = OHLCVDataLoader.get_instance(
        conf.data.loader.name, **conf.data.loader.args
    )
    df = loader.load()
    df.set_index(['symbol', 'time'], inplace=True)

    if verbose:
        console.print(f'[bold green]OHLCV data loaded.')

        table = Table(show_header=True)
        table.add_column('Symbol')
        table.add_column('Begin')
        table.add_column('End')
        table.add_column('Count')

        for symbol in df.index.get_level_values('symbol').unique():
            table.add_row(
                symbol,
                str(df.loc[symbol].index.min()),
                str(df.loc[symbol].index.max()),
                str(len(df.loc[symbol])),
            )
        console.print(table)

    # Filter by time.
    if verbose:
        console.print(
            f'[bold green]Filtering data from {begin or "-inf"} to {end or "inf"}...'
        )

    if begin:
        df = df[
            df.index.get_level_values('time')
            >= pd.Timestamp(begin.format('YYYY-MM-DD HH:mm:ss'))
        ]
    if end:
        df = df[
            df.index.get_level_values('time')
            < pd.Timestamp(end.format('YYYY-MM-DD HH:mm:ss'))
        ]

    if verbose:
        console.print(f'[bold green]OHLCV data filtered.')

        table = Table(show_header=True)
        table.add_column('Symbol')
        table.add_column('Begin')
        table.add_column('End')
        table.add_column('Count')

        for symbol in df.index.get_level_values('symbol').unique():
            table.add_row(
                symbol,
                str(df.loc[symbol].index.min()),
                str(df.loc[symbol].index.max()),
                str(len(df.loc[symbol])),
            )
        console.print(table)

    # Calculate technical indicators.
    if verbose:
        console.print(f'[bold green]Calculating indicators...')

    r_dfs = []
    for symbol in df.index.get_level_values('symbol').unique():
        r_df = _calculate(
            df, symbol=symbol, conf=conf, concurrency=concurrency
        )
        if conf.factor.crosses:
            c_df = _cross(r_df, conf=conf, concurrency=concurrency)
            r_df = pd.concat([r_df, c_df], axis=1)
        r_df['symbol'] = symbol
        r_df.reset_index(inplace=True)
        r_df.set_index(['symbol', 'time'], inplace=True)
        r_dfs.append(r_df)
    calculation_df = pd.concat(r_dfs, axis=0)

    if verbose:
        console.print(f'[bold green]Indicators calculated.')

    # Evaluate indicators.
    if verbose:
        console.print(f'[bold green]Evaluating indicators...')

    if conf.factor.evaluators:
        e_dfs = []
        for symbol in calculation_df.index.get_level_values('symbol').unique():
            e_df = _evaluate(
                calculation_df,
                symbol=symbol,
                conf=conf,
                concurrency=concurrency,
            )
            e_df['symbol'] = symbol
            e_dfs.append(e_df)
        evaluation_df = pd.concat(e_dfs, axis=0)
    else:
        evaluation_df = pd.DataFrame()

    if verbose:
        console.print(f'[bold green]Indicators evaluated.')

    # Write data.
    if verbose:
        console.print(f'[bold green]Writing data...')

    writer = IndicatorWriter.get_instance(
        conf.data.writer.name, **conf.data.writer.args
    )
    writer.write(calculation_df=calculation_df, evaluation_df=evaluation_df)

    if verbose:
        console.print(f'[bold green]Data written.')
