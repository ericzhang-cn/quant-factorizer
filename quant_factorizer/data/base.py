from __future__ import annotations

import abc

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
