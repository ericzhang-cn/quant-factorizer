import os.path
import typing

import pandas as pd

from quant_factorizer.data.base import LoadDataError, OHLCVDataLoader


class LocalFileLoader(OHLCVDataLoader):
    """
    A base class for loading OHLCV data from a local file.

    This class is an abstract base class that provides a common interface for loading OHLCV data from different file types.
    """

    def __init__(
        self,
        *,
        file_path: str,
        file_type: str = 'csv',
        symbol_field: str = 'symbol',
        time_field: str = 'time',
        open_field: str = 'open',
        close_field: str = 'close',
        low_field: str = 'low',
        high_field: str = 'high',
        volume_field: str = 'volume',
    ):
        self.file_path = file_path
        self.file_type = file_type
        self.symbol_field = symbol_field
        self.time_field = time_field
        self.open_field = open_field
        self.close_field = close_field
        self.low_field = low_field
        self.high_field = high_field
        self.volume_field = volume_field

    def load(self) -> pd.DataFrame:
        """
        Load the OHLCV data from the local file.

        :return: The loaded OHLCV data.
        :rtype: pd.DataFrame
        """
        if not os.path.exists(self.file_path):
            raise LoadDataError(f'Path {self.file_path} not exists.')
        if not os.path.isfile(self.file_path):
            raise LoadDataError(f'Path {self.file_path} is not a file.')

        if self.file_type.lower() == 'csv':
            origin_df = pd.read_csv(self.file_path)
        elif self.file_type.lower() == 'pickle':
            origin_df = pd.read_pickle(self.file_path)
            if not isinstance(origin_df, pd.DataFrame):
                raise LoadDataError('The unpickle file is not a DataFrame.')
        else:
            raise LoadDataError(f'Unsupported file type {self.file_type}.')

        cols = [
            self.symbol_field,
            self.time_field,
            self.open_field,
            self.high_field,
            self.low_field,
            self.close_field,
            self.volume_field,
        ]
        for col in cols:
            if col not in origin_df:
                raise LoadDataError(f'The required column {col} not exists.')

        df = pd.DataFrame()
        df['symbol'] = origin_df[self.symbol_field].copy(deep=False)
        df['time'] = origin_df[self.time_field].copy(deep=False)
        df['open'] = origin_df[self.open_field].copy(deep=False)
        df['high'] = origin_df[self.high_field].copy(deep=False)
        df['low'] = origin_df[self.low_field].copy(deep=False)
        df['close'] = origin_df[self.close_field].copy(deep=False)
        df['volume'] = origin_df[self.volume_field].copy(deep=False)
        df['time'] = pd.to_datetime(df['time'])

        return df


class CSVLoader(LocalFileLoader):
    """
    A class for loading OHLCV data from a CSV file.

    This class extends the LocalFileLoader class.
    """

    def __init__(
        self,
        *,
        file_path: str,
        symbol_field: str = 'symbol',
        time_field: str = 'time',
        open_field: str = 'open',
        close_field: str = 'close',
        low_field: str = 'low',
        high_field: str = 'high',
        volume_field: str = 'volume',
    ):
        super().__init__(
            file_path=file_path,
            file_type='csv',
            symbol_field=symbol_field,
            time_field=time_field,
            open_field=open_field,
            close_field=close_field,
            low_field=low_field,
            high_field=high_field,
            volume_field=volume_field,
        )


class PickleLoader(LocalFileLoader):
    """
    A class for loading OHLCV data from a pickle file.

    This class extends the LocalFileLoader class.
    """

    def __init__(
        self,
        *,
        file_path: str,
        symbol_field: str = 'symbol',
        time_field: str = 'time',
        open_field: str = 'open',
        close_field: str = 'close',
        low_field: str = 'low',
        high_field: str = 'high',
        volume_field: str = 'volume',
    ):
        super().__init__(
            file_path=file_path,
            file_type='pickle',
            symbol_field=symbol_field,
            time_field=time_field,
            open_field=open_field,
            close_field=close_field,
            low_field=low_field,
            high_field=high_field,
            volume_field=volume_field,
        )
