import functools
import itertools
import typing

import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class Cross(BaseModel):
    """
     Cross class represents a feature cross.

    :ivar name: The name of the feature cross.
    :vartype name: str
    :ivar definition: The definition or description of the feature cross.
    :vartype definition: str
    :ivar func: The function that performs the feature cross and returns a pandas DataFrame.
    :vartype func: typing.Callable[..., pd.DataFrame]
    """

    name: str
    definition: str
    func: typing.Callable[..., pd.DataFrame]


cross_registry: dict[str, Cross] = {}


def cross(name: str, definition: str = ''):
    """
    Decorator that registers a function as a cross operation.

    :param name: The name of the cross operation.
    :type name: str
    :param definition: The definition of the cross operation (optional).
    :type definition: str, default ''
    :return: The decorated function.
    :rtype: function
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            df = args[0]
            order = kwargs.get('order', 2)
            cols = df.columns.tolist()
            order = max(order, 2)
            order = min(order, len(cols))
            kwargs['order'] = order

            result = func(*args, **kwargs)

            result['time'] = args[0].index.copy()
            result.set_index('time', inplace=True)

            return result

        cross_registry[name] = Cross(
            name=name,
            definition=definition,
            func=wrapper,
        )

        return wrapper

    return decorator


def _get_perm_or_comb(
    *, cols: list[str], order: int = 2, sequential_sensitive: bool = False
) -> list[tuple[str, str]]:
    """
    Get permutations or combinations of multiple technical indicators.

    :param cols: A list of column names representing the technical indicators.
    :type cols: list[str]
    :param order: An integer indicating the order of permutations or combinations (default is 2).
    :type: order: int
    :param sequential_sensitive: A boolean indicating whether the order of elements matters (default is False).
    :type sequential_sensitive: bool
    :return: A list of tuples representing the permutations or combinations of the technical indicators.
    :rtype: list[tuple[str, str]]
    """
    if sequential_sensitive:
        perm_or_comb = list(itertools.permutations(cols, order))
    else:
        perm_or_comb = list(itertools.combinations(cols, order))
    return perm_or_comb


@cross(name='MUL', definition='Multiply Multiple Technical Indicators.')
def mul(
    indicators: pd.DataFrame,
    *,
    order: int = 2,
) -> pd.DataFrame:
    """
    Multiply Multiple Technical Indicators.

    This function multiplies multiple technical indicators together to create new columns in the DataFrame.

    :param indicators: A pandas DataFrame containing the technical indicators.
    :type indicators: pd.DataFrame
    :param order: An optional integer indicating the order of permutations or combinations (default is 2).
    :type order: int
    :return: A pandas DataFrame with the multiplied technical indicators as new columns.
    :rtype: pd.DataFrame
    """
    perm_or_comb = _get_perm_or_comb(
        cols=indicators.columns.tolist(),
        order=order,
        sequential_sensitive=False,
    )

    df = pd.DataFrame()
    for e in perm_or_comb:
        key_name = '__'.join(e)
        key_name = f'mul_{key_name}'
        df[key_name] = indicators[list(e)].prod(axis=1)

    return df


@cross(name='W_SUM', definition='Weighted sum.')
def w_sum(
    indicators: pd.DataFrame,
    *,
    order: int = 2,
    weights: tuple[tuple[float]] = ((0.5, 0.5),),
) -> pd.DataFrame:
    perm_or_comb = _get_perm_or_comb(
        cols=indicators.columns.tolist(),
        order=order,
        sequential_sensitive=True,
    )

    df = pd.DataFrame()
    for w in weights:
        if len(w) != order:
            continue
        for e in perm_or_comb:
            key_name = '__'.join(e)
            key_name = f'w_sum_{"_".join([str(x) for x in w])}_{key_name}'
            df[key_name] = np.dot(indicators[list(e)], w)

    df.index = indicators.index
    return df


@cross(name='PCA', definition='Principal component analysis.')
def pca(
    indicators: pd.DataFrame,
    *,
    order: int = -1,
    n_components: int = 1,
) -> pd.DataFrame:
    """
    Perform Principal Component Analysis (PCA) on the given indicators.

    :param indicators: A pandas DataFrame containing the indicators.
    :param order: The order of the PCA analysis. Default is -1.
    :param n_components: The number of principal components to retain. Default is 1.
    :return: A pandas DataFrame with the PCA results.

    :raises: None

    Example:
    >>> indicators_ = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> pca(indicators_, n_components=2)
       pca_1  pca_2
    0  -1.0    0.0
    1   0.0    0.0
    2   1.0    0.0
    """
    scaler = StandardScaler()
    scaled = scaler.fit_transform(
        indicators.fillna(indicators.mean(), inplace=False)
    )
    pca_ = PCA(n_components=n_components)
    pca_result = pca_.fit_transform(scaled)
    df = pd.DataFrame(
        pca_result, columns=[f'pca_{i + 1}' for i in range(n_components)]
    )
    df.index = indicators.index.copy()

    return df
