# Документация по методам кластеризации

## Авторы
- **Mineev S. A.** [mineeff20@yandex.ru]
- **Meshkova O. V.** [oxn.lar5@yandex.ru]
- **Kozlov A. I.** [alex_kozlov15@mail.ru]

Ниже представлены методы кластеризации, используемые в проекте версии v1.1. Включены как подробные описания параметров, так и практические примеры использования, чтобы сделать работу с кодом более понятной и легкой для дальнейшего улучшения.

### 1. BIRCH из библиотеки scikit-learn

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import Birch
```

**Описание метода:**
Метод BIRCH (Balanced Iterative Reducing and Clustering using Hierarchies) из библиотеки scikit-learn используется для кластеризации больших наборов данных, работая с ограниченными вычислительными ресурсами.

**Сигнатура:**
```python
class sklearn.cluster.Birch(
    *, threshold=0.5, branching_factor=50, n_clusters=3, compute_labels=True, copy=True
)
```

**Параметры:**
- **threshold** (*float*, по умолчанию 0.5): Радиус подкластера, полученный путем слияния нового образца и ближайшего подкластерного центра. Если радиус превышает значение порога, создается новый подкластер. Установка низкого значения способствует более дробному делению кластеров.

- **branching_factor** (*int*, по умолчанию 50): Максимальное количество подкластеров (CF) в каждом узле. Если количество подкластеров превышает значение этого параметра, узел разделяется на два, что приводит к перераспределению подкластеров между ними.

- **n_clusters** (*int, экземпляр модели sklearn.cluster или None*, по умолчанию 3): Количество кластеров на завершающем этапе. Листовые подгруппы рассматриваются как новые точки данных.

- **compute_labels** (*bool*, по умолчанию True): Определяет, вычислять ли метки для каждого объекта данных.

- **copy** (*bool*, по умолчанию True): Определяет, следует ли создавать копию входных данных. Если False, исходные данные будут изменены.


**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.Birch.html)

---

### 2. BIRCH из библиотеки pyclustering

**Установка:**
```bash
python -m pip install pyclustering
```
**Импорт:**
```python
from pyclustering.cluster.birch import birch
from pyclustering.container.cftree import measurement_type
```

**Описание метода:**
Метод BIRCH из библиотеки pyclustering используется для создания CF-дерева и дальнейшей кластеризации данных с использованием заданных параметров.

**Сигнатура:**
```python
birch(
    data, number_clusters=3, branching_factor=50, max_node_entries=3,
    diameter=0.5, type_measurement=measurement_type.CENTROID_EUCLIDEAN_DISTANCE,
    entry_size_limit=500, diameter_multiplier=1.5, ccore=True
)
```

**Параметры:**
- **data** (*list*): Входные данные, представленные в виде списка точек, каждая из которых является списком координат.

- **number_clusters** (*int*, по умолчанию 3): Количество кластеров, которые нужно выделить.

- **branching_factor** (*int*, по умолчанию 50): Максимальное количество подгрупп (CF) в каждом нелистовом узле CF-дерева.

- **max_node_entries** (*int*, по умолчанию 200): Максимальное количество элементов, которые могут содержаться в каждом листовом узле CF-дерева.

- **diameter** (*float*, по умолчанию 0.5): Диаметр CF-входного узла, используемый для построения дерева. Может увеличиваться, если превышен лимит элементов в узле.

- **type_measurement** (*measurement_type*, по умолчанию `measurement_type.CENTROID_EUCLIDEAN_DISTANCE`): Тип метрики, используемой для вычисления расстояний.

- **entry_size_limit** (*int*, по умолчанию 500): Максимальное количество записей, которое может быть в дереве. Если лимит превышен, диаметр увеличивается, и дерево перестраивается.

- **diameter_multiplier** (*float*, по умолчанию 1.5): Множитель для увеличения диаметра при превышении лимита записей.

- **ccore** (*bool*, по умолчанию True): Если True, то для обработки используется часть библиотеки C++.


**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/d6/d00/classpyclustering_1_1cluster_1_1birch_1_1birch.html)

---

### 3. CURE из библиотеки pyclustering

**Установка:**
```bash
python -m pip install pyclustering
```
**Импорт:**
```python
from pyclustering.cluster.cure import cure
```

**Описание метода:**
Метод CURE (Clustering Using Representatives) используется для уменьшения размеров кластеров путем сжатия выбранных репрезентативных точек.

**Сигнатура:**
```python
cure(data, number_clusters=3, number_represent_points=5, compression=0.5, ccore=True)
```

**Параметры:**
- **data** (*list*): Входные данные, представленные в виде списка точек (объектов), где каждая точка - это список координат.

- **number_clusters** (*int*, по умолчанию 3): Количество кластеров, которые должны быть выделены.

- **number_represent_points** (*int*, по умолчанию 5): Количество репрезентативных точек для каждого кластера.

- **compression** (*float*, по умолчанию 0.5): Коэффициент, определяющий уровень сжатия точек представления к центроиду нового кластера после объединения.

- **ccore** (*bool*, по умолчанию True): Если True, то для обработки используется часть библиотеки C++.


**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.0/html/dc/d6d/classpyclustering_1_1cluster_1_1cure_1_1cure.html)

---

### 4. ROCK из библиотеки pyclustering

**Установка:**
```bash
python -m pip install pyclustering
```
**Импорт:**
```python
from pyclustering.cluster.rock import rock
```

**Описание метода:**
Метод ROCK (Robust Clustering using Links) используется для кластеризации категориальных данных и основан на количестве "связей" между точками.

**Сигнатура:**
```python
rock(data, eps, number_clusters=3, threshold=0.5, ccore=True)
```

**Параметры:**
- **data** (*list*): Входные данные, представленные в виде списка точек, где каждая точка - это список координат.

- **eps** (*float*): Радиус связности. Точки являются соседними, если расстояние между ними меньше заданного радиуса.

- **number_clusters** (*int*, по умолчанию 3): Количество кластеров, которые должны быть выделены.

- **threshold** (*float*, по умолчанию 0.5): Порог нормализации, влияющий на выбор кластеров для объединения.

- **ccore** (*bool*, по умолчанию True): Определяет, должен ли CCORE (библиотека C ++ для пикластеринга) использоваться вместо кода Python или нет.


**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.8.2/html/d8/dde/classpyclustering_1_1cluster_1_1rock_1_1rock.html)

---


### 5. DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import DBSCAN
```

