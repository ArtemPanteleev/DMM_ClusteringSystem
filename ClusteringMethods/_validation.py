"""
Проверка входных данных DENCLUE и FCM
Автор: Пантелеев Артём [pantelartems@gmail.com]
Последнее обновление: 2026-10-17
"""

from numbers import Integral, Real

import numpy as np


def prepare_features(data):
    """Приводит входные данные к массиву (n_samples, n_features)."""
    features = np.asarray(data, dtype=np.float64)
    if features.ndim == 1:
        features = features.reshape(-1, 1)
    if features.ndim != 2 or 0 in features.shape:
        raise ValueError("Ожидается непустой массив (n_samples, n_features).")
    if not np.isfinite(features).all():
        raise ValueError("Данные не должны содержать NaN или бесконечность.")
    return features


def positive_real(name, value, allow_zero=False):
    """Проверяет конечное положительное или неотрицательное число."""
    if (isinstance(value, (bool, np.bool_)) or not isinstance(value, Real)
            or not np.isfinite(value) or value < 0
            or (not allow_zero and value == 0)):
        relation = ">= 0" if allow_zero else "> 0"
        raise ValueError(f"{name} должен быть конечным числом {relation}.")


def positive_integer(name, value, allow_zero=False):
    """Проверяет целое число без округления и преобразования bool."""
    if (isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral)
            or value < (0 if allow_zero else 1)):
        relation = ">= 0" if allow_zero else "> 0"
        raise ValueError(f"{name} должен быть целым числом {relation}.")
