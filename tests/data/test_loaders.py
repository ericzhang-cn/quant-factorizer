import os.path

from quant_factorizer.data.loaders import CSVLoader


def test_load_csv():
    loader = CSVLoader(
        file_path=os.path.join('fixture', 'ohlcv_example.csv'),
        time_field='candle_begin_time',
    )
    df = loader.load()
    assert set(df.columns) == {
        'symbol',
        'time',
        'open',
        'high',
        'low',
        'close',
        'volume',
    }