**Описание метода:**
DBSCAN (Density-Based Spatial Clustering of Applications with Noise) — это алгоритм кластеризации, основанный на плотности, который выделяет кластеры по плотности точек и позволяет эффективно работать с шумовыми данными.

**Сигнатура:**
```python
class sklearn.cluster.DBSCAN(
    eps=0.5, min_samples=5, metric='euclidean',
    algorithm='auto', leaf_size=30, p=2, n_jobs=None
)
```

**Параметры:**
- **eps** (*float*, по умолчанию 0.5): Максимальное расстояние между точками, чтобы считать их соседями.
- **min_samples** (*int*, по умолчанию 5): Минимальное число точек для формирования плотного кластера.
- **metric** (*str*, по умолчанию 'euclidean'): Метрика расстояния между точками.
- **algorithm** (*str*, по умолчанию 'auto'): Алгоритм расчета: 'auto', 'ball_tree', 'kd_tree', 'brute'.
- **leaf_size** (*int*, по умолчанию 30): Параметр для оптимизации скорости деревьев.
- **p** (*float*, по умолчанию 2): Степень метрики Minkowski.
- **n_jobs** (*int*, по умолчанию None): Число потоков (-1 для использования всех доступных).

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)

---

### 6. HDBSCAN (Hierarchical DBSCAN)

**Установка:**
```bash
python -m pip install hdbscan
```
**Импорт:**
```python
from hdbscan import HDBSCAN
```

**Описание метода:**
HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) расширяет DBSCAN для работы с иерархическими структурами кластеров и автоматического определения количества кластеров.

**Сигнатура:**
```python
class hdbscan.HDBSCAN(
    min_cluster_size=5, metric='euclidean', cluster_selection_method='eom'
)
```

**Параметры:**
- **min_cluster_size** (*int*, по умолчанию 5): Минимальное количество точек в кластере.
- **metric** (*str*, по умолчанию 'euclidean'): Метрика для расчета расстояний.
- **cluster_selection_method** (*str*, по умолчанию 'eom'): Метод выбора кластеров ('eom' или 'leaf').

**Источник:** [Документация HDBSCAN](https://hdbscan.readthedocs.io/en/latest/)

---

### 7. GMM (Gaussian Mixture Model)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.mixture import GaussianMixture
```

**Описание метода:**
GMM (Gaussian Mixture Model) использует подходы вероятностного моделирования для определения кластеров, предполагая, что данные распределены как смесь нескольких гауссианов.

**Сигнатура:**
```python
class sklearn.mixture.GaussianMixture(
    n_components=1, covariance_type='full', tol=0.001, max_iter=100
)
```

**Параметры:**
- **n_components** (*int*, по умолчанию 1): Количество гауссианов.
- **covariance_type** (*str*, по умолчанию 'full'): Тип ковариации ('full', 'tied', 'diag', 'spherical').
- **tol** (*float*, по умолчанию 0.001): Порог для завершения итераций.
- **max_iter** (*int*, по умолчанию 100): Максимальное количество итераций.

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html)

---

### 8. OPTICS (Ordering Points To Identify the Clustering Structure)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import OPTICS
```

**Описание метода:**
OPTICS — это алгоритм кластеризации, который упорядочивает точки так, чтобы можно было определить иерархические кластеры.

**Сигнатура:**
```python
class sklearn.cluster.OPTICS(
    min_samples=5, max_eps=np.inf, metric='minkowski',
    p=2, cluster_method='xi', eps=np.inf
)
```

**Параметры:**
- **min_samples** (*int*, по умолчанию 5): Минимальное число точек в кластере.
- **max_eps** (*float*, по умолчанию np.inf): Максимальное расстояние для кластеризации.
- **metric** (*str*, по умолчанию 'minkowski'): Метрика для расчета расстояния.
- **p** (*float*, по умолчанию 2): Степень метрики Minkowski.
- **cluster_method** (*str*, по умолчанию 'xi'): Метод кластеризации ('xi' или 'dbscan').
- **eps** (*float*, по умолчанию np.inf): Максимальное расстояние между точками для включения в кластер.

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html)

---

### 9. Spectral Biclustering

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import SpectralBiclustering
```

**Описание метода:**
Spectral Biclustering — это метод, который находит кластеры как по строкам, так и по столбцам матрицы, выделяя скрытые структуры данных.

**Сигнатура:**
```python
class sklearn.cluster.SpectralBiclustering(
    n_clusters=3, method='bistochastic', n_components=6
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 3): Количество кластеров.
- **method** (*str*, по умолчанию 'bistochastic'): Метод обработки ('bistochastic', 'scale', 'log').
- **n_components** (*int*, по умолчанию 6): Количество компонент для анализа.

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralBiclustering.html)

---

### 10. BANG (Bounding And Nesting Grid)

**Установка:**
```bash
python -m pip install pyclustering
```
**Импорт:**
```python
from pyclustering.cluster.bang import bang
```

**Описание метода:**
BANG использует иерархическую сеточную структуру для быстрого поиска и выделения кластеров в многомерных данных.

**Сигнатура:**
```python
bang(data, levels=15)
```

**Параметры:**
- **data** (*list*): Входные данные, представленные в виде списка точек.
- **levels** (*int*, по умолчанию 15): Глубина иерархии сетки.

**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/da/d85/classpyclustering_1_1cluster_1_1bang_1_1bang.html)

---

### 11. Fuzzy C-means

**Установка:**
```bash
python -m pip install scikit-fuzzy
```
**Импорт:**
```python
from skfuzzy.cluster import cmeans
```

**Описание метода:**
Метод нечёткой кластеризации C-средних позволяет разбить имеющееся множество элементов мощностью *N* на заданное число нечётких множеств *k*.

**Сигнатура:**
```python
cmeans(data, 
        c=2,
        m=2.0,
        error=0.005,
        maxiter=1000)
```

