import concurrent
import typing

import pandas as pd
from arrow import Arrow

from quant_factorizer.data.base import OHLCVDataLoader
from quant_factorizer.factor.crosses import cross_registry
from quant_factorizer.factor.indicators import technical_indicator_registry
from quant_factorizer.workflow.config import WorkflowConf


def run_workflow(
    conf: WorkflowConf,
    *,
    begin: typing.Optional[Arrow] = None,
    end: typing.Optional[Arrow] = None,
    concurrency: int = 1,
) -> typing.Generator[tuple[str, pd.DataFrame], None, None]:
    """
    Runs a workflow based on the provided configuration.

    :param conf: The WorkflowConf object representing the workflow configuration.
    :param begin: (Optional) The beginning timestamp for the workflow. Defaults to None.
    :param end: (Optional) The ending timestamp for the workflow. Defaults to None.
    :param concurrency: (Optional) The number of concurrent processes to use. Defaults to 1.
    :return: A dictionary containing AssetResult objects, with asset names as keys.
    """
    if concurrency <= 0:
        concurrency = 1

    # Load data.
    loader = OHLCVDataLoader.get_instance(
        conf.data.loader.name, **conf.data.loader.args
    )
    df = loader.load()
    df.set_index(['symbol', 'time'], inplace=True)

    # Filter by time.
    if begin:
        df = df[df.index.get_level_values('time') >= begin]
    if end:
        df = df[df.index.get_level_values('time') <= end]

    # Calculate technical indicators.
    for symbol in df.index.get_level_values('symbol').unique():
        dfs = []

        with concurrent.futures.ProcessPoolExecutor(
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

        r_df = pd.concat(dfs, axis=1)

        if conf.factor.crosses:
            copy_ = r_df.copy(deep=False)
            dfs = []

            with concurrent.futures.ProcessPoolExecutor(
                max_workers=concurrency
            ) as executor:
                futures = [
                    executor.submit(
                        cross_registry[cr.name].func,
                        copy_,
                        order=o,
                        **cr.args,
                    )
                    for cr in conf.factor.crosses
                    for o in cr.orders
                ]

                for future in futures:
                    dfs.append(future.result())

            c_df = pd.concat(dfs, axis=1)
            r_df = pd.concat([r_df, c_df], axis=1)
        r_df['symbol'] = symbol
        r_df.reset_index(inplace=True)
        r_df.set_index(['symbol', 'time'], inplace=True)
        yield symbol, r_df
