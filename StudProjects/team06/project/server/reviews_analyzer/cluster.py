"""Classes for clusters."""

class ClusterEntry():
    """An entry in a cluster."""
    def __init__(self):
        """Initializes a new entry. Label is the index of the review amongst the
        reviews with the same key."""
        self.label = ""


class Cluster():
    """An object representing a cluster, containing multiple entries."""
    def __init__(self):
        """Initializes an empty cluster."""
        self.entries = []
        self.keywords = []


    def add(self, entry):
        """Adds a new entry to the cluster."""
        self.entries = self.entries + [entry]