**Параметры:**
- **data** (*list*): Входные данные, представленные в виде списка точек.
- **c** (*int*, по умолчанию 2): Желаемое количество кластеров.
- **m**(*float*, по умолчанию 2.0): Фактор фаззификации.
- **error**(*float*, по умолчанию 0.005): Критерий остановки; остановка досрочная, если норма (u[p] - u[p-1]) < ошибка.
- **maxiter**(*int*, по умолчанию 1000): Максимальное разрешенное количество итераций.

**Источник:** [Документация scikit-fuzzy](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.cluster.html#cmeans)


---

### 12. Spectral Clustering

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import SpectralClustering
```

**Описание метода:**
Spectral Сlustering —  это метод кластеризации, который использует методы спектральной теории графов для выделения кластеров в данных. 

**Сигнатура:**
```python
class sklearn.cluster.SpectralСlustering(
   n_clusters=3, affinity='rbf', gamma=1.0, n_neighbors=10, eigen_solver=None, random_state=0
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 3): Количество кластеров.
- **affinity** (*str*, по умолчанию 'rbf'): Функция сходства ('rbf', 'nearest_neighbors', 'precomputed', 'precomputed_nearest_neighbors').
- **gamma** (*float*, по умолчанию 1.0): Параметр gamma для ядра RBF. Используется, если affinity='rbf'.
- **n_neighbors** (*int*, по умолчанию 10): Количество соседей для affinity='nearest_neighbors'.
- **eigen_solver** (*str*, по умолчанию None): Решатель собственных значений ('None','arpack', 'lobpcg', 'amg').
- **random_state** (*int*, по умолчанию 0): Инициализация генератора случайных чисел..

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html)

---

### 13. WaveClustering (Кластеризация на основе вейвлет-преобразования)

**Установка:**
```bash
python -m pip install PyWavelets scipy
```
**Импорт:**
```python
from ClusteringMethods.WaveClusteringAlgorithm import WaveClustering
```

**Описание метода:**
WaveClustering использует вейвлет-преобразование для анализа пространства признаков на разных масштабах. Алгоритм квантует данные в сетку, применяет вейвлет-преобразование для выделения плотных областей на различных уровнях разрешения, а затем находит связные компоненты в преобразованном пространстве. Это позволяет обнаруживать кластеры различного размера и формы, используя многомасштабный анализ.

**Сигнатура:**
```python
class WaveClustering(
    n_grid=32, wavelet='haar', n_levels=2, density_threshold=0.1
)
```

**Параметры:**
- **n_grid** (*int*, по умолчанию 32): Количество делений каждого измерения на ячейки сетки. Большие значения дают более детальное разбиение, но требуют больше памяти.

- **wavelet** (*str*, по умолчанию 'haar'): Тип вейвлет-функции для преобразования. Доступные варианты: 'haar' (самый простой и быстрый), 'db2', 'db4', 'db6' (Добеши различных порядков), 'coif1' (Койфлет 1-го порядка).

- **n_levels** (*int*, по умолчанию 2): Количество уровней вейвлет-разложения (масштабы кластеров). Большие значения дают более крупные кластеры.

- **density_threshold** (*float*, по умолчанию 0.1): Порог для определения плотных областей (доля от максимальной плотности). Значения от 0 до 1. Меньшие значения дают больше кластеров.

**Источник:** `ClusteringMethods/WaveClusteringAlgorithm.py`

---

### 14. BallTree Hierarchical Clustering (Иерархическая кластеризация с использованием BallTree)

**Установка:**
```bash
python -m pip install scikit-learn scipy
```
**Импорт:**
```python
from ClusteringMethods.BallTreeClustering import BallTreeClustering
```

**Описание метода:**
Метод объединяет структуру данных BallTree с иерархической кластеризацией на основе матрицы попарных расстояний. Алгоритм вычисляет полную матрицу расстояний между всеми точками, строит иерархическое дерево кластеров с использованием методов linkage (ward, complete, average, single), а затем разрезает дерево на заданное количество кластеров. Нормализация данных является критически важной для корректной работы алгоритма.

**Сигнатура:**
```python
class BallTreeClustering(
    n_neighbors=5, leaf_size=40, metric='euclidean',
    linkage_method='ward', n_clusters=4, normalize=True
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 4): Желаемое количество кластеров. В отличие от DBSCAN, здесь обязательно указывать количество.

- **linkage_method** (*str*, по умолчанию 'ward'): Метод объединения кластеров в иерархии. Доступные варианты: 'ward' (минимизирует дисперсию, рекомендуется), 'complete' (максимальное расстояние), 'average' (среднее расстояние), 'single' (минимальное расстояние).

- **metric** (*str*, по умолчанию 'euclidean'): Метрика для расчета расстояния. Доступные варианты: 'euclidean' (евклидово, рекомендуется), 'manhattan' (манхэттенское), 'chebyshev' (максимальная норма).

- **n_neighbors** (*int*, по умолчанию 5): Зарезервировано для совместимости. В текущей версии не используется (используется полная матрица расстояний).

- **leaf_size** (*int*, по умолчанию 40): Зарезервировано для совместимости. В текущей версии не используется.

- **normalize** (*bool*, по умолчанию True): Нормализировать данные перед кластеризацией. Критически важно для корректной работы алгоритма.

**Источник:** `ClusteringMethods/BallTreeClustering.py`

---

### 15. HPStream (Проекционная кластеризация потоковых данных)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from ClusteringMethods.HPStreamClasteringAlgorithm import HPStreamClustering
```

**Описание метода:**
HPStream (High-dimensional Projected Stream clustering) предназначен для кластеризации высокомерных потоковых данных. Алгоритм автоматически определяет значимые размерности для каждого кластера, используя адаптивные веса признаков, и выполняет кластеризацию только в подпространствах релевантных признаков. Метод поддерживает инкрементальное обучение на новых батчах данных с использованием скользящего окна, что делает его пригодным для потоковой обработки.

**Сигнатура:**
```python
class HPStreamClustering(
    num_clusters=5, projection_threshold=0.1,
    window_size=1000, fade_threshold=0.1, normalize=True
)
```

**Параметры:**
- **num_clusters** (*int*, по умолчанию 5): Желаемое количество кластеров.

- **projection_threshold** (*float*, по умолчанию 0.1): Порог для определения значимых размерностей. Размерности с весом выше этого порога считаются значимыми для кластеризации.

- **window_size** (*int*, по умолчанию 1000): Размер окна для потоковых данных. Определяет количество последних точек, которые учитываются при обновлении модели.

