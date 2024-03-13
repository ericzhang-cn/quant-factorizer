import functools
import typing

import pandas as pd
import talib as ta
from pydantic import BaseModel


class TechnicalIndicator(BaseModel):
    """
    Represents a technical indicator used in financial analysis.

    :ivar name: The name of the technical indicator.
    :vartype name: str
    :ivar definition: The definition or description of the technical indicator.
    :vartype definition: str
    :ivar func: The callable function used to calculate the technical indicator.
    :vartype func: typing.Callable[..., pd.DataFrame]
    """

    name: str
    definition: str
    func: typing.Callable[..., pd.DataFrame]


technical_indicator_registry: dict[str, TechnicalIndicator] = {}


def indicator(name: str, definition: str = ''):
    """
    Decorator that registers a function as a technical indicator.

    :param name: The name of the indicator.
    :type name: str
    :param definition: The definition of the indicator (optional).
    :type definition: str, default ''
    :return: The decorated function.
    :rtype: function
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get('periods', None) is None:
                kwargs['periods'] = [
                    2,
                    5,
                ]

            result = func(*args, **kwargs)

            result['time'] = args[0].index.copy()
            result.set_index('time', inplace=True)

            return result

        technical_indicator_registry[name] = TechnicalIndicator(
            name=name,
            definition=definition,
            func=wrapper,
        )

        return wrapper

    return decorator


@indicator(
    name='SMA',
    definition='The Simple Moving Average calculates the average price of an asset over a specified number of periods.',
)
def sma(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    """
    Calculate the Simple Moving Average (SMA) for the given periods.

    :param ohlcv: DataFrame containing Open, High, Low, Close, and Volume data.
    :type ohlcv: pd.DataFrame
    :param periods: List of periods for which to calculate the SMA.
    :type periods: list[int] | None
    :return: DataFrame containing the SMA values for each period.
    :rtype: pd.DataFrame
    """
    df = pd.DataFrame()
    for p in periods:
        df[f'sma_{p}'] = ta.SMA(ohlcv['close'], timeperiod=p)
    return df


@indicator(
    name='RSI',
    definition='RSI stands for Relative Strength Index.',
)
def rsi(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    """
    Calculate the Relative Strength Index (RSI) for the given periods.

    :param ohlcv: DataFrame containing Open, High, Low, Close, and Volume data.
    :type ohlcv: pd.DataFrame
    :param periods: List of periods for which to calculate the RSI.
    :type periods: list[int] | None
    :return: DataFrame containing the RSI values for each period.
    :rtype: pd.DataFrame
    """
    df = pd.DataFrame()
    for p in periods:
        df[f'rsi_{p}'] = ta.RSI(ohlcv['close'], timeperiod=p)
    return df


@indicator(
    name='Return',
    definition='The gain or loss generated on an investment over a specific period of time.',
)
def return_(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    """
    Calculates the return for a given DataFrame of OHLCV (Open, High, Low, Close, Volume) data.

    :param ohlcv: DataFrame containing OHLCV data.
    :type ohlcv: pd.DataFrame
    :param periods: List of periods to calculate returns for.
    :type periods: list[int] | None, optional
    :return: DataFrame containing return values for each period.
    :rtype: pd.DataFrame
    """
    df = pd.DataFrame()
    for p in periods:
        df[f'return_{p}'] = ohlcv['close'].diff(periods=p)
    return df


@indicator(
    name='Percentage_Of_Return',
    definition='The rate of return.',
)
def return_pct(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    """
    Calculate the percentage change in value over the specified periods.

    :param ohlcv: DataFrame containing Open, High, Low, Close, and Volume data.
    :type ohlcv: pd.DataFrame
    :param periods: List of periods for which to calculate the percentage change.
        If None, default periods [7, 14, 30] will be used.
    :type periods: list[int] | None
    :return: DataFrame containing the percentage change in value for each period.
    :rtype: pd.DataFrame
    """
    df = pd.DataFrame()
    for p in periods:
        df[f'return_pct_{p}'] = ohlcv['close'].pct_change(periods=p)
    return df


@indicator(
    name='OBV',
    definition='On-Balance Volume.',
)
def obv(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    df = pd.DataFrame()
    df['obv'] = ta.OBV(ohlcv['close'], ohlcv['volume'])
    return df


@indicator(
    name='AD',
    definition='Accumulation/Distribution Line.',
)
def ad_line(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    df = pd.DataFrame()
    df['ad_line'] = ta.AD(
        ohlcv['high'], ohlcv['low'], ohlcv['close'], ohlcv['volume']
    )
    return df


@indicator(
    name='ADX',
    definition='Average Directional Index.',
)
def adx(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        df[f'adx_{p}'] = ta.ADX(
            ohlcv['high'], ohlcv['low'], ohlcv['close'], timeperiod=p
        )
    return df


@indicator(
    name='Aroon',
    definition='Aroon Indicator.',
)
def aroon(
    ohlcv: pd.DataFrame, *, periods: typing.Optional[list[int]] = None
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        df[f'aroon_down_{p}'], df[f'aroon_up_{p}'] = ta.AROON(
            ohlcv['high'], ohlcv['low'], timeperiod=p
        )
    return df


@indicator(
    name='MACD',
    definition='Moving Average Convergence Divergence.',
)
def macd(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> pd.DataFrame:
    df = pd.DataFrame()
    df['macd'], _, _ = ta.MACD(
        ohlcv['close'],
        fastperiod=fast_period,
        slowperiod=slow_period,
        signalperiod=signal_period,
    )
    return df


@indicator(
    name='STOCH',
    definition='Stochastic Oscillator.',
)
def so(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
    fastk_period: int = 5,
    slowk_period: int = 3,
    slowk_matype: int = 0,
    slowd_period: int = 3,
    slowd_matype: int = 0,
) -> pd.DataFrame:
    df = pd.DataFrame()
    df['slowk'], df['slowd'] = ta.STOCH(
        ohlcv['high'],
        ohlcv['low'],
        ohlcv['close'],
        fastk_period=fastk_period,
        slowk_period=slowk_period,
        slowk_matype=slowk_matype,
        slowd_period=slowd_period,
        slowd_matype=slowd_matype,
    )
    return df


@indicator(
    name='ATR',
    definition='Average True Range.',
)
def atr(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        df[f'atr_{p}'] = ta.ATR(
            ohlcv['high'], ohlcv['low'], ohlcv['close'], timeperiod=p
        )
    return df


@indicator(
    name='BIAS',
    definition='The percentage deviation of the closing price from the moving average.',
)
def bias(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        sma_ = ta.SMA(ohlcv['close'], timeperiod=p)
        df[f'bias_{p}'] = (ohlcv['close'] - sma_) / sma_
    return df


@indicator(
    name='PRR',
    definition='Price Range Ratio.',
)
def prr(
    ohlcv: pd.DataFrame,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    df['prr'] = ohlcv['high'] / ohlcv['low']
    return df


@indicator(
    name='ROC',
    definition='Rate of Change.',
)
def roc(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        df[f'roc_{p}'] = ta.ROC(ohlcv['close'], timeperiod=p)
    return df


@indicator(
    name='AMP',
    definition='Amplitude.',
)
def amp(
    ohlcv: pd.DataFrame,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        max_ = ohlcv['close'].rolling(p).max()
        min_ = ohlcv['close'].rolling(p).min()
        df[f'amp_{p}'] = (max_ - min_) / min_
    return df


@indicator(
    name='VOL',
    definition='Volatility.',
)
def vol(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        sma_ = ta.SMA(ohlcv['close'], timeperiod=p)
        std = ta.STDDEV(ohlcv['close'], timeperiod=p)
        df[f'vol_{p}'] = sma_ / std
    return df


@indicator(
    name='HL',
    definition='High to Low.',
)
def hl(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    range_ = ohlcv['high'] / ohlcv['low']
    for p in periods:
        df[f'hl_{p}'] = ta.SMA(range_, timeperiod=p)
    return df


@indicator(
    name='DPO',
    definition='Detrended Price Oscillator.',
)
def dpo(
    ohlcv: pd.DataFrame,
    *,
    periods: typing.Optional[list[int]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()
    for p in periods:
        sma_ = ta.SMA(ohlcv['close'], timeperiod=p)
        shifted = ohlcv['close'].shift(int(p / 2 + 1))
        df[f'dpo_{p}'] = shifted - sma_
    return df
