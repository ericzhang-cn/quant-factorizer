from __future__ import annotations

import abc
import typing

import pandas as pd


class LoadDataError(Exception):
    """Raised when there is an error while loading data."""

    pass


class LoaderNotFoundError(Exception):
    """raised when a loader is not found"""

    pass


class OHLCVDataLoader(abc.ABC):
    """
    Abstract base class for loading OHLCV (Open, High, Low, Close, Volume) data.
    """

    @abc.abstractmethod
    def load(self) -> pd.DataFrame:
        """
        Abstract method to load the OHLCV data.

        :return: The loaded OHLCV data.
        :rtype: pd.DataFrame
        """
        raise NotImplementedError

    @classmethod
    def get_instance(cls, name: str, **kwargs) -> OHLCVDataLoader:
        """
        Returns an instance of :class:`OHLCVDataLoader` based on the provided name.

        :param name: The name of the loader.
        :type name: str
        :param **kwargs: Additional keyword arguments to be passed to the loader.
        :return: An instance of :class:`OHLCVDataLoader`.
        :rtype: OHLCVDataLoader
        :raises LoaderNotFoundError: If the specified loader name is not found.
        """
        if name.lower() == 'pickle':
            from quant_factorizer.data.loaders import PickleLoader

            return PickleLoader(**kwargs)
        if name.lower() == 'csv':
            from quant_factorizer.data.loaders import CSVLoader

            return CSVLoader(**kwargs)
        else:
            raise LoaderNotFoundError(f'Loader {name} not found.')


class WriteDataError(Exception):
    """Raised when there is an error while writing data."""

    pass


class WriterNotFoundError(Exception):
    """raised when a writer is not found"""

    pass


class IndicatorWriter(abc.ABC):
    """
    Abstract base class for writing technical indicator data.
    """

    @abc.abstractmethod
    def write(
        self,
        *,
        calculation_df: typing.Optional[pd.DataFrame] = None,
        evaluation_df: typing.Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Abstract method to write the technical indicator data.

        :param calculation_df: The dataframe containing the calculated technical indicators.
        :type calculation_df: pd.DataFrame
        :param evaluation_df: The dataframe containing the evaluated technical indicators.
        :type evaluation_df: pd.DataFrame
        """
        raise NotImplementedError

    @classmethod
    def get_instance(cls, name: str, **kwargs) -> IndicatorWriter:
        """
        Returns an instance of :class:`IndicatorWriter` based on the provided name.

        :param name: The name of the writer.
        :type name: str
        :param **kwargs: Additional keyword arguments to be passed to the writer.
        :return: An instance of :class:`IndicatorWriter`.
        :rtype: IndicatorWriter
        :raises WriterNotFoundError: If the specified writer name is not found.
        """
        if name.lower() == 'pickle':
            from quant_factorizer.data.writers import PickleWriter

            return PickleWriter(**kwargs)
        if name.lower() == 'csv':
            from quant_factorizer.data.writers import CSVWriter

            return CSVWriter(**kwargs)

        else:
            raise WriterNotFoundError(f'Writer {name} not found.')
