import typing

import tomli
from pydantic import BaseModel


class IndicatorConf(BaseModel):
    name: str
    args: dict[str, typing.Any] = {}


class CrossConf(BaseModel):
    name: str
    orders: list[int] = [2]
    args: dict[str, typing.Any] = {}


class FactorConf(BaseModel):
    indicators: list[IndicatorConf] = {}
    crosses: typing.Optional[list[CrossConf]] = None


class LoaderConf(BaseModel):
    name: str
    args: dict[str, typing.Any] = {}


class WriterConf(BaseModel):
    name: str
    args: dict[str, typing.Any] = {}


class DataConf(BaseModel):
    loader: LoaderConf
    writer: WriterConf


class WorkflowConf(BaseModel):
    name: str
    data: DataConf
    factor: FactorConf


def load_config(io: typing.TextIO) -> WorkflowConf:
    """
    Load the configuration file content from the given text IO object and return a WorkflowConf object.

    :param io: An open text IO object used to read the configuration file content.
    :type io: typing.TextIO

    :return: A WorkflowConf object created from the configuration file content.
    :rtype: WorkflowConf

    :raises TypeError: If a valid WorkflowConf object cannot be parsed from the configuration file content.
    """
    content = io.read()
    o = tomli.loads(content)
    return WorkflowConf(**o)
