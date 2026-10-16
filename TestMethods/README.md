# TestMethods - Директория для Тестирования Алгоритмов Кластеризации

## Содержание

- [Назначение](#назначение)
- [Структура Директории](#структура-директории)
- [Быстрый Старт](#быстрый-старт)
- [Создание Нового Теста](#создание-нового-теста)
- [Примеры Использования](#примеры-использования)
- [Рекомендации](#рекомендации)
- [FAQ](#faq)

---

## Назначение

Директория `TestMethods/` предназначена для **тестирования и валидации** алгоритмов кластеризации перед их интеграцией в основной GUI фреймворк.

### Основные Цели

 - **Проверка корректности** работы алгоритмов  
 - **Визуализация результатов** кластеризации  
 - **Сравнение параметров** и их влияния на результаты  
 - **Генерация документации** с примерами работы  
 - **Отладка** новых методов кластеризации  

---

## Структура Директории

```
DMM_ClusteringSystem/
├── TestMethods/                      # Корневая директория для тестов
│   ├── README.md                     # Этот файл - документация
│   ├── test_wave.py                  # Тест WaveClustering
│   ├── test_dbscan.py                # Тест DBSCAN
│   ├── test_spectral_biclustering.py # Тест Spectral Biclustering
│   ├── test_agglomerative.py         # Тест Agglomerative Clustering
│   ├── test_meanshift.py             # Тест MeanShift
│   ├── test_kmedians.py              # Тест K-Medians
│   ├── test_xmeans.py                # Тест X-Means
│   ├── test_mbsas.py                 # Тест MBSAS
│   ├── test_som.py                   # Тест SOM
│   ├── test_clique.py               # Тест CLIQUE
│   ├── test_clarans.py              # Тест CLARANS
│   ├── test_denclue.py               # Тест DENCLUE
│   ├── test_fcm_pyc.py               # Тест FCM (PyClustering)
│   ├── test_denclue_fcm_regression.py # Регрессионные тесты DENCLUE и FCM
│   ├── test_template.py              # Шаблон для новых тестов
│   │
│   └── Images/                       # Директория для результатов
│       ├── WaveClustering/           # Результаты WaveClustering
│       │   ├── test_basic_2d.png
│       │   ├── test_parameters.png
│       │   ├── test_datasets.png
│       │   ├── test_3d.png
│       │   └── test_strategy.png
│       │
│       ├── DBSCAN/                   # Результаты DBSCAN
│       │   ├── test_basic_2d.png
│       │   ├── test_parameters.png
│       │   ├── test_datasets.png
│       │   ├── test_3d.png
│       │   └── test_strategy.png
│       │
│       └── SpectralBiclustering/    # Результаты Spectral Biclustering
│           ├── test_basic_2d.png
│           ├── test_parameters.png
│           ├── test_datasets.png
│           ├── test_3d.png
│           └── test_strategy.png
```

### Описание Компонентов

| Файл/Папка | Назначение |
|------------|------------|
| `test_*.py` | Скрипты для тестирования конкретных алгоритмов |
| `test_template.py` | Шаблон для создания новых тестов |
| `Images/` | Хранение визуализаций результатов |
| `Images/{AlgorithmName}/` | Отдельная папка для каждого алгоритма |

---

## Быстрый Старт

### Шаг 1: Запуск Существующего Теста

```bash
# Перейдите в корневую директорию проекта
cd <path_to_your_project>\DMM_ClusteringSystem

# Запустите тест WaveClustering
python TestMethods/test_wave.py

# Тест DENCLUE
python TestMethods/test_denclue.py --no-show

# Тест FCM (PyClustering)
python TestMethods/test_fcm_pyc.py --no-show

# Регрессионные тесты DENCLUE и FCM
python -m unittest TestMethods.test_denclue_fcm_regression -v
```

Для `test_denclue.py` и `test_fcm_pyc.py` флаг `--no-show` отключает показ окон.
Пять стандартных PNG сохраняются в `Images/DENCLUE/` и `Images/FCM_PyClustering/`.

### Шаг 2: Просмотр Результатов

После выполнения теста:

1. **Консоль** покажет статистику:
   ```
   ================================================================================
   ТЕСТ 1: Базовая 2D Кластеризация
   ================================================================================
   Количество точек: 300
   Истинное количество кластеров: 3
   Найдено кластеров: 3
   ✅ Сохранено: test_basic_2d.png
   ```

2. **Графики** автоматически откроются в matplotlib

3. **Файлы PNG** сохранятся в `TestMethods/Images/WaveClustering/`

### Шаг 3: Анализ Результатов

Откройте созданные изображения:
- `test_basic_2d.png` - базовая 2D кластеризация (сравнение истинных и предсказанных кластеров)
- `test_parameters.png` - чувствительность к параметрам (4 варианта)
- `test_datasets.png` - тестирование на разных типах датасетов (blobs, moons, circles)
- `test_3d.png` - 3D кластеризация с проекциями
- `test_strategy.png` - тест интеграции с фреймворком через Strategy Pattern

---

## Создание Нового Теста

### Использование Шаблона (Рекомендуется)

Все тесты в проекте следуют единому стандарту. Используйте `test_template.py` как основу.

#### Шаг 1: Создайте Файл Теста

```bash
# Скопируйте шаблон
cp TestMethods/test_template.py TestMethods/test_your_algorithm.py
```

#### Шаг 2: Настройте Импорты

В файле `test_your_algorithm.py` замените:

```python
ALGORITHM_NAME = "YourAlgorithm"  # Имя вашего алгоритма

try:
    from ClusteringMethods.ClasteringAlgorithms import (
        ConcreteStrategyYourAlgorithm,  # Замените на ваш класс стратегии
        Context,
        StrategiesManager
    )
    ALGORITHM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Предупреждение: {e}")
    ALGORITHM_AVAILABLE = False
```

#### Шаг 3: Настройте ID Стратегии

В каждой тестовой функции замените:

```python
config = StrategiesManager.getStrategyRunConfigById("youralgorithm")  # Замените на ID вашего алгоритма
```

ID стратегии обычно соответствует имени в нижнем регистре (например, `"dbscan_sk"`, `"waveclustering"`, `"spectral_biclustering_sk"`).

#### Шаг 4: Настройте Параметры

В тестовых функциях настройте параметры вашего алгоритма:

```python
config["parameter1"] = value1
config["parameter2"] = value2
```

#### Шаг 5: Запустите Тест

```bash
python TestMethods/test_your_algorithm.py
```

### Стандартная Структура Теста

Все тесты должны содержать следующие функции:

1. **`test_basic_2d_clustering()`** - базовая 2D кластеризация
   - Генерирует простой датасет (blobs)
   - Сравнивает истинные и предсказанные кластеры
   - Сохраняет: `test_basic_2d.png`

2. **`test_parameter_sensitivity()`** - чувствительность к параметрам
   - Тестирует разные значения ключевого параметра
   - Сохраняет: `test_parameters.png`

3. **`test_different_datasets()`** - разные типы датасетов
   - Тестирует на blobs, moons, circles
   - Сохраняет: `test_datasets.png`

4. **`test_3d_clustering()`** - 3D кластеризация
   - Генерирует 3D данные
   - Визуализирует в 3D и 2D проекциях
   - Сохраняет: `test_3d.png`

5. **`test_strategy_integration()`** - интеграция с фреймворком
   - Тестирует через Strategy Pattern
   - Использует `Context` и `do_some_clustering_points()`
   - Сохраняет: `test_strategy.png`

### Пример: Минимальный Тест

```python
"""
Тестовый скрипт для проверки YourAlgorithm с визуализацией
Автор: Ваше Имя your.email@example.com
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
from sklearn.datasets import make_blobs, make_moons, make_circles

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

ALGORITHM_NAME = "YourAlgorithm"

try:
    from ClusteringMethods.ClasteringAlgorithms import (
        ConcreteStrategyYourAlgorithm,
        Context,
        StrategiesManager
    )
    ALGORITHM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Предупреждение: {e}")
    ALGORITHM_AVAILABLE = False

STRATEGY_AVAILABLE = ALGORITHM_AVAILABLE

TEST_DIR = Path(__file__).parent
IMAGES_DIR = TEST_DIR / "Images" / ALGORITHM_NAME
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print(f"📁 Директория для результатов: {IMAGES_DIR}")
print("="*80 + "\n")

def generate_test_data_2d(dataset_type='blobs', n_samples=300, **kwargs):
    np.random.seed(kwargs.get('random_state', 42))
    if dataset_type == 'blobs':
        X, y_true = make_blobs(n_samples=n_samples, n_features=2,
                              centers=kwargs.get('centers', 3),
                              cluster_std=kwargs.get('cluster_std', 0.5),
                              random_state=kwargs.get('random_state', 42))
    elif dataset_type == 'moons':
        X, y_true = make_moons(n_samples=n_samples,
                               noise=kwargs.get('noise', 0.05),
                               random_state=kwargs.get('random_state', 42))
    elif dataset_type == 'circles':
        X, y_true = make_circles(n_samples=n_samples,
                                 noise=kwargs.get('noise', 0.05),
                                 factor=kwargs.get('factor', 0.5),
                                 random_state=kwargs.get('random_state', 42))
    else:
        raise ValueError(f"Unknown dataset type: {dataset_type}")
    return X, y_true

def generate_test_data_3d(n_samples=300, n_clusters=3, cluster_std=0.5):
    X, y_true = make_blobs(n_samples=n_samples, n_features=3,
                          centers=n_clusters, cluster_std=cluster_std,
                          random_state=42)
    return X, y_true

def save_figure(fig, filename, dpi=150):
    output_path = IMAGES_DIR / filename
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✅ Сохранено: {output_path.name}")

def test_basic_2d_clustering():
    print("="*80)
    print("ТЕСТ 1: Базовая 2D Кластеризация")
    print("="*80)
    if not ALGORITHM_AVAILABLE:
        print("❌ Алгоритм не доступен. Пропускаем тест.")
        return
    
    X, y_true = generate_test_data_2d('blobs', n_samples=300, centers=3, cluster_std=0.5)
    
    config = StrategiesManager.getStrategyRunConfigById("youralgorithm")
    # Настройте параметры вашего алгоритма
    # config["param1"] = value1
    
    strategy = ConcreteStrategyYourAlgorithm()
    y_pred = strategy.clastering_points(X, config)
    
    n_clusters_pred = len(np.unique(y_pred[y_pred != -1]))
    n_clusters_true = len(np.unique(y_true))
    
    print(f"Количество точек: {len(X)}")
    print(f"Истинное количество кластеров: {n_clusters_true}")
    print(f"Найдено кластеров: {n_clusters_pred}")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    scatter1 = axes[0].scatter(X[:, 0], X[:, 1], c=y_true, cmap='viridis',
                              alpha=0.6, s=30, edgecolors='k', linewidth=0.5)
    axes[0].set_title('Истинные Кластеры', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('X₁', fontsize=12)
    axes[0].set_ylabel('X₂', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    plt.colorbar(scatter1, ax=axes[0], label='Истинная метка')
    
    scatter2 = axes[1].scatter(X[:, 0], X[:, 1], c=y_pred, cmap='tab10',
                              alpha=0.6, s=30, edgecolors='k', linewidth=0.5)
    axes[1].set_title(f'{ALGORITHM_NAME} Результаты\n({n_clusters_pred} кластеров)',
                     fontsize=14, fontweight='bold')
    axes[1].set_xlabel('X₁', fontsize=12)
    axes[1].set_ylabel('X₂', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    plt.colorbar(scatter2, ax=axes[1], label='Предсказанная метка')
    plt.tight_layout()
    save_figure(fig, 'test_basic_2d.png')
    print()

# Добавьте остальные тестовые функции (test_parameter_sensitivity, 
# test_different_datasets, test_3d_clustering, test_strategy_integration)

def main():
    print("\n" + "="*80)
    print(f"ТЕСТИРОВАНИЕ АЛГОРИТМА: {ALGORITHM_NAME}")
    print("="*80 + "\n")
    if not ALGORITHM_AVAILABLE:
        print("❌ ОШИБКА: Алгоритм не найден!")
        return
    try:
        test_basic_2d_clustering()
        # Добавьте вызовы остальных тестов
        print("="*80)
        print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО! ✅")
        print("="*80)
        print(f"\n📊 Результаты сохранены в: {IMAGES_DIR}")
        print(f"📁 Всего файлов: {len(list(IMAGES_DIR.glob('*.png')))}")
        print("\nОткройте изображения для просмотра результатов!")
        print("="*80 + "\n")
        plt.show()
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

---

### Расширенный Тест (как test_wave.py)

Все тесты в проекте следуют единому стандарту. Используйте `test_template.py` как основу - он уже содержит все необходимые функции для расширенного тестирования.

---

## Примеры Использования

### Пример 1: Быстрый Тест Нового Алгоритма

```bash
# 1. Создайте файл теста из шаблона
cd TestMethods
cp test_template.py test_myalgorithm.py

# 2. Отредактируйте test_myalgorithm.py
# - Замените ALGORITHM_NAME = "YourAlgorithm" на имя вашего алгоритма
# - Замените импорты на ваши классы
# - Замените "youralgorithm" на ID вашей стратегии в StrategiesManager
# - Настройте параметры в тестовых функциях

# 3. Запустите
python TestMethods/test_myalgorithm.py

# 4. Проверьте результаты
ls TestMethods/Images/MyAlgorithm/
# Должны быть созданы файлы:
# - test_basic_2d.png
# - test_parameters.png
# - test_datasets.png
# - test_3d.png
# - test_strategy.png
```

### Пример 2: Сравнение Параметров

```python
# В вашем test_*.py

def compare_parameters():
    """Сравнение разных значений параметра"""
    
    X, y_true = generate_data()
    
    param_values = [0.1, 0.5, 1.0, 2.0]
    results = []
    
    for param in param_values:
        model = YourAlgorithm(param=param)
        y_pred = model.fit_predict(X)
        results.append((param, y_pred, len(np.unique(y_pred))))
    
    # Визуализация
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.ravel()
    
    for i, (param, labels, n_clusters) in enumerate(results):
        axes[i].scatter(X[:, 0], X[:, 1], c=labels, cmap='tab10')
        axes[i].set_title(f'Param={param}, Clusters={n_clusters}')
    
    plt.savefig(IMAGES_DIR / "comparison.png")
```

### Пример 3: Тест на Реальных Данных

```python
def test_real_data():
    """Тест на реальном датасете"""
    
    # Загрузка данных
    from sklearn.datasets import load_iris
    iris = load_iris()
    X = iris.data[:, :2]  # Только первые 2 признака для визуализации
    
    # Кластеризация
    model = YourAlgorithm()
    labels = model.fit_predict(X)
    
    # Визуализация
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
    plt.title('Iris Dataset Clustering')
    plt.xlabel('Sepal Length')
    plt.ylabel('Sepal Width')
    
    plt.savefig(IMAGES_DIR / "iris_test.png")
```

---

## Рекомендации

### Хорошие Практики

1. **Именование файлов:**
   - `test_{algorithm_name}.py` - для скриптов тестирования
   - Стандартные имена изображений (одинаковые для всех алгоритмов):
     - `test_basic_2d.png` - базовая 2D кластеризация
     - `test_parameters.png` - чувствительность к параметрам
     - `test_datasets.png` - разные типы датасетов
     - `test_3d.png` - 3D кластеризация
     - `test_strategy.png` - интеграция с фреймворком

2. **Структура теста (стандартная для всех тестов):**
   ```python
   # 1. Импорты (numpy, matplotlib, sklearn, pathlib)
   # 2. Настройка PROJECT_ROOT и sys.path
   # 3. ALGORITHM_NAME и импорты алгоритма
   # 4. Настройка TEST_DIR и IMAGES_DIR
   # 5. Функции генерации данных (generate_test_data_2d, generate_test_data_3d)
   # 6. Функция save_figure
   # 7. Стандартные тестовые функции:
   #    - test_basic_2d_clustering()
   #    - test_parameter_sensitivity()
   #    - test_different_datasets()
   #    - test_3d_clustering()
   #    - test_strategy_integration()
   # 8. Главная функция main()
   ```

3. **Визуализация:**
   - Используйте высокое разрешение (dpi=150 или 300)
   - Добавляйте заголовки и подписи осей
   - Используйте сетку для удобства чтения
   - Сохраняйте с `bbox_inches='tight'`

4. **Документация:**
   - Добавляйте docstring к каждой функции
   - Комментируйте сложные участки кода
   - Указывайте автора и дату в заголовке

5. **Обработка ошибок:**
   ```python
   try:
       test_function()
   except Exception as e:
       print(f"❌ Ошибка: {e}")
       import traceback
       traceback.print_exc()
   ```

### Чего Избегать

1.  Жестко зашитые пути (используйте `Path(__file__).parent`)
2.  Сохранение в корень проекта (используйте `Images/` директорию)
3.  Отсутствие обработки ошибок
4.  Визуализации без подписей и заголовков
5.  Тесты без вывода статистики

---

## Шаблон Визуализации

### Базовый График

```python
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='tab10',
           alpha=0.6, s=30, edgecolors='k', linewidth=0.5)
plt.title('Algorithm Name Results', fontsize=14, fontweight='bold')
plt.xlabel('Feature 1', fontsize=12)
plt.ylabel('Feature 2', fontsize=12)
plt.grid(True, alpha=0.3)
plt.colorbar(label='Cluster')
plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight')
```

### Сравнение (Multiple Subplots)

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 12))
axes = axes.ravel()

for i, (title, data, labels) in enumerate(test_cases):
    axes[i].scatter(data[:, 0], data[:, 1], c=labels, cmap='tab10')
    axes[i].set_title(title, fontsize=12, fontweight='bold')
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight')
```

### 3D Визуализация

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels, 
                    cmap='tab10', alpha=0.6, s=30)
ax.set_xlabel('X₁')
ax.set_ylabel('X₂')
ax.set_zlabel('X₃')
ax.set_title('3D Clustering Results', fontsize=14, fontweight='bold')

plt.colorbar(scatter, label='Cluster')
plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight')
```

---

## FAQ

### Где должен находиться файл теста?

**Ответ:** В директории `TestMethods/`:
```
TestMethods/test_your_algorithm.py
```

### Куда сохраняются результаты?

**Ответ:** В поддиректорию `Images/`:
```
TestMethods/Images/{AlgorithmName}/
```

### Как автоматически создать директорию для результатов?

**Ответ:** Используйте `Path` и `mkdir`:
```python
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "Images" / "YourAlgorithm"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
```

### Как добавить метаданные к изображениям?

**Ответ:** Используйте параметр `metadata`:
```python
metadata = {
    'Title': 'Test Results',
    'Author': 'Your Name',
    'Algorithm': 'YourAlgorithm',
    'Date': 'гггг-мм-дд'
}

plt.savefig(output, dpi=150, bbox_inches='tight', metadata=metadata)
```

### Можно ли запускать несколько тестов одновременно?

**Ответ:** Да, каждый тест независим и сохраняет результаты в свою директорию.

### Как сравнить разные алгоритмы?

**Ответ:** Создайте отдельный тест `test_comparison.py`:
```python
from ClusteringMethods.ClasteringAlgorithms import (
    ConcreteStrategyWaveClustering,
    ConcreteStrategyDBSCAN_from_SKLEARN,
    StrategiesManager
)

# Генерация данных
X, y_true = generate_test_data_2d('blobs', n_samples=300, centers=3)

# Сравнение алгоритмов
algorithms = [
    ("WaveClustering", "waveclustering", ConcreteStrategyWaveClustering()),
    ("DBSCAN", "dbscan_sk", ConcreteStrategyDBSCAN_from_SKLEARN())
]

fig, axes = plt.subplots(1, len(algorithms), figsize=(5*len(algorithms), 5))

for i, (name, strategy_id, strategy) in enumerate(algorithms):
    config = StrategiesManager.getStrategyRunConfigById(strategy_id)
    # Настройте параметры
    y_pred = strategy.clastering_points(X, config)
    
    axes[i].scatter(X[:, 0], X[:, 1], c=y_pred, cmap='tab10',
                   alpha=0.6, s=30, edgecolors='k', linewidth=0.5)
    axes[i].set_title(f'{name}\n({len(np.unique(y_pred))} кластеров)')
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(IMAGES_DIR / "comparison.png", dpi=150, bbox_inches='tight')
```

---

## Поддержка

Если у вас возникли вопросы:
1. Проверьте примеры в существующих тестах (`test_wave.py`, `test_dbscan.py`, `test_spectral_biclustering.py`)
2. Используйте шаблон `test_template.py` - он содержит полную структуру стандартного теста
3. Убедитесь, что ваш алгоритм правильно интегрирован в `ClusteringMethods.ClasteringAlgorithms`
4. Проверьте, что ID стратегии в `StrategiesManager` соответствует используемому в тесте

## Важные Замечания

### Стандартизация Тестов

Все тесты в проекте следуют единому стандарту:
- ✅ Одинаковая структура файлов
- ✅ Одинаковые имена тестовых функций
- ✅ Одинаковые имена выходных изображений
- ✅ Использование `StrategiesManager` и `clastering_points()`
- ✅ Единый стиль визуализации

Это обеспечивает:
- Легкость сравнения результатов разных алгоритмов
- Простоту добавления новых тестов
- Консистентность документации

### Использование Strategy Pattern

Все тесты должны использовать паттерн Strategy через:
- `StrategiesManager.getStrategyRunConfigById(strategy_id)` - получение конфигурации
- `strategy.clastering_points(X, config)` - кластеризация точек
- `Context(strategy).do_some_clustering_points(X.T, config)` - для теста интеграции

Это гарантирует совместимость с основным GUI фреймворком.

---

**Авторы:** Левинский Григорий Дмитриевич [levinskiy@mirea.ru]  
**Последнее обновление:** 2025-11-06

---
