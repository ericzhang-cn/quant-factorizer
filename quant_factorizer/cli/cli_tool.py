import os.path
import typing
import warnings

import arrow
import click
from rich.console import Console

from quant_factorizer.cli.types import ArrowType
from quant_factorizer.workflow.config import load_config
from quant_factorizer.workflow.run import run_workflow

warnings.filterwarnings('ignore')


@click.group()
def cli():
    """Command-line interface of QuantFactorizer."""
    pass


@cli.command()
@click.option(
    '--workflow',
    required=True,
    type=click.types.File('r'),
    help='Workflow configuration file.',
)
@click.option(
    '--begin',
    required=False,
    type=ArrowType(),
    help='Begin time (included).',
)
@click.option(
    '--end',
    required=False,
    type=ArrowType(),
    help='End time (excluded).',
)
@click.option(
    '--concurrency',
    required=False,
    type=click.types.IntRange(min=1),
    default=1,
    help='The number of concurrent processes to use.',
)
@click.option(
    '--output-dir',
    required=True,
    type=click.types.Path(file_okay=False, dir_okay=True),
    help='The path of the output directory.',
)
def run(
        workflow: typing.TextIO,
        begin: typing.Optional[arrow.Arrow],
        end: typing.Optional[arrow.Arrow],
        concurrency: int,
        output_dir: str,
):
    """
     Runs a workflow.

    :param workflow: The workflow configuration file.
    :param begin: Begin time (included).
    :param end: End time (excluded).
    :param concurrency: The number of concurrent processes to use.
    :param output_dir: The path of the output directory.

    :return: None
    """

    conf = load_config(workflow)
    console = Console()
    for symbol, df in run_workflow(conf, begin=begin, end=end, concurrency=concurrency):
        console.print(symbol)
        df.to_csv(
            os.path.join(output_dir, f'{symbol}.csv'),
            header=True,
            index=True,
        )
