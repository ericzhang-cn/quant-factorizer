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
def describe(indicators: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluator for computing basic statistics.

    :param indicators: The DataFrame containing the indicators.
    :type indicators: pd.DataFrame
    :param labels: The DataFrame containing the labels.
    :type labels: pd.DataFrame
    :return: The computed basic statistics as a transposed DataFrame.
    :rtype: pd.DataFrame
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    normalized = scaler.fit_transform(indicators)
    normalized = pd.DataFrame(normalized, columns=indicators.columns)
    return indicators.describe().T.join(
        normalized.describe().T.rename(
            columns={
                col: f'norm_{col}' for col in normalized.describe().T.columns
            },
        )
    )


@evaluator(
    name='PCC', definition='Pearson product-moment correlation coefficient.'
)
def pcc(indicators: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluator for computing Pearson product-moment correlation coefficient.

    :param indicators: The DataFrame containing the indicators.
    :type indicators: pd.DataFrame
    :param labels: The DataFrame containing the labels.
    :type labels: pd.DataFrame
    :return: The computed correlation coefficients as a DataFrame.
    :rtype: pd.DataFrame
    """
    result = pd.DataFrame(
        index=indicators.columns, columns=[f'pcc_{x}' for x in labels.columns]
    )

    for col1 in indicators:
        for col2 in labels:
            correlation = indicators[col1].corr(labels[col2])
            result.at[col1, f'pcc_{col2}'] = correlation

    return result
