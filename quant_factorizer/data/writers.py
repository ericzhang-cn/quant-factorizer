import os
import typing

import pandas as pd
from loguru import logger

from quant_factorizer.data.base import IndicatorWriter, WriteDataError


class LocalFileWriter(IndicatorWriter):
    def __init__(
        self,
        *,
        dir_path: str,
        file_type: str = 'csv',
        prefix: str = '',
        suffix: str = '',
    ):
        self.dir_path = dir_path
        self.file_type = file_type
        self.prefix = prefix
        self.suffix = suffix

        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        if not os.path.isdir(self.dir_path):
            raise WriteDataError(f'{self.dir_path} is not a directory.')

    def write(
        self,
        *,
        calculation_df: typing.Optional[pd.DataFrame] = None,
        evaluation_df: typing.Optional[pd.DataFrame] = None,
    ) -> None:
        if calculation_df is None:
            calculation_df = pd.DataFrame()
        if evaluation_df is None:
            evaluation_df = pd.DataFrame()

        calculation_df.reset_index(inplace=True)
        evaluation_df.reset_index(inplace=True)

        if self.file_type.lower() == 'csv':
            calculation_df.to_csv(
                os.path.join(
                    self.dir_path,
                    f'{self.prefix}calculations{self.suffix}.csv',
                ),
                header=True,
                index=False,
            )
            evaluation_df.to_csv(
                os.path.join(
                    self.dir_path, f'{self.prefix}evaluations{self.suffix}.csv'
                ),
                header=True,
                index=False,
            )
        elif self.file_type.lower() == 'pickle':
            calculation_df.to_pickle(
                os.path.join(
                    self.dir_path,
                    f'{self.prefix}calculations{self.suffix}.pkl',
                )
            )
            evaluation_df.to_pickle(
                os.path.join(
                    self.dir_path, f'{self.prefix}evaluations{self.suffix}.pkl'
                )
            )
        else:
            raise WriteDataError(f'Unsupported file type {self.file_type}.')


class CSVWriter(LocalFileWriter):
    def __init__(
        self,
        *,
        dir_path: str,
        prefix: str = '',
        suffix: str = '',
    ):
        super().__init__(
            dir_path=dir_path, file_type='csv', prefix=prefix, suffix=suffix
        )


class PickleWriter(LocalFileWriter):
    def __init__(
        self,
        *,
        dir_path: str,
        prefix: str = '',
        suffix: str = '',
    ):
        super().__init__(
            dir_path=dir_path, file_type='pickle', prefix=prefix, suffix=suffix
        )
