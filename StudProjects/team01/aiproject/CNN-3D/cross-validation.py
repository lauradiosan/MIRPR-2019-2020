def get_validation_set(data, batch_size, iteration):
    start = iteration * batch_size
    end = start + batch_size
    return data[start:end]


def get_training_set(data, batch_size, iteration):
    training_set = []
    if iteration != 0:
        training_set.extend(data[0: iteration * batch_size])
    start = iteration * batch_size + batch_size
    training_set.extend(data[start:])
    return training_set


def get_data_set(data, batch_size, iteration):
    return {"validation": get_validation_set(data, batch_size, iteration),
            "train": get_training_set(data, batch_size, iteration)}


def k_fold_cross_validation(data, *, k=4):
    batch_size = len(data) // k
    return [get_data_set(data, batch_size, i) for i in range(k)]


'''
    Usage example:
        print(k_fold_cross_validation([1, 2, 3, 4, 5, 6, 7, 8], k=2))
        Output:
            [{'validation': [1, 2, 3, 4], 'train': [5, 6, 7, 8]}, {'validation': [5, 6, 7, 8], 'train': [1, 2, 3, 4]}]

        print(k_fold_cross_validation([1, 2, 3, 4, 5, 6, 7, 8], k=2))
        Output:
            [{'validation': [1, 2], 'train': [3, 4, 5, 6, 7, 8]}, {'validation': [3, 4], 'train': [1, 2, 5, 6, 7, 8]}, {'validation': [5, 6], 'train': [1, 2, 3, 4, 7, 8]}]
'''
