"""DENCLUE с гауссовской плотностью и поиском аттракторов сдвигом среднего.

Автор: ArtemPanteleev. Дата: 2026-10-16.
Плотность — среднее гауссовских влияний без нормирующего множителя KDE.
Связность аттракторов приближается проверкой плотности вдоль отрезков.
"""

import warnings

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler

from ClusteringMethods.ClasteringAlgorithms import (
    Strategy, StrategyParamType, StrategyRunConfig, StrategiesManager,
)
from ClusteringMethods._validation import (
    prepare_features, positive_integer, positive_real,
)


class DENCLUE:
    """Плотностная кластеризация: fit_predict(X), labels_, attractors_, density_.

    xi задаётся в единицах mean(exp(-distance² / (2*sigma²))), от 0 до 1.
    Повторяющиеся точки учитываются с весами; матрица расстояний строится
    блоками. Стоимость поиска аттракторов O(max_iter * u² * d), где u —
    число различных точек. Для больших изображений следует уменьшить размер.
    """

    def __init__(self, sigma=0.5, xi=0.01, tolerance=0.0001, max_iter=200,
                 merge_radius=0.5, min_cluster_size=1, normalize=False,
                 batch_size=128):
        """Сохранить параметры; их проверка выполняется перед обучением."""
        self.sigma = sigma
        self.xi = xi
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.merge_radius = merge_radius
        self.min_cluster_size = min_cluster_size
        self.normalize = normalize
        self.batch_size = batch_size

    def _validate(self):
        """Проверить диапазоны параметров до вычисления плотности."""
        for name in ("sigma", "tolerance", "merge_radius"):
            positive_real(name, getattr(self, name))
        positive_real("xi", self.xi, allow_zero=True)
        if self.xi > 1:
            raise ValueError("xi должен принадлежать [0, 1].")
        for name in ("max_iter", "min_cluster_size", "batch_size"):
            positive_integer(name, getattr(self, name))

    def _weights(self, queries):
        """Получить гауссовские влияния с учётом кратности исходных точек."""
        distances = cdist(queries, self._samples)
        with np.errstate(over="ignore", under="ignore"):
            weights = np.exp(-0.5 * np.square(distances / self.sigma))
        return weights * self._counts

    def _density(self, queries):
        """Вычислить плотность запросов ограниченными по памяти блоками."""
        result = np.empty(len(queries))
        for start in range(0, len(queries), self.batch_size):
            block = queries[start:start + self.batch_size]
            result[start:start + len(block)] = self._weights(block).sum(axis=1) / self._counts.sum()
        return result

    def _connected(self, left, right):
        """Проверить плотностный мост с шагом не больше sigma/2.

        Это дискретная аппроксимация непрерывного условия DENCLUE.
        Концы отрезка уже проверены на плотность >= xi.
        """
        distance = np.linalg.norm(right - left)
        steps = max(2, int(np.ceil(2 * distance / self.sigma)))
        for start in range(1, steps, self.batch_size):
            fractions = np.arange(start, min(start + self.batch_size, steps)) / steps
            queries = left + fractions[:, None] * (right - left)
            if np.any(self._density(queries) < self.xi):
                return False
        return True

    def fit(self, data):
        """Найти аттракторы, объединить плотные области и присвоить шуму -1."""
        self._validate()
        features = prepare_features(data)
        self.scaler_ = StandardScaler().fit(features) if self.normalize else None
        if self.scaler_ is not None:
            features = self.scaler_.transform(features)
        # Перенос начала координат уменьшает потерю точности при больших сдвигах.
        self._origin = features[0].copy()
        with np.errstate(over="ignore", invalid="ignore"):
            features = features - self._origin
        if not np.isfinite(features).all():
            raise ValueError("Слишком большой диапазон координат; масштабируйте данные.")
        self._samples, inverse, self._counts = np.unique(
            features, axis=0, return_inverse=True, return_counts=True,
        )
        attractors = self._samples.copy()
        converged = np.zeros(len(attractors), dtype=bool)
        self.n_iter_ = 0
        for iteration in range(self.max_iter):
            active = np.flatnonzero(~converged)
            if not len(active):
                break
            for start in range(0, len(active), self.batch_size):
                indices = active[start:start + self.batch_size]
                weights = self._weights(attractors[indices])
                totals = weights.sum(axis=1)
                if np.any(totals == 0):
                    raise ValueError("Численная потеря плотности; увеличьте sigma или масштабируйте данные.")
                updated = (weights / totals[:, None]) @ self._samples
                shifts = np.linalg.norm(updated - attractors[indices], axis=1)
                converged[indices] = shifts <= self.tolerance
                attractors[indices] = updated
            self.n_iter_ = iteration + 1

        if not converged.all():
            warnings.warn("DENCLUE: часть точек не достигла аттрактора за max_iter; "
                          "им присвоен шум (-1). Увеличьте max_iter.", RuntimeWarning, stacklevel=2)
        density = self._density(attractors)
        valid = np.flatnonzero(converged & (density >= self.xi))
        labels = np.full(len(attractors), -1, dtype=np.intp)
        if len(valid):
            modes = attractors[valid]
            tree = cKDTree(modes)
            parents = np.arange(len(modes))

            def root(index):
                """Найти компоненту с уплотнением пути."""
                while parents[index] != index:
                    parents[index] = parents[parents[index]]
                    index = parents[index]
                return index

            for index, mode in enumerate(modes):
                for neighbor in tree.query_ball_point(mode, self.merge_radius):
                    if neighbor <= index:
                        continue
                    left, right = root(index), root(neighbor)
                    if left != right and self._connected(mode, modes[neighbor]):
                        parents[right] = left
            components = np.array([root(i) for i in range(len(modes))])
            next_label = 0
            for component in np.unique(components):
                indices = valid[components == component]
                if self._counts[indices].sum() >= self.min_cluster_size:
                    labels[indices] = next_label
                    next_label += 1

        self.labels_ = labels[inverse]
        # Аттракторы в координатах после опционального StandardScaler.
        self.attractors_ = (attractors + self._origin)[inverse]
        self.density_ = density[inverse]
        self.converged_ = converged[inverse]
        return self

    def fit_predict(self, data):
        """Вернуть метки в исходном порядке объектов."""
        return self.fit(data).labels_


