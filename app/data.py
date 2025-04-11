from pandas import DataFrame
import numpy as np

"""
A class that encapsulates the logic surrounding working
with values and labels of Tensorflow.
"""
class Data:
    def __init__(self, df: DataFrame, values, model):
        self._df = df
        self._values = values
        self.model = model

    def last(self, amount):
        return self._values[-amount:]

    """
    Append a new value tensor to the existing data values.
    """
    def append(self, value):
        shape_size = self._values.shape[1] - 1
        count = self._values.shape[0]

        new_value = []
        for idx in range(count - shape_size, count):
            new_value.append(self._values[idx][6])
        new_value.append(value)

        self._values = np.vstack([ self._values, [ new_value ] ])

    """
    Look up the features associated with a given label.
    Throws a ValueError iff the label wasn't found.
    """
    def get_features(self, label):
        row = self._df[self._df["meal"] == label]

        if row.empty:
            raise ValueError(f"Unknown label: {label}")

        return row.drop(columns=["meal"]).values[0]