"""
Тестовый скрипт для проверки DENCLUE с визуализацией
Автор: Пантелеев Артём [pantelartems@gmail.com]
"""

import argparse
from pathlib import Path
import sys

import matplotlib
if "--no-show" in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs, make_moons, make_circles
from sklearn.metrics import adjusted_rand_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ClusteringMethods.ClasteringAlgorithms import Context, StrategiesManager
from ClusteringMethods.DENCLUEClustering import ConcreteStrategyDENCLUE

ALGORITHM_NAME = "DENCLUE"
STRATEGY_ID = "denclue"
IMAGES_DIR = Path(__file__).parent / "Images" / ALGORITHM_NAME


def generate_test_data_2d(dataset_type="blobs", n_samples=180):
    """Генерация двумерных тестовых данных."""
    if dataset_type == "blobs":
        return make_blobs(n_samples=n_samples, centers=[[-3, 0], [0, 4], [3, 0]],
                          cluster_std=0.25, random_state=42)
    if dataset_type == "moons":
        return make_moons(n_samples=n_samples, noise=0.04, random_state=42)
    if dataset_type == "circles":
        return make_circles(n_samples=n_samples, factor=0.45, noise=0.03, random_state=42)
    raise ValueError(dataset_type)


def generate_test_data_3d():
    """Генерация трёхмерных тестовых данных."""
    return make_blobs(n_samples=150, n_features=3, centers=3,
                      cluster_std=0.25, random_state=42)


def run_strategy(points, **overrides):
    """Запускает стратегию и проверяет формат меток."""
    config = StrategiesManager.getStrategyRunConfigById(STRATEGY_ID)
    for name, value in overrides.items():
        config[name] = value
    labels = ConcreteStrategyDENCLUE().clastering_points(points, config)
    assert labels.shape == (len(points),)
    assert np.issubdtype(labels.dtype, np.integer)
    clusters = len(set(labels) - {-1})
    print(f"{ALGORITHM_NAME}: {len(points)} точек, {clusters} кластеров, "
          f"{np.count_nonzero(labels == -1)} точек шума")
    return labels


def save_figure(fig, filename):
    """Сохраняет рисунок в директорию результатов."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / filename, dpi=150, bbox_inches="tight")
    print(f"Сохранено: {IMAGES_DIR / filename}")


def scatter(ax, points, labels, title):
    """Отображает точки и метки кластеров."""
    if points.shape[1] == 3:
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=labels, cmap="tab10", s=15)
        ax.set_zlabel("X3")
    else:
        ax.scatter(points[:, 0], points[:, 1], c=labels, cmap="tab10", s=15)
    ax.set_title(title)
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")
    ax.grid(True, alpha=0.3)


def test_basic_2d_clustering():
    """Тест базовой кластеризации на 2D данных."""
    points, truth = generate_test_data_2d()
    labels = run_strategy(points)
    score = adjusted_rand_score(truth, labels)
    print(f"ARI: {score:.4f}")
    assert score > 0.95
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    scatter(axes[0], points, truth, "True clusters")
    scatter(axes[1], points, labels, f"{ALGORITHM_NAME}; ARI={score:.3f}")
    save_figure(fig, "test_basic_2d.png")


def test_parameter_sensitivity():
    """Тест чувствительности к параметрам."""
    points, _ = generate_test_data_2d()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, value in zip(axes.ravel(), (0.15, 0.5, 1.5, 3.0)):
        labels = run_strategy(points, sigma=value)
        scatter(ax, points, labels, f"sigma={value}")
    save_figure(fig, "test_parameters.png")


def test_different_datasets():
    """Тест на различных типах данных."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, kind in zip(axes, ("blobs", "moons", "circles")):
        points, _ = generate_test_data_2d(kind)
        options = {} if kind == "blobs" else {"sigma": 0.12, "merge_radius": 0.3}
        labels = run_strategy(points, **options)
        scatter(ax, points, labels, kind)
    save_figure(fig, "test_datasets.png")


def test_3d_clustering():
    """Тест кластеризации в 3D."""
    points, truth = generate_test_data_3d()
    labels = run_strategy(points)
    assert adjusted_rand_score(truth, labels) > 0.95
    fig = plt.figure(figsize=(11, 5))
    scatter(fig.add_subplot(121, projection="3d"), points, truth, "True clusters")
    scatter(fig.add_subplot(122, projection="3d"), points, labels, ALGORITHM_NAME)
    save_figure(fig, "test_3d.png")


def test_strategy_integration():
    """Тест интеграции со стратегией."""
    points, _ = generate_test_data_2d(n_samples=90)
    config = StrategiesManager.getStrategyRunConfigById(STRATEGY_ID)
    strategy = ConcreteStrategyDENCLUE()
    direct = strategy.clastering_points(points, config)
    contextual = Context(strategy).do_some_clustering_points(points.T, config)
    np.testing.assert_array_equal(direct, contextual)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    scatter(axes[0], points, direct, "Strategy")
    scatter(axes[1], points, contextual, "Context")
    save_figure(fig, "test_strategy.png")


def main():
    """Запускает все тесты."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-show", action="store_true", help="Сохранить PNG без графических окон")
    args = parser.parse_args()
    for test in (test_basic_2d_clustering, test_parameter_sensitivity,
                 test_different_datasets, test_3d_clustering, test_strategy_integration):
        test()
    print(f"Все 5 проверок {ALGORITHM_NAME} пройдены. Результаты: {IMAGES_DIR}")
    if args.no_show:
        plt.close("all")
    else:
        plt.show()


if __name__ == "__main__":
    main()