@StrategiesManager.registerStrategy(
    "denclue", "DENCLUE", "Гауссовская плотность, аттракторы и выделение шума",
)
class ConcreteStrategyDENCLUE(Strategy):
    """Интеграция DENCLUE с точками, изображениями и параметрами GUI."""

    @classmethod
    def _setupParams(cls):
        """Описать все параметры DENCLUE для StrategyOptionsDialog."""
        cls._addParam("sigma", "Ширина гауссовского ядра", StrategyParamType.UFloating,
                      "Положительный масштаб влияния точки в единицах признаков.", 0.5)
        cls._addParam("xi", "Минимальная плотность", StrategyParamType.UFloating,
                      "От 0 до 1: порог среднего гауссовского влияния в аттракторе.", 0.01)
        cls._addParam("tolerance", "Допуск сходимости", StrategyParamType.UFloating,
                      "Положительный порог евклидова перемещения аттрактора.", 0.0001)
        cls._addParam("max_iter", "Максимальное число итераций", StrategyParamType.UNumber,
                      "Положительный лимит; несошедшиеся точки получают метку -1.", 200)
        cls._addParam("merge_radius", "Радиус объединения аттракторов", StrategyParamType.UFloating,
                      "Положительный радиус поиска соседних аттракторов; между ними проверяется плотность.", 0.5)
        cls._addParam("min_cluster_size", "Минимальный размер кластера", StrategyParamType.UNumber,
                      "Кластеры меньшего размера считаются шумом. Не меньше 1.", 1)
        cls._addParam("normalize", "Нормализовать данные", StrategyParamType.Bool,
                      "StandardScaler перед кластеризацией; sigma и радиус задаются в новом масштабе.", False)
        cls._addParam("batch_size", "Размер блока вычислений", StrategyParamType.UNumber,
                      "Число одновременно обрабатываемых точек; ограничивает память, не размер выборки.", 128)

    def _cluster(self, data, params):
        """Создать независимую модель для одного запуска стратегии."""
        return DENCLUE(**{name: params[name] for name in self.params()}).fit_predict(data)

    def clastering_points(self, points: np.ndarray, params: StrategyRunConfig) -> np.ndarray:
        """Кластеризовать матрицу точек (n_samples, n_features)."""
        return self._cluster(points, params)

    def clastering_image(self, pixels: np.ndarray, params: StrategyRunConfig) -> np.ndarray:
        """Кластеризовать матрицу пикселей (n_pixels, n_channels)."""
        return self._cluster(pixels, params)
