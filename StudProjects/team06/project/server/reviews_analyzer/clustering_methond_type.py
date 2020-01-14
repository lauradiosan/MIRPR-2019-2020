'''An enum for all the types of clustering used by the reviews analyzer.'''
from enum import Enum

class ClusteringMethodType(Enum):
    """An enum for all the types of clustering used by the reviews analyzer."""
    KMEANS = 0
    DBSCAN = 1
    HDBSCAN = 2
    AGGLOMERATIVE = 3
