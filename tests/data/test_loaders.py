import os.path

from pandas import Timestamp

from quant_factorizer.data.loaders import CSVLoader, PickleLoader


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
    assert df.loc[0, 'symbol'] == 'BTC-USDT'
    assert df.loc[0, 'time'] == Timestamp('2019-09-08 17:00:00')
    assert df.loc[0, 'open'] == 10000.0
    assert df.loc[0, 'close'] == 10000.0
    assert df.loc[0, 'high'] == 10000.0
    assert df.loc[0, 'low'] == 10000.0
    assert df.loc[0, 'volume'] == 0.002


def test_load_pickle():
    loader = PickleLoader(
        file_path=os.path.join('fixture', 'ohlcv_example.pkl'),
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
    assert df.loc[0, 'symbol'] == 'BTC-USDT'
    assert df.loc[0, 'time'] == Timestamp('2019-09-08 17:00:00')
    assert df.loc[0, 'open'] == 10000.0
    assert df.loc[0, 'close'] == 10000.0
    assert df.loc[0, 'high'] == 10000.0
    assert df.loc[0, 'low'] == 10000.0
    assert df.loc[0, 'volume'] == 0.002
