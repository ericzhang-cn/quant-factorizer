import functools
import typing

import pandas as pd
from pydantic import BaseModel
from sklearn.preprocessing import MinMaxScaler


class Evaluator(BaseModel):
    """
    Evaluator class for performing evaluations.

    :param name: The name of the evaluator.
    :type name: str
    :param definition: The definition of the evaluator.
    :type definition: str
    :param func: A callable function that takes any number of arguments and returns a pandas DataFrame.
    :type func: typing.Callable[..., pd.DataFrame]
    """

    name: str
    definition: str
    func: typing.Callable[..., pd.DataFrame]


evaluator_registry: dict[str, Evaluator] = {}


def evaluator(name: str, definition: str = ''):
    """
    Decorator function that registers a function as an evaluator.

    :param name: The name of the evaluator.
    :type name: str
    :param definition: (Optional) The definition of the evaluator.
    :type definition: str, optional
    :return: A decorator function.
    :rtype: typing.Callable
    """

    def decorator(func):
        evaluator_registry[name] = Evaluator(
            name=name,
            definition=definition,
            func=func,
        )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result

        return wrapper

    return decorator


@evaluator(name='Describe', definition='Basic statistics.')
def describe(df: pd.DataFrame, normalize: bool = True) -> pd.DataFrame:
    """
    Evaluator for computing basic statistics.

    :param df: The DataFrame containing the indicators.
    :type df: pd.DataFrame
    :param normalize: Whether to normalize the statistics.
    :type normalize: bool
    :return: The computed basic statistics as a transposed DataFrame.
    :rtype: pd.DataFrame
    """
    if not normalize:
        return df.describe().T
    else:
        scaler = MinMaxScaler(feature_range=(0, 1))
        normalized = scaler.fit_transform(df)
        normalized = pd.DataFrame(normalized, columns=df.columns)
        return normalized.describe().T


@evaluator(
    name='PCC', definition='Pearson product-moment correlation coefficient.'
)
def pcc(indicators: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluator for computing Pearson product-moment correlation coefficient.

    :param indicators: The DataFrame containing the indicators.
    :type indicators: pd.DataFrame
    :return: The computed correlation coefficients as a DataFrame.
    :rtype: pd.DataFrame
    """
    result = pd.DataFrame(
        index=indicators.columns,
        columns=[f'pcc_{x}' for x in indicators.columns],
    )

    for col1 in indicators:
        for col2 in indicators:
            correlation = indicators[col1].corr(indicators[col2])
            result.at[col1, f'pcc_{col2}'] = correlation

    return result
