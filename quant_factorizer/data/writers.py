import pandas as pd

from quant_factorizer.data.base import IndicatorWriter, WriteDataError


class LocalFileWriter(IndicatorWriter):
    def __init__(
        self,
        *,
        file_path: str,
        file_type: str = 'csv',
    ):
        self.file_path = file_path
        self.file_type = file_type

    def write(self, df: pd.DataFrame) -> None:
        df.reset_index(inplace=True)

        if self.file_type.lower() == 'csv':
            df.to_csv(self.file_path, header=True, index=False)
        elif self.file_type.lower() == 'pickle':
            df.to_pickle(self.file_path)
        else:
            raise WriteDataError(f'Unsupported file type {self.file_type}.')


class CSVWriter(LocalFileWriter):
    def __init__(
        self,
        *,
        file_path: str,
    ):
        super().__init__(file_path=file_path, file_type='csv')


class PickleWriter(LocalFileWriter):
    def __init__(
        self,
        *,
        file_path: str,
    ):
        super().__init__(file_path=file_path, file_type='pickle')