- **fade_threshold** (*float*, по умолчанию 0.1): Коэффициент затухания весов размерностей. Контролирует скорость адаптации весов к новым данным.

- **max_iterations** (*int*, по умолчанию 100): Максимальное количество итераций алгоритма кластеризации.

- **normalize** (*bool*, по умолчанию True): Нормализировать входные данные перед кластеризацией.

**Источник:** `ClusteringMethods/HPStreamClasteringAlgorithm.py`

---

### 16. KMeans (KMeans с опциональной PCA декомпозицией)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
```

**Описание метода:**
Реализация классического алгоритма KMeans из библиотеки scikit-learn с дополнительной возможностью применения PCA (Principal Component Analysis) для снижения размерности данных перед кластеризацией. Алгоритм итеративно обновляет центроиды кластеров, минимизируя сумму квадратов расстояний от точек до ближайших центров. PCA позволяет работать с данными высокой размерности, сохраняя основную вариативность данных.

**Сигнатура:**
```python
class sklearn.cluster.KMeans(
    n_clusters=3, init='k-means++', n_init=10, max_iter=300,
    random_state=42
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 3): Желаемое количество кластеров для KMeans. Примеры: 2, 3, 4, 5...

- **init** (*str*, по умолчанию 'k-means++'): Метод инициализации центроидов. Доступные варианты: 'k-means++' (умная инициализация, рекомендуется), 'random' (случайная инициализация).

- **n_init** (*int*, по умолчанию 10): Количество различных инициализаций для выбора лучшего результата. Больше значений = лучше результат, но медленнее. Рекомендуется: 10-20.

- **max_iter** (*int*, по умолчанию 300): Максимальное количество итераций алгоритма KMeans. Рекомендуется: 300-500.

- **random_state** (*int*, по умолчанию 42): Инициализация генератора случайных чисел для воспроизводимости результатов.

- **use_pca** (*bool*, по умолчанию True): Включить/выключить PCA декомпозицию перед кластеризацией. Если False, используется только стандартизация данных.

- **n_components** (*int*, по умолчанию 0): Количество главных компонент для PCA декомпозиции. Если 0, используется автоматический выбор (min(n_samples, n_features)). Рекомендуется: 2-3 для визуализации, больше для сохранения информации.

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) и `ClusteringMethods/KMeansClustering.py`

---

### 17. MiniBatchKMeans (Мини-батч версия KMeans)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
```

**Описание метода:**
MiniBatchKMeans является оптимизированной версией KMeans, которая обрабатывает данные небольшими батчами вместо использования всего набора данных на каждой итерации. Это значительно ускоряет обучение, особенно на больших наборах данных, при сохранении приемлемого качества кластеризации. Алгоритм обновляет центроиды на основе мини-батчей, что делает его пригодным для потоковой обработки и работы с данными, которые не помещаются в память.

**Сигнатура:**
```python
class sklearn.cluster.MiniBatchKMeans(
    n_clusters=3, init='k-means++', max_iter=100, batch_size=100,
    verbose=False, compute_labels=True, random_state=42, reassignment_ratio=0.01
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 3): Желаемое количество кластеров для MiniBatchKMeans. Примеры: 2, 3, 4, 5...

- **init** (*str*, по умолчанию 'k-means++'): Метод инициализации центроидов. Доступные варианты: 'k-means++' (умная инициализация, рекомендуется), 'random' (случайная инициализация).

- **max_iter** (*int*, по умолчанию 100): Максимальное количество итераций алгоритма MiniBatchKMeans. Рекомендуется: 100-300.

- **batch_size** (*int*, по умолчанию 100): Размер мини-батча для обработки данных. Большие значения дают более точные результаты, но медленнее. Рекомендуется: 100-1000.

- **verbose** (*bool*, по умолчанию False): Включить/выключить подробный вывод процесса кластеризации.

- **compute_labels** (*bool*, по умолчанию True): Вычислять метки для всех точек после обучения. Если False, метки будут вычисляться только при необходимости.

- **random_state** (*int*, по умолчанию 42): Инициализация генератора случайных чисел для воспроизводимости результатов.

- **reassignment_ratio** (*float*, по умолчанию 0.01): Коэффициент перераспределения центроидов. Контролирует частоту перераспределения центров кластеров. Рекомендуется: 0.01-0.1.

- **use_pca** (*bool*, по умолчанию True): Включить/выключить PCA декомпозицию перед кластеризацией. Если False, используется только стандартизация данных.

- **n_components** (*int*, по умолчанию 0): Количество главных компонент для PCA декомпозиции. Если 0, используется автоматический выбор (min(n_samples, n_features)). Рекомендуется: 2-3 для визуализации, больше для сохранения информации.

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html) и `ClusteringMethods/MiniBatchKMeansClustering.py`

---

### 18. VP-Tree Bregman Divergence Clustering (Кластеризация на основе VP-tree с дивергенциями)

**Установка:**
```bash
python -m pip install scikit-learn scipy
```
**Импорт:**
```python
from ClusteringMethods.VPTreeClustering import VPTreeBregmanClustering
```

**Описание метода:**
Метод объединяет концепцию VP-tree (Vantage Point Tree) с иерархической кластеризацией, используя различные типы дивергенций и метрик расстояния для вычисления матрицы попарных расстояний. Алгоритм поддерживает евклидову дивергенцию, дивергенции Хеллингера и Бхаттачарьи (полезны для вероятностных данных), а также метрики Манхэттена, Чебышёва и косинусное расстояние. На основе вычисленной матрицы строится иерархическое дерево кластеров.

