"""
ClusteringMethods Package - UPDATED with VP-Tree Bregman (БЕЗ pyBregman)

Автоматическая загрузка всех алгоритмов кластеризации
"""

# Импорт базовых классов и алгоритмов
from ClusteringMethods.ClasteringAlgorithms import *

# Импорт WaveClustering
try:
    from ClusteringMethods.WaveClusteringAlgorithm import (
        ConcreteStrategyWaveClustering,
        WaveClustering
    )
    print("✅ WaveClustering успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️ WaveClustering не загружен: {e}")
    print("   Убедитесь, что установлены: pip install PyWavelets scipy")

# Импорт BallTree Clustering
try:
    from ClusteringMethods.BallTreeClustering import (
        ConcreteStrategyBallTree,
        BallTreeClustering
    )
    print("✅ BallTree Clustering успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️ BallTree Clustering не загружен: {e}")
    print("   Убедитесь, что установлены: pip install scikit-learn scipy numpy")

# ============================================================================
# Импорт VP-Tree Bregman Clustering (БЕЗ pyBregman!)
# ============================================================================
try:
    from ClusteringMethods.VPTreeClustering import (
        ConcreteStrategyVPTreeBregman,
        VPTreeBregmanClustering
    )
    print("✅ VP-Tree Bregman Clustering успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️ VP-Tree Bregman Clustering не загружен: {e}")
    print("   Убедитесь, что установлены: pip install scipy scikit-learn numpy")

try:
    from ClusteringMethods.HPStreamClasteringAlgorithm import (
        ConcreteStrategyHPStream,
        HPStreamClustering
    )
    print("✅ HPStreamClustering успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  HPStreamClustering не загружен: {e}")
    print("   Убедитесь, что установлены: pip install numpy scikit-learn")

# Импорт KMeans с PCA
try:
    from ClusteringMethods.KMeansClustering import (
        ConcreteStrategyKMeans_from_SKLEARN
    )
    print("✅ KMeans (SKLearn) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  KMeans (SKLearn) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install scikit-learn numpy")

# Импорт MiniBatchKMeans
try:
    from ClusteringMethods.MiniBatchKMeansClustering import (
        ConcreteStrategyMiniBatchKMeans_from_SKLEARN
    )
    print("✅ MiniBatchKMeans (SKLearn) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  MiniBatchKMeans (SKLearn) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install scikit-learn numpy")

# Импорт AgglomerativeClustering
try:
    from ClusteringMethods.AgglomerativeClustering import (
        ConcreteStrategyAgglomerative_from_SKLEARN
    )
    print("✅ AgglomerativeClustering (SKLearn) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  AgglomerativeClustering (SKLearn) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install scikit-learn numpy")

# Импорт MeanShift
try:
    from ClusteringMethods.MeanShiftClustering import (
        ConcreteStrategyMeanShift_from_SKLEARN
    )
    print("✅ MeanShift (SKLearn) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  MeanShift (SKLearn) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install scikit-learn numpy")

# Импорт K-Medians
try:
    from ClusteringMethods.KMediansClustering import (
        ConcreteStrategyKMedians_from_PYCLUSTERING
    )
    print("✅ K-Medians (PyClustering) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  K-Medians (PyClustering) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install pyclustering scikit-learn numpy")

# Импорт X-Means
try:
    from ClusteringMethods.XMeansClustering import (
        ConcreteStrategyXMeans_from_PYCLUSTERING
    )
    print("✅ X-Means (PyClustering) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  X-Means (PyClustering) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install pyclustering scikit-learn numpy")

# Импорт MBSAS
try:
    from ClusteringMethods.MBSASClustering import (
        ConcreteStrategyMBSAS_from_PYCLUSTERING
    )
    print("✅ MBSAS (PyClustering) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  MBSAS (PyClustering) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install pyclustering scikit-learn numpy")

# Импорт SOM
try:
    from ClusteringMethods.SOMClustering import (
        ConcreteStrategySOM_from_PYCLUSTERING
    )
    print("✅ SOM (PyClustering) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  SOM (PyClustering) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install pyclustering scikit-learn numpy")

# Импорт CLIQUE
try:
    from ClusteringMethods.CliqueClustering import (
        ConcreteStrategyCLIQUE
    )
    print("✅ CLIQUE (pyclustering) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  CLIQUE (pyclustering) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install pyclustering numpy")

# Импорт CLARANS
try:
    from ClusteringMethods.ClaransClustering import (
        ConcreteStrategyCLARANS
    )
    print("✅ CLARANS (pyclustering) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️  CLARANS (pyclustering) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install pyclustering numpy")

# Импорт DENCLUE
try:
    from ClusteringMethods.DENCLUEClustering import DENCLUE, ConcreteStrategyDENCLUE
    print("✅ DENCLUE успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️ DENCLUE не загружен: {e}")
    print("   Убедитесь, что установлены: pip install numpy scipy scikit-learn")

# Импорт расширенного FCM (существующий fuzzy_cmeans сохраняется)
try:
    from ClusteringMethods.FCMClustering import ConcreteStrategyFCM_from_PYCLUSTERING
    print("✅ FCM (PyClustering) успешно загружен и зарегистрирован!")
except ImportError as e:
    print(f"⚠️ FCM (PyClustering) не загружен: {e}")
    print("   Убедитесь, что установлены: pip install pyclustering scikit-learn numpy")

# Экспортируем все
__all__ = [
    'Strategy',
    'StrategiesManager',
    'Context',
    'ConcreteStrategyWaveClustering',
    'WaveClustering',
    'ConcreteStrategyBallTree',
    'BallTreeClustering',
    'ConcreteStrategyVPTreeBregman',
    'VPTreeBregmanClustering',
    'ConcreteStrategyHPStream',
    'HPStreamClustering',
    'ConcreteStrategyKMeans_from_SKLEARN',
    'ConcreteStrategyMiniBatchKMeans_from_SKLEARN',
    'ConcreteStrategyAgglomerative_from_SKLEARN',
    'ConcreteStrategyMeanShift_from_SKLEARN',
    'ConcreteStrategyKMedians_from_PYCLUSTERING',
    'ConcreteStrategyXMeans_from_PYCLUSTERING',
    'ConcreteStrategyMBSAS_from_PYCLUSTERING',
    'ConcreteStrategySOM_from_PYCLUSTERING',
    'ConcreteStrategyCLIQUE',
    'ConcreteStrategyCLARANS',
    'DENCLUE',
    'ConcreteStrategyDENCLUE',
    'ConcreteStrategyFCM_from_PYCLUSTERING',
]
