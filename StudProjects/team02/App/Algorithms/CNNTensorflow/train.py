import model
from filter_dataset import filter_dataset
from config import *

if __name__ == "__main__":
    global train_dataset
    filter_dataset(train_dataset)
    model.train()
    