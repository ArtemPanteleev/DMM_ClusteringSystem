# DENCLUE и расширенный FCM

Автор: ArtemPanteleev. Дата: 2026-10-16.

## Назначение и интеграция

Добавлены две независимые стратегии:

| ID | Название в GUI | Реализация |
|---|---|---|
| `denclue` | DENCLUE | Собственная реализация на NumPy/SciPy |
| `fcm_pyc` | FCM (PyClustering) | `pyclustering.cluster.fcm.fcm` |

Существующая стратегия `fuzzy_cmeans` (scikit-fuzzy) сохранена вместе с её
параметрами и тестами. DENCLUE отсутствует в pyclustering 0.10.1.2, поэтому
для него реализован отдельный класс `DENCLUE`. Новые зависимости не нужны.

Методы следуют [правилам добавления стратегии](Как%20добавить%20новый%20метод%20кластеризации.md):
наследуют `Strategy`, регистрируются декоратором `StrategiesManager.registerStrategy`,
описывают настройки в `_setupParams` и реализуют `clastering_points` и
`clastering_image`. Импорт и регистрация происходят в `ClusteringMethods/__init__.py`.
GUI получает все поля автоматически, изменения `.ui` не нужны.

## Контракт данных

Прямой вызов стратегии принимает числовую матрицу **(число объектов, число признаков)**.
Одномерный массив интерпретируется как один признак. Матрицы не транспонируются
по эвристике: две точки с 12 признаками остаются двумя точками.

- `clastering_points(X, config)` и `clastering_image(pixels, config)` возвращают
  одномерный целочисленный массив длины `len(X)` / `len(pixels)`.
- В `Context.do_some_clustering_points` нужно передавать **X.T**, как в существующих тестах.
- `Context.do_some_clustering_image(image, config, 1)` разворачивает цветное изображение
  `(height, width, channels)` в матрицу пикселей. При `i=0` передайте уже развёрнутые пиксели.
- Пустые данные, нулевая размерность признаков, NaN, бесконечности и неправильные
  диапазоны параметров вызывают `ValueError`. GUI показывает сообщение об ошибке метода.
- Исходный массив не изменяется.

## DENCLUE

**Импорт и сигнатура:**

```python
from ClusteringMethods.DENCLUEClustering import DENCLUE, ConcreteStrategyDENCLUE

DENCLUE(sigma=0.5, xi=0.01, tolerance=0.0001, max_iter=200,
        merge_radius=0.5, min_cluster_size=1, normalize=False, batch_size=128)
```

| Параметр | Тип / по умолчанию | Назначение |
|---|---|---|
| `sigma` | float / 0.5 | Ширина гауссовского ядра, строго > 0 |
| `xi` | float / 0.01 | Минимальная плотность аттрактора, диапазон [0, 1] |
| `tolerance` | float / 0.0001 | Допустимое евклидово смещение точки на итерации, > 0 |
| `max_iter` | int / 200 | Лимит итераций поиска аттракторов, > 0 |
| `merge_radius` | float / 0.5 | Радиус поиска соседних аттракторов, > 0 |
| `min_cluster_size` | int / 1 | Минимальное число исходных объектов в кластере, > 0 |
| `normalize` | bool / False | Применить StandardScaler перед вычислениями |
| `batch_size` | int / 128 | Число запросов в блоке расстояний, > 0 |

Плотность определяется как **среднее гауссовских влияний**:

$$f(x)=\frac{1}{n}\sum_{i=1}^{n}\exp\left(-\frac{\|x-x_i\|^2}{2\sigma^2}\right).$$

Множитель нормировки KDE `(2*pi*sigma²)^(-d/2)` не используется.
Поэтому `xi` не является ни числом соседей, ни плотностью вероятности в единицах KDE.
Если источник использует сумму влияний, его порог нужно разделить на `n`.

Каждая точка движется к аттрактору по гауссовскому взвешенному среднему. Повторения
сжимаются для вычислений, но сохраняют исходную кратность в плотности, размере
кластера и выходных метках. Близкие аттракторы объединяются, если плотность вдоль
соединяющего их отрезка не опускается ниже `xi`. Отрезок проверяется дискретно,
с шагом не более `sigma/2`, включая середину. Это **численная аппроксимация**
плотностной связности, ограниченная `merge_radius`, а не точная проверка всех
непрерывных путей произвольной формы.

Метка `-1` означает шум: низкая плотность аттрактора, слишком маленький кластер
или отсутствие сходимости за `max_iter`. В последнем случае выдаётся `RuntimeWarning`.
Можно увеличить `max_iter` и проверить `model.converged_`.

После `fit(X)` доступны `labels_`, `attractors_`, `density_`, `converged_`,
`n_iter_` и `scaler_`. Аттракторы возвращаются в пространстве после опционального
StandardScaler; для исходного масштаба используйте `scaler_.inverse_transform`.

**Ограничения:** поиск имеет стоимость `O(max_iter * u² * d)`, где `u` — число
уникальных точек; дополнительная проверка связности также требует вычисления
плотности. Память матрицы расстояний ограничена `O(batch_size * u)`.
Это реализация для исследовательских выборок, без ускоряющего grid-индекса
оригинальной публикации. Начинайте со 100–300 точек или маленьких изображений.
`batch_size` уменьшает расход памяти, но не делает большую выборку вычислительно дешёвой.

