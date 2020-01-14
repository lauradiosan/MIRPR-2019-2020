"""Utils for nltk."""
from nltk import Tree


def get_nodes(tree, label):
    """TODO

    Returns an empty list if no such label was found."""
    result = []
    for node in tree:
        if isinstance(node, Tree):
            if node.label() == label:
                result = result + [node.leaves()]
            result = result + get_nodes(node, label)
    return result


def is_node_about_subject(node, subject, stemmer):
    """Checks whether the given node contains a leaf present in the given subject list."""
    for leaf in node:
        stemmed_word = stemmer.stem(leaf[0])
        if stemmed_word in subject:
            return True
    return False


def extract_cardinal_number(node):
    """Return the first occurence of a leaf that has the label CD.

    Returns None if no such leaf was found.
    TODO. explain duplcicates."""
    for leaf in node:
        if leaf[1] == 'CD':
            return leaf[0]
    return None


def extract_number_of_subject(doc, subject, lemmatizer):
    """TODO

    Returns None if no such subject with a number associated was found.
    TODO. explain duplcicates."""
    tokens = [(X.orth_, X.head.orth_) for X in doc if X.tag_ == 'CD']
    if not tokens:
        return None

    tokens_about_subject = ([X for X in tokens if lemmatizer.lemmatize(X[1]) in subject])
    if not tokens_about_subject:
        return None

    return tokens_about_subject[0][0]