**Сигнатура:**
```python
class VPTreeBregmanClustering(
    divergence='euclidean', linkage_method='ward', n_clusters=4,
    normalize=True, max_depth=10
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 4): Желаемое количество кластеров для разбиения. Примеры: 2, 3, 4, 5...

- **divergence** (*str*, по умолчанию 'euclidean'): Выбор метрики/дивергенции для измерения расстояния. Доступные варианты: 'euclidean' (евклидова дивергенция, рекомендуется), 'hellinger' (дивергенция Хеллингера для вероятностей), 'bhattacharyya' (дивергенция Бхаттачарьи, статистическое расстояние), 'manhattan' (манхэттенское расстояние), 'chebyshev' (максимальная норма), 'cosine' (косинусное расстояние).

- **linkage_method** (*str*, по умолчанию 'ward'): Метод для связывания кластеров в иерархии. Доступные варианты: 'ward' (минимизирует дисперсию, рекомендуется), 'complete' (максимальное расстояние между кластерами), 'average' (среднее расстояние между кластерами), 'single' (минимальное расстояние между кластерами).

- **normalize** (*bool*, по умолчанию True): Нормализировать входные данные перед кластеризацией.

- **max_depth** (*int*, по умолчанию 10): Максимальная глубина дерева VP-tree. Зарезервировано для будущих версий.

**Источник:** `ClusteringMethods/VPTreeClustering.py`

---

### 19. Agglomerative Clustering (Иерархическая агломеративная кластеризация)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import AgglomerativeClustering
from ClusteringMethods.AgglomerativeClustering import ConcreteStrategyAgglomerative_from_SKLEARN
```

**Описание метода:**
Agglomerative Clustering — иерархический алгоритм снизу вверх: каждая точка начинается как отдельный кластер, после чего ближайшие кластеры последовательно объединяются. Способ слияния задаётся параметром linkage (ward, complete, average, single). Число кластеров можно задать явно через `n_clusters` либо определить автоматически по порогу расстояния `distance_threshold`. Метод linkage `ward` работает только с евклидовой метрикой; при другом выборе метрика автоматически заменяется на `euclidean`. Для изображений выполняется выборка пикселей, а оставшиеся точки получают метки по ближайшему центроиду.