Для RGB 0–255 `sigma=0.5` обычно слишком мало: используйте, например, `sigma=15.0`,
`merge_radius=15.0` либо `normalize=True` и подберите параметры в новом масштабе.

## FCM (PyClustering)

**Импорт:**

```python
from ClusteringMethods.FCMClustering import ConcreteStrategyFCM_from_PYCLUSTERING
```

**Базовый вызов библиотеки:**

```python
from pyclustering.cluster.fcm import fcm
model = fcm(data, initial_centers, m=2.0, tolerance=0.001, itermax=200, ccore=True)
model.process()
```

| Параметр стратегии | Тип / по умолчанию | Назначение |
|---|---|---|
| `n_clusters` | int / 3 | От 1 до числа различных объектов |
| `m` | float / 2.0 | Фаззи-фактор, строго > 1 |
| `tolerance` | float / 0.001 | Порог максимального **квадрата** смещения центра, > 0 |
| `itermax` | int / 200 | Максимальное число итераций, > 0 |
| `init` | str / kmeans++ | `kmeans++` или `random` |
| `random_state` | int / 42 | Seed инициализации, от 0 до 2³²−1 |
| `normalize` | bool / False | StandardScaler до инициализации центров |
| `ccore` | bool / True | C++ при доступности, иначе Python |

Инициализация `kmeans++` использует scikit-learn и избегает несовместимости
инициализатора pyclustering с NumPy 2. `random` выбирает различные координаты
локальным генератором NumPy. Значение seed обеспечивает повторяемость при одинаковых
данных, параметрах и вычислительном backend. Глобальный генератор случайных чисел
не переустанавливается. При ошибке загрузки CCORE запуск повторяется с `ccore=False`.

Стратегия передаёт `m`, `tolerance`, `itermax` в pyclustering и преобразует
индексы `get_clusters()` в метки исходных строк. Нечёткое разбиение внутри библиотеки
превращается в жёсткие метки для существующего GUI. Число непустых кластеров может
оказаться меньше `n_clusters`. Совпадение результатов с `fuzzy_cmeans` не гарантируется:
у библиотек разные реализации, инициализация и критерии остановки.

Если `n_clusters` совпадает с числом различных точек, возвращается точное
разбиение по совпадению координат без итераций: оно даёт нулевую целевую функцию.
Это также обходит ошибку обработки нулевых расстояний в pyclustering 0.10.1.2,
из-за которой изображение из двух цветов может схлопнуться в один кластер.
В этом частном случае параметры итераций и инициализации не влияют на результат.

FCM рассчитан на компактные облака и не выделяет шум отдельной меткой. На кольцах
и полумесяцах правильное разделение по форме не гарантируется.

## Пример через Strategy

Запускать из корня репозитория в активированном окружении:

```python
from sklearn.datasets import make_blobs
from ClusteringMethods.ClasteringAlgorithms import StrategiesManager, Context
from ClusteringMethods.DENCLUEClustering import ConcreteStrategyDENCLUE
from ClusteringMethods.FCMClustering import ConcreteStrategyFCM_from_PYCLUSTERING

X, _ = make_blobs(n_samples=150, centers=3, cluster_std=0.3, random_state=42)

config = StrategiesManager.getStrategyRunConfigById("denclue")
config["sigma"] = 0.5
labels_denclue = Context(ConcreteStrategyDENCLUE()).do_some_clustering_points(X.T, config)

config = StrategiesManager.getStrategyRunConfigById("fcm_pyc")
config["n_clusters"] = 3
config["init"] = "kmeans++"
config["random_state"] = 42
labels_fcm = ConcreteStrategyFCM_from_PYCLUSTERING().clastering_points(X, config)
print(labels_denclue.shape, labels_fcm.shape)  # (150,) (150,)
```

## Проверки

```bash
python -m unittest TestMethods.test_denclue_fcm_regression -v
python TestMethods/test_denclue.py --no-show
python TestMethods/test_fcm_pyc.py --no-show
```

Последние две команды выполняют пять стандартных проверок: 2D, чувствительность к
параметрам, разные датасеты, 3D и интеграция с Context. PNG сохраняются в
`TestMethods/Images/DENCLUE/` и `TestMethods/Images/FCM_PyClustering/`:
`test_basic_2d.png`, `test_parameters.png`, `test_datasets.png`, `test_3d.png`,
`test_strategy.png`. Без `--no-show` после проверок откроются окна matplotlib.

Автоматические проверки дополнительно проверяют шум, кратность точек, плотностный
мост, сходимость, размер блока, нормализацию, валидацию, fallback CCORE и RGB.
Ошибка проверки возвращает ненулевой код процесса.

## Источники

- [Hinneburg, Keim: DENCLUE, KDD 1998](https://s.aaai.org/Papers/KDD/1998/KDD98-009.pdf).
- [Исходный код FCM в pyclustering](https://github.com/annoviko/pyclustering/blob/master/pyclustering/cluster/fcm.py).
- [Существующая реализация scikit-fuzzy](https://scikit-fuzzy.github.io/scikit-fuzzy/_modules/skfuzzy/cluster/_cmeans.html).
