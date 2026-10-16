"""
Тестовый скрипт для проверки DENCLUE и FCM (PyClustering)
Автор: Пантелеев Артём [pantelartems@gmail.com]
"""

import unittest
from unittest.mock import patch

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score

from ClusteringMethods.ClasteringAlgorithms import Context, StrategiesManager
from ClusteringMethods.DENCLUEClustering import DENCLUE, ConcreteStrategyDENCLUE
from ClusteringMethods.FCMClustering import ConcreteStrategyFCM_from_PYCLUSTERING


def configuration(strategy_id, **values):
    """Получить настоящую конфигурацию реестра с указанными параметрами."""
    config = StrategiesManager.getStrategyRunConfigById(strategy_id)
    for key, value in values.items():
        config[key] = value
    return config


class DENCLUERegressionTests(unittest.TestCase):
    """Плотность, шум, сходимость, масштаб и контракт результата."""

    def test_separated_clusters_and_noise(self):
        """Два плотных облака должны отделяться от изолированного выброса."""
        points, truth = make_blobs(n_samples=80, centers=[[-3, 0], [3, 0]],
                                  cluster_std=0.15, random_state=42)
        points = np.vstack([points, [30, 30]])
        labels = ConcreteStrategyDENCLUE().clastering_points(
            points, configuration("denclue", xi=0.05))
        self.assertEqual(labels[-1], -1)
        self.assertGreater(adjusted_rand_score(truth, labels[:-1]), 0.99)

    def test_density_definition_and_duplicates(self):
        """Плотность учитывает каждое повторение, а не только уникальные точки."""
        points = np.array([[0.], [0.], [0.], [10.]])
        model = DENCLUE(sigma=0.1, xi=0.5).fit(points)
        assert_allclose(model.density_, [0.75, 0.75, 0.75, 0.25])
        assert_array_equal(model.labels_, [0, 0, 0, -1])

    def test_density_bridge_blocks_merging(self):
        """Даже большой радиус не соединяет моды через провал плотности."""
        points = np.repeat([[-3.], [3.]], 10, axis=0)
        labels = DENCLUE(sigma=0.2, xi=0.1, merge_radius=10.).fit_predict(points)
        self.assertEqual(len(np.unique(labels)), 2)

    def test_minimum_size_and_all_noise(self):
        """Малые кластеры и области ниже порога сохраняют длину массива меток."""
        points = np.array([[0.], [0.], [5.]])
        assert_array_equal(DENCLUE(sigma=0.1, min_cluster_size=2).fit_predict(points), [0, 0, -1])
        assert_array_equal(DENCLUE(sigma=0.1, xi=1.).fit_predict(points), [-1, -1, -1])

    def test_density_bridge_connects_modes(self):
        """Разные моды объединяются при наличии достаточно плотного моста."""
        points = np.repeat([[0.], [0.5]], 10, axis=0)
        split = DENCLUE(sigma=0.15, xi=0.01, merge_radius=0.2).fit_predict(points)
        merged = DENCLUE(sigma=0.15, xi=0.01, merge_radius=0.6).fit_predict(points)
        self.assertEqual(len(np.unique(split)), 2)
        assert_array_equal(merged, np.zeros(20, dtype=int))

    def test_unconverged_points_are_noise(self):
        """Лимит итераций не превращает незавершённые траектории в аттракторы."""
        with self.assertWarnsRegex(RuntimeWarning, "max_iter"):
            model = DENCLUE(max_iter=1, tolerance=1e-12).fit([[0.], [0.2], [0.9]])
        self.assertTrue(np.all(model.labels_[~model.converged_] == -1))

    def test_batch_size_and_scaling(self):
        """Блоки не меняют решение; StandardScaler компенсирует масштабы осей."""
        points, _ = make_blobs(n_samples=50, centers=2, random_state=42)
        first = DENCLUE(normalize=True, batch_size=1).fit_predict(points)
        second = DENCLUE(normalize=True, batch_size=64).fit_predict(points * [10, 0.2] + 4)
        self.assertEqual(adjusted_rand_score(first, second), 1.)

    def test_one_point_and_high_dimension(self):
        """Одна точка и матрица с числом признаков больше числа объектов."""
        assert_array_equal(DENCLUE().fit_predict([[1., 2., 3.]]), [0])
        labels = DENCLUE().fit_predict(np.array([[0.] * 12, [10.] * 12]))
        self.assertEqual(labels.shape, (2,))
        self.assertEqual(len(np.unique(labels)), 2)

    def test_parameter_validation(self):
        """Неправильные диапазоны должны отвергаться до расчёта."""
        for key, value in [("sigma", 0.), ("sigma", float("nan")), ("xi", -0.1),
                           ("xi", 1.1), ("max_iter", 0), ("max_iter", 1.5),
                           ("min_cluster_size", 0), ("batch_size", 0),
                           ("merge_radius", 0.), ("tolerance", float("inf"))]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                DENCLUE(**{key: value}).fit([[0.], [1.]])