**Сигнатура:**
```python
class sklearn.cluster.AgglomerativeClustering(
    n_clusters=2, metric='euclidean', linkage='ward',
    compute_full_tree='auto', distance_threshold=None, compute_distances=False
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 3): Желаемое количество кластеров. Игнорируется, если `distance_threshold` больше 0.

- **linkage** (*str*, по умолчанию 'ward'): Метод объединения кластеров. Доступные варианты: 'ward' (минимизирует дисперсию, рекомендуется), 'complete' (максимальное расстояние), 'average' (среднее расстояние), 'single' (минимальное расстояние).

- **metric** (*str*, по умолчанию 'euclidean'): Метрика расстояния. Доступные варианты: 'euclidean', 'manhattan', 'cosine', 'l1', 'l2', 'chebyshev'. Для `linkage='ward'` используется только 'euclidean'.

- **compute_full_tree** (*str*, по умолчанию 'auto'): Строить ли полное дерево слияния. Доступные варианты: 'auto', 'true', 'false'. При использовании `distance_threshold` всегда строится полное дерево.

- **distance_threshold** (*float*, по умолчанию 0.0): Порог расстояния для остановки слияния. Значение 0 означает, что используется `n_clusters`. Если значение больше 0, число кластеров определяется автоматически.

- **compute_distances** (*bool*, по умолчанию False): Вычислять расстояния между узлами дерева слияния. На метки кластеров не влияет.

- **normalize** (*bool*, по умолчанию True): Стандартизировать признаки перед кластеризацией.

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html) и `ClusteringMethods/AgglomerativeClustering.py`

---

### 20. MeanShift (Кластеризация методом сдвига среднего)

**Установка:**
```bash
python -m pip install scikit-learn
```
**Импорт:**
```python
from sklearn.cluster import MeanShift, estimate_bandwidth
from ClusteringMethods.MeanShiftClustering import ConcreteStrategyMeanShift_from_SKLEARN
```

**Описание метода:**
MeanShift — алгоритм, основанный на плотности: вокруг каждой точки строится окно радиуса `bandwidth`, и точка многократно сдвигается в среднее (центр масс) точек, попавших в окно. В результате все точки «сползают» к локальным максимумам плотности данных (модам). Точки, сошедшиеся в одну моду, образуют один кластер, поэтому число кластеров определяется автоматически. Если `bandwidth` равен 0, радиус оценивается функцией `estimate_bandwidth` по параметру `quantile`. Метод хорошо находит кластеры «округлой» формы, но плохо справляется с вложенными и вытянутыми структурами (moons, circles). Для изображений модель обучается на выборке пикселей, а остальные пиксели получают метку ближайшего найденного центра.

**Сигнатура:**
```python
class sklearn.cluster.MeanShift(
    bandwidth=None, seeds=None, bin_seeding=False,
    min_bin_freq=1, cluster_all=True, n_jobs=None, max_iter=300
)
```

**Параметры:**
- **bandwidth** (*float*, по умолчанию 0.0): Радиус окна. Меньше радиус — больше мелких кластеров. Значение 0 означает автоматическую оценку по `quantile`.

- **quantile** (*float*, по умолчанию 0.2): Квантиль попарных расстояний для автоматической оценки `bandwidth` (от 0 до 1). Рекомендуется 0.1–0.3.

- **bin_seeding** (*bool*, по умолчанию False): Запускать сдвиги из узлов сетки, а не из каждой точки. Ускоряет работу на больших данных.

- **min_bin_freq** (*int*, по умолчанию 1): Минимальное число точек в ячейке сетки, чтобы она стала стартовой. Используется только при `bin_seeding=True`.

- **cluster_all** (*bool*, по умолчанию True): Если False, точки вне всех окон получают метку -1 (шум).

- **max_iter** (*int*, по умолчанию 300): Максимальное число сдвигов для одной стартовой точки.

- **normalize** (*bool*, по умолчанию True): Стандартизировать признаки перед кластеризацией.

**Источник:** [Документация scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MeanShift.html) и `ClusteringMethods/MeanShiftClustering.py`

---

### 21. K-Medians (Кластеризация по медианам)

**Установка:**
```bash
python -m pip install pyclustering scikit-learn
```
**Импорт:**
```python
from pyclustering.cluster.kmedians import kmedians
from ClusteringMethods.KMediansClustering import ConcreteStrategyKMedians_from_PYCLUSTERING
```

**Описание метода:**
K-Medians — вариант KMeans, в котором центр кластера вычисляется не как среднее, а как медиана по каждой координате. Алгоритм по очереди повторяет два шага: относит каждую точку к ближайшему центру и пересчитывает центры как медианы точек кластера, пока центры не перестанут сдвигаться (параметр `tolerance`). Медиана не смещается под влиянием отдельных далёких точек, поэтому метод устойчивее к выбросам, чем KMeans. Медиана минимизирует сумму манхэттенских расстояний, поэтому метрикой по умолчанию выбрана `manhattan`. Начальные центры выбираются через `sklearn.cluster.kmeans_plusplus`, так как инициализатор pyclustering несовместим с numpy >= 2. Если C++ часть pyclustering недоступна на платформе (например, macOS arm64), автоматически используется реализация на Python.

**Сигнатура:**
```python
class pyclustering.cluster.kmedians.kmedians(
    data, initial_medians, tolerance=0.001, ccore=True, metric=None, itermax=200
)
```

**Параметры:**
- **n_clusters** (*int*, по умолчанию 3): Количество кластеров.

- **init** (*str*, по умолчанию 'k-means++'): Способ выбора начальных центров: 'k-means++' (центры далеко друг от друга) или 'random' (случайные точки выборки).

- **metric** (*str*, по умолчанию 'manhattan'): Метрика расстояния. Доступные варианты: 'manhattan', 'euclidean', 'euclidean_square', 'chebyshev'.

- **tolerance** (*float*, по умолчанию 0.001): Алгоритм останавливается, когда максимальный сдвиг центров меньше этого значения.

- **itermax** (*int*, по умолчанию 200): Максимальное число итераций.

- **random_state** (*int*, по умолчанию 42): Инициализация генератора случайных чисел.

- **normalize** (*bool*, по умолчанию True): Стандартизировать признаки перед кластеризацией.

- **ccore** (*bool*, по умолчанию True): Использовать C++ часть pyclustering. При ошибке загрузки используется Python-реализация.

**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/d0/d7a/classpyclustering_1_1cluster_1_1kmedians_1_1kmedians.html) и `ClusteringMethods/KMediansClustering.py`

---

### 22. X-Means (KMeans с автоматическим подбором числа кластеров)

**Установка:**
```bash
python -m pip install pyclustering scikit-learn
```
**Импорт:**
```python
from pyclustering.cluster.xmeans import xmeans, splitting_type
from ClusteringMethods.XMeansClustering import ConcreteStrategyXMeans_from_PYCLUSTERING
```

**Описание метода:**
X-Means — расширение KMeans, которое само определяет число кластеров. Алгоритм начинает с `kmin` центров и повторяет два шага: запускает обычный KMeans, затем пробует разделить каждый кластер на два. Разделение сохраняется, только если оно улучшает критерий качества (BIC или MNDL): два кластера должны описывать данные заметно лучше одного с учётом «штрафа» за лишние параметры модели. Поиск останавливается, когда ни одно разделение не улучшает критерий или число кластеров достигло `kmax`. Критерии рассчитаны на круглые (сферические) кластеры одинакового разброса, поэтому вытянутые кластеры алгоритм дробит на части. По этой причине нормализация по умолчанию выключена: стандартизация сжимает оси по-разному и может сделать круглые кластеры вытянутыми. На фотографиях цвета распределены непрерывно, поэтому алгоритм обычно доходит до `kmax` — число цветовых групп стоит ограничивать этим параметром. Для совместимости pyclustering с numpy >= 2 атрибут `numpy.warnings` подменяется стандартным модулем `warnings`. Если C++ часть pyclustering недоступна на платформе (например, macOS arm64), автоматически используется реализация на Python.

**Сигнатура:**
```python
class pyclustering.cluster.xmeans.xmeans(
    data, initial_centers=None, kmax=20, tolerance=0.001,
    criterion=splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore=True,
    repeat=1, random_state=None
)
```

**Параметры:**
- **kmin** (*int*, по умолчанию 2): Начальное количество кластеров, с которого начинается поиск.

- **kmax** (*int*, по умолчанию 20): Максимальное количество кластеров.

- **criterion** (*str*, по умолчанию 'bic'): Критерий разделения: 'bic' (байесовский информационный критерий, рекомендуется) или 'mndl' (минимальная длина описания без шума, обычно находит меньше кластеров).

- **tolerance** (*float*, по умолчанию 0.001): Точность остановки внутреннего KMeans.

- **repeat** (*int*, по умолчанию 1): Сколько раз запускать KMeans при попытке разделить кластер.

- **random_state** (*int*, по умолчанию 42): Инициализация генератора случайных чисел.

- **normalize** (*bool*, по умолчанию False): Стандартизировать признаки перед кластеризацией. Включайте только для признаков разного масштаба.

- **ccore** (*bool*, по умолчанию True): Использовать C++ часть pyclustering. При ошибке загрузки используется Python-реализация.

**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/dd/db4/classpyclustering_1_1cluster_1_1xmeans_1_1xmeans.html) и `ClusteringMethods/XMeansClustering.py`

---

### 23. MBSAS (Модифицированный базовый последовательный алгоритм)

**Установка:**
```bash
python -m pip install pyclustering scikit-learn
```
**Импорт:**
```python
from pyclustering.cluster.mbsas import mbsas
from ClusteringMethods.MBSASClustering import ConcreteStrategyMBSAS_from_PYCLUSTERING
```

**Описание метода:**
MBSAS (Modified Basic Sequential Algorithmic Scheme) — последовательный алгоритм, который проходит по данным дважды. На первом проходе точки просматриваются по порядку: если расстояние от точки до ближайшего кластера больше порога `threshold` и лимит `maximum_clusters` не исчерпан, точка открывает новый кластер, остальные точки пропускаются. На втором проходе каждая пропущенная точка относится к ближайшему кластеру, а представитель кластера (среднее его точек) пересчитывается. Число кластеров определяется порогом. Результат зависит от порядка точек: кластеры открывают точки, встретившиеся раньше. Параметр `shuffle` позволяет перемешать точки перед обработкой. Порог измеряется в единицах расстояния, поэтому по умолчанию данные стандартизируются и порог задаётся в стандартных отклонениях. Если C++ часть pyclustering недоступна на платформе (например, macOS arm64), автоматически используется реализация на Python.

**Сигнатура:**
```python
class pyclustering.cluster.mbsas.mbsas(
    data, maximum_clusters, threshold, ccore=True, metric=distance_metric(type_metric.EUCLIDEAN)
)
```

**Параметры:**
- **maximum_clusters** (*int*, по умолчанию 10): Максимальное количество кластеров.

- **threshold** (*float*, по умолчанию 1.0): Порог расстояния: точка дальше порога от всех кластеров открывает новый кластер. Меньше порог — больше кластеров. Рекомендуется 0.5–1.5.

- **metric** (*str*, по умолчанию 'euclidean'): Метрика расстояния: 'euclidean', 'manhattan', 'chebyshev'.

- **shuffle** (*bool*, по умолчанию False): Перемешать точки перед обработкой.

- **random_state** (*int*, по умолчанию 42): Инициализация генератора случайных чисел для перемешивания.

- **normalize** (*bool*, по умолчанию True): Стандартизировать признаки перед кластеризацией.

- **ccore** (*bool*, по умолчанию True): Использовать C++ часть pyclustering. При ошибке загрузки используется Python-реализация.

**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/d4/d02/classpyclustering_1_1cluster_1_1mbsas_1_1mbsas.html) и `ClusteringMethods/MBSASClustering.py`

---

### 24. SOM (Самоорганизующаяся карта Кохонена)

**Установка:**
```bash
python -m pip install pyclustering scikit-learn
```
**Импорт:**
```python
from pyclustering.nnet.som import som, som_parameters, type_conn, type_init
from ClusteringMethods.SOMClustering import ConcreteStrategySOM_from_PYCLUSTERING
```

**Описание метода:**
SOM (Self-Organizing Map) — нейронная сеть из нейронов, расположенных в узлах сетки `rows` x `cols`. У каждого нейрона есть вектор весов — точка в пространстве данных. При обучении для каждой точки находится нейрон-победитель с ближайшими весами, и веса победителя и его соседей по сетке сдвигаются в сторону точки; сила сдвига и радиус соседства уменьшаются с каждой эпохой. После обучения каждая точка относится к своему нейрону-победителю: один нейрон — один кластер. Число кластеров не превышает `rows * cols`; нейроны, не выигравшие ни одной точки («мёртвые» нейроны), в результат не попадают. Для обычной кластеризации удобно задавать `rows = 1`, а число кластеров — через `cols`. Для изображений сеть обучается на выборке пикселей, а все пиксели относятся к ближайшему нейрону. Если C++ часть pyclustering недоступна на платформе (например, macOS arm64), автоматически используется реализация на Python.

**Сигнатура:**
```python
class pyclustering.nnet.som.som(
    rows, cols, conn_type=type_conn.grid_eight, parameters=None, ccore=True
)
```

**Параметры:**
- **rows** (*int*, по умолчанию 1): Число строк сетки нейронов.

- **cols** (*int*, по умолчанию 3): Число столбцов сетки нейронов. Максимальное число кластеров равно `rows * cols`.

- **conn_type** (*str*, по умолчанию 'grid_eight'): Какие нейроны считаются соседями: 'grid_eight' (8 соседей), 'grid_four' (4 соседа), 'honeycomb' (6 соседей), 'func_neighbor' (по функции расстояния).

- **init_type** (*str*, по умолчанию 'uniform_grid'): Начальное расположение весов: 'uniform_grid', 'random', 'random_centroid', 'random_surface'.

- **epochs** (*int*, по умолчанию 100): Количество эпох обучения.

- **learn_rate** (*float*, по умолчанию 0.1): Начальная скорость обучения.

- **random_state** (*int*, по умолчанию 42): Инициализация генератора случайных чисел.

- **normalize** (*bool*, по умолчанию True): Стандартизировать признаки перед кластеризацией.

- **ccore** (*bool*, по умолчанию True): Использовать C++ часть pyclustering. При ошибке загрузки используется Python-реализация.

**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/d7/d2c/classpyclustering_1_1nnet_1_1som_1_1som.html) и `ClusteringMethods/SOMClustering.py`

---

### 25. CLIQUE (Кластеризация на основе сетки)

**Установка:**
```bash
python -m pip install pyclustering numpy
```
**Импорт:**
```python
from pyclustering.cluster.clique import clique
from ClusteringMethods.CliqueClustering import ConcreteStrategyCLIQUE
```

**Описание метода:**
CLIQUE (CLustering In QUEst) — density-based grid-алгоритм кластеризации. Пространство данных разбивается на grid-ячейки по каждому измерению: каждое измерение делится на `amount_intervals` интервалов, образуя сетку. Для каждой ячейки подсчитывается количество точек. Ячейки, содержащие не менее `density_threshold` точек, считаются плотными; точки в разреженных ячейках помечаются как шум (метка -1). Смежные плотные ячейки (имеющие общую грань) объединяются в кластеры. Алгоритм не вычисляет расстояния между точками — только распределяет точки по ячейкам за один проход, что делает его самым быстрым density-based методом в системе (сложность O(n)). Хорошо работает на сферических кластерах (blobs), но плохо — на изогнутых формах (moons, circles), так как сетка разрезает их на прямоугольные фрагменты.

**Сигнатура:**
```python
class pyclustering.cluster.clique.clique(
    data, amount_intervals, density_threshold, **kwargs
)
```

**Параметры:**
- **amount_intervals** (*int*, по умолчанию 5): Количество интервалов в каждом измерении. Определяет granularity сетки: больше интервалов — мельче сетка, больше кластеров и больше шума.

- **density_threshold** (*int*, по умолчанию 10): Минимальное количество точек в блоке сетки, чтобы точки не считались выбросами (шумом). Больше порог — больше точек помечаются как шум.

- **ccore** (*bool*, по умолчанию True): Использовать C++ часть библиотеки pyclustering для обработки. Автоматически отключается, если C++ ядро недоступно.

**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/d2/dcc/classpyclustering_1_1cluster_1_1clique_1_1clique.html) и `ClusteringMethods/CliqueClustering.py`

---

### 26. CLARANS (Кластеризация на основе случайного поиска)

**Установка:**
```bash
python -m pip install pyclustering numpy
```
**Импорт:**
```python
from pyclustering.cluster.clarans import clarans
from ClusteringMethods.ClaransClustering import ConcreteStrategyCLARANS
```

**Описание метода:**
CLARANS (Clustering Large Applications based on RANdomized Search) — алгоритм кластеризации на основе K-Medoids с randomized search. В отличие от K-Means, где центром кластера является вычисленный центроид (среднее арифметическое), CLARANS использует медоиды — реальные точки данных как центры кластеров. Это делает алгоритм устойчивым к выбросам: выброс не искажает медоид, так как медоид является фактической точкой из данных. Алгоритм случайно выбирает начальные медоиды, затем итеративно заменяет случайный медоид на случайную не-медоидную точку: если замена уменьшает общую стоимость (сумму расстояний от точек до их медоидов), она принимается. Процесс повторяется `numlocal` раз с разными начальными конфигурациями, каждый раз проверяя до `maxneighbor` соседей. Чем больше `numlocal` и `maxneighbor`, тем точнее результат, но тем медленнее работа. Сложность O(n²·k·numlocal·maxneighbor) — медленнее K-Means, но надёжнее при наличии шума и выбросов. Шум не выделяется (все точки относятся к какому-либо кластеру).

**Сигнатура:**
```python
class pyclustering.cluster.clarans.clarans(
    data, number_clusters, numlocal, maxneighbor
)
```

**Параметры:**
- **number_clusters** (*int*, по умолчанию 3): Количество кластеров (медоидов) для выделения. Алгоритм ищет указанное количество оптимальных медоидов.

- **numlocal** (*int*, по умолчанию 2): Количество локальных минимумов для поиска (amount of iterations for solving the problem). Больше значений — лучше результат, но медленнее. Рекомендуется: 2–4.

- **maxneighbor** (*int*, по умолчанию 5): Максимальное количество соседей для проверки за одну итерацию. Чем больше, тем ближе CLARANS к K-Medoids (точнее, но дольше каждый поиск локального минимума). Рекомендуется: 3–8. При значениях больше 10 на больших данных возможны длительные задержки.

**Источник:** [Документация pyclustering](https://pyclustering.github.io/docs/0.10.1/html/d6/d1f/classpyclustering_1_1cluster_1_1clarans_1_1clarans.html) и `ClusteringMethods/ClaransClustering.py`

---

---

### 27. DENCLUE (Кластеризация по гауссовской плотности)

**Установка:**
```bash
python -m pip install numpy scipy scikit-learn
```

**Импорт:**
```python
from ClusteringMethods.DENCLUEClustering import DENCLUE, ConcreteStrategyDENCLUE
```

**Описание метода:**
Собственная реализация DENCLUE на NumPy/SciPy: поиск аттракторов плотности,
объединение по плотностным мостам и выделение шума (`-1`). В pyclustering 0.10.1.2
DENCLUE отсутствует. ID стратегии: `denclue`.

**Сигнатура:**
```python
DENCLUE(sigma=0.5, xi=0.01, tolerance=0.0001, max_iter=200,
        merge_radius=0.5, min_cluster_size=1, normalize=False, batch_size=128)
