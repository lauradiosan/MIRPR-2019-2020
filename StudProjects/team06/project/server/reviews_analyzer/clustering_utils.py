"""Various clustering methods."""
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from hdbscan import HDBSCAN

from .clustering_methond_type import ClusteringMethodType
from .cluster import Cluster, ClusterEntry

def cluster_data(points, method):
    """Cluster the data using the given method.

    Returns an array of clusters"""
    if method == ClusteringMethodType.KMEANS:
        return cluster_data_using_kmeans(points)
    if method == ClusteringMethodType.DBSCAN:
        return cluster_data_using_dbscan(points)
    if method == ClusteringMethodType.HDBSCAN:
        return cluster_data_using_hdbscan(points)
    if method == ClusteringMethodType.AGGLOMERATIVE:
        return cluster_data_using_agglomerative(points)

    raise Exception('Invalid clustering method.')


def cluster_data_using_kmeans(points, number_of_clusters=5):
    """TODO

    Args:
        points: a list of numpy arrays

    Returns an array of clusters."""
    kmeans = KMeans(n_clusters=number_of_clusters,
                    n_init=10,
                    max_iter=500,
                    random_state=0)
    indexes = kmeans.fit_predict(points)
    return create_clusters(number_of_clusters=number_of_clusters,
                           indexes=indexes)


def cluster_data_using_dbscan(points, eps=9.7, min_samples=2):
    """TODO

    Args:
        points: a list of numpy arrays

    Returns an array of clusters."""
    dbscan = DBSCAN(eps=eps, min_samples=min_samples,  algorithm='ball_tree', 
        metric='minkowski', leaf_size=90, p=2)
    indexes = dbscan.fit_predict(points)
    number_of_clusters = len(set(dbscan.labels_)) - \
        (1 if -1 in dbscan.labels_ else 0)
    return create_clusters(number_of_clusters=number_of_clusters,
                           indexes=indexes)


def cluster_data_using_hdbscan(points):
    """TODO

    Args:
        points: a list of numpy arrays

    Returns an array of clusters."""
    dbscan = HDBSCAN(algorithm='best', alpha=1.0, approx_min_span_tree=True,
        gen_min_span_tree=False, leaf_size=40, 
        metric='euclidean', min_cluster_size=5, min_samples=None, p=None)
    indexes = dbscan.fit_predict(points)
    number_of_clusters = len(set(dbscan.labels_)) - \
        (1 if -1 in dbscan.labels_ else 0)
    return create_clusters(number_of_clusters=number_of_clusters,
                           indexes=indexes)


def cluster_data_using_agglomerative(points, number_of_clusters=5):
    """TODO

    Args:
        points: a list of numpy arrays

    Returns an array of clusters."""
    agglomerative = AgglomerativeClustering(linkage='complete', 
                                            affinity='euclidean', 
                                            n_clusters=number_of_clusters)
    indexes = agglomerative.fit_predict(points)
    number_of_clusters = len(set(agglomerative.labels_)) - \
        (1 if -1 in agglomerative.labels_ else 0)
    return create_clusters(number_of_clusters=number_of_clusters,
                           indexes=indexes)


def create_clusters(number_of_clusters, indexes):
    """Returns a list of Cluster objects created based on the given params."""
    clusters = [Cluster() for _ in range(number_of_clusters)]
    for index in range(len(indexes)):
        entry = ClusterEntry()
        entry.label = index
        clusters[indexes[index]].add(entry)
    return clusters