class FCMRegressionTests(unittest.TestCase):
    """Интеграция pyclustering, воспроизводимость и проверка параметров."""

    def test_quality_initialization_and_reproducibility(self):
        """Обе инициализации воспроизводимы и разделяют простые облака."""
        points, truth = make_blobs(n_samples=75, centers=[[-5, 0], [0, 5], [5, 0]],
                                  cluster_std=0.25, random_state=42)
        for init in ("kmeans++", "random"):
            with self.subTest(init=init):
                config = configuration("fcm_pyc", init=init, ccore=False)
                strategy = ConcreteStrategyFCM_from_PYCLUSTERING()
                labels = strategy.clastering_points(points, config)
                assert_array_equal(labels, strategy.clastering_points(points, config))
                self.assertGreater(adjusted_rand_score(truth, labels), 0.99)

    def test_constant_data(self):
        """Один кластер на совпадающих точках даёт конечные результаты."""
        labels = ConcreteStrategyFCM_from_PYCLUSTERING().clastering_points(
            np.ones((5, 3)), configuration("fcm_pyc", n_clusters=1, ccore=False))
        assert_array_equal(labels, np.zeros(5, dtype=int))

    def test_exact_color_partition(self):
        """Изображение из двух цветов не должно схлопываться в один кластер."""
        pixels = np.repeat([[0., 0., 0.], [255., 255., 255.]], 10, axis=0)
        labels = ConcreteStrategyFCM_from_PYCLUSTERING().clastering_image(
            pixels, configuration("fcm_pyc", n_clusters=2, ccore=False))
        self.assertEqual(adjusted_rand_score(np.repeat([0, 1], 10), labels), 1.)

    def test_does_not_reset_global_rng_or_modify_input(self):
        """Seed влияет только на локальную инициализацию центров."""
        points, _ = make_blobs(n_samples=20, centers=2, random_state=42)
        original = points.copy()
        before = np.random.get_state()
        ConcreteStrategyFCM_from_PYCLUSTERING().clastering_points(
            points, configuration("fcm_pyc", n_clusters=2, normalize=True, ccore=False))
        after = np.random.get_state()
        assert_array_equal(before[1], after[1])
        self.assertEqual(before[2:], after[2:])
        assert_array_equal(points, original)

    def test_parameter_validation(self):
        """Ошибочные параметры не должны приводить к делению на ноль в библиотеке."""
        for key, value in [("m", 1.), ("m", float("inf")), ("tolerance", 0.),
                           ("n_clusters", 0), ("n_clusters", 4), ("itermax", 0),
                           ("random_state", 2**32)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                ConcreteStrategyFCM_from_PYCLUSTERING().clastering_points(
                    [[0.], [1.], [2.]], configuration("fcm_pyc", **{key: value}))

    def test_ccore_load_failure_falls_back(self):
        """Ошибка загрузки CCORE должна приводить к повторному запуску на Python."""
        from pyclustering.cluster.fcm import fcm

        def factory(*args, **kwargs):
            """Эмулировать платформу без CCORE, сохранив реальное вычисление FCM."""
            if kwargs["ccore"]:
                raise OSError("CCORE unavailable")
            return fcm(*args, **kwargs)

        points, _ = make_blobs(n_samples=20, centers=2, random_state=42)
        with patch("ClusteringMethods.FCMClustering.fcm", side_effect=factory) as wrapped:
            labels = ConcreteStrategyFCM_from_PYCLUSTERING().clastering_points(
                points, configuration("fcm_pyc", n_clusters=2))
        self.assertEqual(labels.shape, (20,))
        self.assertEqual(wrapped.call_count, 2)
        self.assertFalse(wrapped.call_args.kwargs["ccore"])

    def test_parameters_reach_backend(self):
        """Проверить передачу расширенных параметров, включая стандартизацию."""
        from pyclustering.cluster.fcm import fcm
        points, _ = make_blobs(n_samples=25, centers=2, random_state=42)
        config = configuration("fcm_pyc", n_clusters=2, normalize=True,
                               m=2.5, tolerance=0.002, itermax=30, ccore=False)
        with patch("ClusteringMethods.FCMClustering.fcm", wraps=fcm) as wrapped:
            ConcreteStrategyFCM_from_PYCLUSTERING().clastering_points(points, config)
        assert_allclose(wrapped.call_args.args[0].mean(axis=0), 0, atol=1e-12)
        assert_allclose(wrapped.call_args.args[0].std(axis=0), 1)
        for key in ("m", "tolerance", "itermax", "ccore"):
            self.assertEqual(wrapped.call_args.kwargs[key], config[key])


class StrategyIntegrationTests(unittest.TestCase):
    """Контракт общего Context и независимость от существующего FCM."""

    def test_registry(self):
        """Оба FCM и DENCLUE зарегистрированы с независимыми параметрами."""
        registry = StrategiesManager.strategies()
        for key in ("denclue", "fcm_pyc", "fuzzy_cmeans"):
            self.assertIn(key, registry)
        self.assertNotIn("ccore", configuration("fuzzy_cmeans").params)

    def test_context_points_and_images(self):
        """Context транспонирует точки и разворачивает RGB без потери пикселей."""
        rng = np.random.default_rng(42)
        image = np.clip(np.vstack([rng.normal(30, 2, (18, 3)),
                                   rng.normal(220, 2, (18, 3))]), 0, 255).astype(np.uint8).reshape(6, 6, 3)
        flat = image.reshape(-1, 3)
        for key, strategy, options in (
                ("denclue", ConcreteStrategyDENCLUE(), {"sigma": 10.}),
                ("fcm_pyc", ConcreteStrategyFCM_from_PYCLUSTERING(), {"n_clusters": 2, "ccore": False})):
            with self.subTest(strategy=key):
                config = configuration(key, **options)
                direct = strategy.clastering_points(flat, config)
                assert_array_equal(direct, Context(strategy).do_some_clustering_points(flat.T, config))
                assert_array_equal(direct, Context(strategy).do_some_clustering_image(image, config, 1))
                assert_array_equal(direct, Context(strategy).do_some_clustering_image(flat, config, 0))
                self.assertEqual(direct.shape, (36,))
                self.assertTrue(np.issubdtype(direct.dtype, np.integer))

    def test_invalid_data(self):
        """Пустые, нечисловые и бесконечные данные отвергаются явно."""
        for key, strategy in (("denclue", ConcreteStrategyDENCLUE()),
                              ("fcm_pyc", ConcreteStrategyFCM_from_PYCLUSTERING())):
            for data in ([], np.empty((2, 0)), [[[1.]]], [[float("nan")]], [[float("inf")]], [["x"]]):
                with self.subTest(strategy=key, data=data), self.assertRaises(ValueError):
                    strategy.clastering_points(data, configuration(key))


if __name__ == "__main__":
    unittest.main()
