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


@cli.command(
    name='run',
    help='Runs a workflow.',
)
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
def run(
    workflow: typing.TextIO,
    begin: typing.Optional[arrow.Arrow],
    end: typing.Optional[arrow.Arrow],
    concurrency: int,
):
    """
     Runs a workflow.

    :param workflow: The workflow configuration file.
    :param begin: Begin time (included).
    :param end: End time (excluded).
    :param concurrency: The number of concurrent processes to use.

    :return: None
    """

    conf = load_config(workflow)
    run_workflow(
        conf,
        begin=begin,
        end=end,
        concurrency=concurrency,
    )
