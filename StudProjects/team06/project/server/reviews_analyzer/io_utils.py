"""Read and write utils for pandas.DataFrame."""
import os
import pandas


def load_dataset_from_file(filename, columns):
    """Returns the given data as a pandas.DataFrame object."""
    return pandas.read_csv(filename,
                           header=0,
                           nrows=405, # first hotel only
                           quotechar='"',
                           lineterminator='\n',
                           usecols=columns)


def load_dataset_from_numpy_array(data, columns):
    """Returns the given data as a pandas.DataFrame object."""
    if len(data[0]) != len(columns):
        raise Exception('Invalid number of columns')
    return pandas.DataFrame(data, columns=columns)


def save_dataset(dataset, filename, columns):
    """Saves the given pands.DataFrame to the given csv file."""
    dataset.to_csv(filename, quotechar='"', columns=columns)


if __name__ == '__main__':
    dataset_filename = os.path.join(os.path.dirname(
        __file__), 'datasets/hotel_reviews_booking/Hotel_Reviews.csv')
    columns_to_extract = ['Hotel_Address', 'Hotel_Name',
                          'Negative_Review', 'Positive_Review']
    a = load_dataset_from_file(dataset_filename, columns=columns_to_extract)
    print(type(a))
    # print(a.head)

    array = [[10, 100, 'a', 1], [20, 21, 'b', 2]]
    b = load_dataset_from_numpy_array(array, columns=columns_to_extract)
    print(type(b))
    # print(b.head)
