"""
FCM Algorithm Implementation
Автор: Пантелеев Артём [pantelartems@gmail.com]
Последнее обновление: 2026-10-17

Кластеризация методом Fuzzy C-Means на базе pyclustering.cluster.fcm.

Алгоритм вычисляет степени принадлежности точек к кластерам и обновляет
их центры. Для отображения в интерфейсе каждой точке присваивается метка
кластера с наибольшей степенью принадлежности.

Ограничения:
- Начальные центры выбираются через sklearn.cluster.kmeans_plusplus:
  pyclustering.cluster.center_initializer не работает с numpy >= 2
  (обращается к удалённому numpy.warnings).
- C++ часть pyclustering (ccore) собрана не для всех платформ
  (например, отсутствует для macOS arm64). Если её не удаётся
  загрузить, используется реализация на Python.
- Если число кластеров равно числу различных точек, возвращается точное
  разбиение по координатам. Это обходит ошибку нулевых расстояний pyclustering.

Источник:
https://github.com/annoviko/pyclustering/blob/master/pyclustering/cluster/fcm.py
"""

import numpy as np
from pyclustering.cluster.fcm import fcm
from sklearn.cluster import kmeans_plusplus
from sklearn.preprocessing import StandardScaler

from ClusteringMethods.ClasteringAlgorithms import (
    Strategy, StrategyParamType, StrategyRunConfig, StrategiesManager,
)
from ClusteringMethods._validation import (
    prepare_features, positive_integer, positive_real,
)


@StrategiesManager.registerStrategy(
    "fcm_pyc", "FCM (PyClustering)",
    "Расширенный Fuzzy C-Means: выбор начальных центров и нормализация",
)
class ConcreteStrategyFCM_from_PYCLUSTERING(Strategy):
    """Стратегия кластеризации методом FCM из pyclustering."""

    @classmethod
    def _setupParams(cls):
        """Инициализирует параметры стратегии FCM."""
        cls._addParam("n_clusters", "Количество кластеров", StrategyParamType.UNumber,
                      "От 1 до количества различных объектов в данных.", 3)
        cls._addParam("m", "Фаззи-фактор", StrategyParamType.UFloating,
                      "Степень нечёткости кластеров; строго больше 1.", 2.0)
        cls._addParam("tolerance", "Допуск перемещения центров", StrategyParamType.UFloating,
                      "Порог максимального квадрата смещения центра; строго больше 0.", 0.001)
        cls._addParam("itermax", "Максимальное число итераций", StrategyParamType.UNumber,
                      "Положительное ограничение числа итераций FCM.", 200)
        cls._addParam("init", "Инициализация центров", StrategyParamType.Switch,
                      "kmeans++ или случайный выбор различных объектов.", "kmeans++",
                      switches=["kmeans++", "random"])
        cls._addParam("random_state", "Состояние случайности", StrategyParamType.UNumber,
                      "Seed начальных центров: целое число от 0 до 4294967295.", 42)
        cls._addParam("normalize", "Нормализовать данные", StrategyParamType.Bool,
                      "StandardScaler: нулевое среднее и единичная дисперсия признаков.", False)
        cls._addParam("ccore", "Использовать C++", StrategyParamType.Bool,
                      "Использовать CCORE, если доступно; иначе перейти на Python.", True)

    def _cluster(self, data, params):
        """Запускает FCM и возвращает метки кластеров."""
        features = prepare_features(data)
        for name in ("n_clusters", "itermax"):
            positive_integer(name, params[name])
        positive_integer("random_state", params["random_state"], allow_zero=True)
        if params["random_state"] > 2**32 - 1:
            raise ValueError("random_state должен быть не больше 4294967295.")
        positive_real("m", params["m"])
        if params["m"] <= 1:
            raise ValueError("m должен быть строго больше 1.")
        positive_real("tolerance", params["tolerance"])
        if params["init"] not in ("kmeans++", "random"):
            raise ValueError("init должен быть kmeans++ или random.")

        if params["normalize"]:
            features = StandardScaler().fit_transform(features)
        unique, inverse = np.unique(features, axis=0, return_inverse=True)
        n_clusters = params["n_clusters"]
        if n_clusters > len(unique):
            raise ValueError("n_clusters превышает количество различных объектов.")
        # Точное разбиение с нулевой целевой функцией обходит ошибку
        # обработки нулевых расстояний в pyclustering 0.10.1.2.
        if n_clusters == len(unique):
            return inverse.astype(np.intp, copy=False)

        if params["init"] == "kmeans++":
            centers, _ = kmeans_plusplus(features, n_clusters,
                                         random_state=params["random_state"])
        else:
            rng = np.random.default_rng(params["random_state"])
            centers = unique[rng.choice(len(unique), n_clusters, replace=False)]

        kwargs = {name: params[name] for name in ("m", "tolerance", "itermax")}
        try:
            model = fcm(features, centers, ccore=params["ccore"], **kwargs)
            model.process()
        except OSError:
            if not params["ccore"]:
                raise
            model = fcm(features, centers, ccore=False, **kwargs)
            model.process()

        labels = np.full(len(features), -1, dtype=np.intp)
        for index, cluster in enumerate(model.get_clusters()):
            labels[cluster] = index
        if (np.any(labels < 0) or not np.isfinite(model.get_centers()).all()
                or not np.isfinite(model.get_membership()).all()):
            raise ValueError("FCM не получил конечное разбиение; проверьте масштаб данных и m.")
        return labels

    def clastering_points(self, points: np.ndarray, params: StrategyRunConfig) -> np.ndarray:
        """
        Кластеризация точек методом FCM.

        Parameters:
        -----------
        points : ndarray
            Точки данных в виде массива (n_samples, n_features).
        params : StrategyRunConfig
            Параметры запуска стратегии.

        Returns:
        --------
        ndarray
            Метка кластера для каждой точки.
        """
        return self._cluster(points, params)

    def clastering_image(self, pixels: np.ndarray, params: StrategyRunConfig) -> np.ndarray:
        """
        Кластеризация изображения методом FCM.

        Parameters:
        -----------
        pixels : ndarray
            Пиксели изображения в виде массива признаков.
        params : StrategyRunConfig
            Параметры запуска стратегии.

        Returns:
        --------
        ndarray
            Метка кластера для каждого пикселя.
        """
        return self._cluster(pixels, params)
