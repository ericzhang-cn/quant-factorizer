import pandas as pd
import pytest

from quant_factorizer.factor.indicators import rsi, return_pct, return_


@pytest.fixture(scope='function')
def ohlcv():
    numbers = list(range(100))
    return pd.DataFrame(
        {
            'open': numbers,
            'close': numbers,
            'high': numbers,
            'low': numbers,
            'volume': numbers,
        }
    )


def test_rsi(ohlcv):
    indicators = rsi(ohlcv)
    assert indicators.loc[14, 'rsi_5'] == 100.0


def test_return(ohlcv):
    indicators = return_(
        ohlcv,
        periods=[
            1,
        ],
    )
    assert indicators.loc[1, 'return_1'] == 1.0


def test_return_pct(ohlcv):
    indicators = return_pct(
        ohlcv,
        periods=[
            1,
        ],
    )
    assert indicators.loc[2, 'return_pct_1'] == 1.0
