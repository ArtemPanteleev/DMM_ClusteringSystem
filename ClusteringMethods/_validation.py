"""Проверка входных данных DENCLUE и FCM.

Автор: ArtemPanteleev. Дата: 2026-10-16.
"""

from numbers import Integral, Real

import numpy as np


def prepare_features(data):
    """Вернуть конечную матрицу (объекты, признаки), не меняя ориентацию осей."""
    features = np.asarray(data, dtype=np.float64)
    if features.ndim == 1:
        features = features.reshape(-1, 1)
    if features.ndim != 2 or 0 in features.shape:
        raise ValueError("Ожидается непустой массив (n_samples, n_features).")
    if not np.isfinite(features).all():
        raise ValueError("Данные не должны содержать NaN или бесконечность.")
    return features


def positive_real(name, value, allow_zero=False):
    """Проверить конечное положительное (или неотрицательное) число."""
    if (isinstance(value, (bool, np.bool_)) or not isinstance(value, Real)
            or not np.isfinite(value) or value < 0
            or (not allow_zero and value == 0)):
        relation = ">= 0" if allow_zero else "> 0"
        raise ValueError(f"{name} должен быть конечным числом {relation}.")


def positive_integer(name, value, allow_zero=False):
    """Проверить целое число без неявного округления и преобразования bool."""
    if (isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral)
            or value < (0 if allow_zero else 1)):
        relation = ">= 0" if allow_zero else "> 0"
        raise ValueError(f"{name} должен быть целым числом {relation}.")