```

**Параметры:**
- **sigma** (*float*, 0.5): положительная ширина гауссовского ядра.
- **xi** (*float*, 0.01): минимальное среднее гауссовское влияние, от 0 до 1;
  плотность считается без нормирующего множителя KDE.
- **tolerance** (*float*, 0.0001): положительный порог перемещения аттрактора.
- **max_iter** (*int*, 200): положительный лимит итераций; несошедшиеся точки — шум.
- **merge_radius** (*float*, 0.5): положительный радиус объединения аттракторов;
  плотность на соединяющем отрезке проверяется дискретно с шагом не более `sigma/2`.
- **min_cluster_size** (*int*, 1): минимальный размер кластера с учётом повторений.
- **normalize** (*bool*, False): StandardScaler перед кластеризацией.
- **batch_size** (*int*, 128): положительный размер блока расстояний для ограничения памяти.

**Пример:**
```python
labels = DENCLUE(sigma=0.5, xi=0.02).fit_predict(X)
```

Стоимость поиска аттракторов квадратична по числу различных точек. Начинайте с малых
выборок; для изображений учитывайте масштаб RGB или включайте нормализацию.

**Источники:** [Hinneburg, Keim, KDD 1998](https://s.aaai.org/Papers/KDD/1998/KDD98-009.pdf),
[описание реализации, ограничений и тестов](../Documentation/Programming%20documentation/DENCLUE%20и%20FCM.md).

---

### 28. FCM (Расширенный Fuzzy C-Means из pyclustering)

**Установка:**
```bash
python -m pip install pyclustering scikit-learn numpy
```

**Импорт:**
```python
from ClusteringMethods.FCMClustering import ConcreteStrategyFCM_from_PYCLUSTERING
```

**Описание метода:**
Отдельная стратегия `fcm_pyc` с выбором инициализации, воспроизводимым seed,
нормализацией и переключением CCORE/Python. Существующий `fuzzy_cmeans` из
scikit-fuzzy сохранён. Выход — жёсткие метки кластеров для общего GUI.

**Сигнатура базового алгоритма:**
```python
fcm(data, initial_centers, m=2.0, tolerance=0.001, itermax=200, ccore=True)
```

**Параметры стратегии:**
- **n_clusters** (*int*, 3): положительное число кластеров, не больше числа различных объектов.
- **m** (*float*, 2.0): фаззи-фактор, строго больше 1.
- **tolerance** (*float*, 0.001): положительный порог максимального квадрата смещения центров.
- **itermax** (*int*, 200): положительный лимит итераций.
- **init** (*str*, `kmeans++`): `kmeans++` или `random`.
- **random_state** (*int*, 42): seed начальных центров, от 0 до 4294967295.
- **normalize** (*bool*, False): стандартизировать признаки перед инициализацией.
- **ccore** (*bool*, True): использовать C++; при недоступности автоматически выбрать Python.

**Пример:**
```python
from ClusteringMethods.ClasteringAlgorithms import StrategiesManager
config = StrategiesManager.getStrategyRunConfigById("fcm_pyc")
config["n_clusters"] = 3
config["init"] = "random"
config["random_state"] = 42
labels = ConcreteStrategyFCM_from_PYCLUSTERING().clastering_points(X, config)
```

**Источники:** [Исходный код pyclustering FCM](https://github.com/annoviko/pyclustering/blob/master/pyclustering/cluster/fcm.py),
[параметры, примеры и проверки](../Documentation/Programming%20documentation/DENCLUE%20и%20FCM.md).
