from abc import abstractmethod
import numpy as np
import pandas as pd
import sqlite3

"""
A class that encapsulates the logic surrounding working
with values and labels of Tensorflow.
"""
class Data:
    def __init__(self, df, values, model):
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
    
class Source:
    def __init__(self, label_encoder):
        self._label_encoder = label_encoder

    def create_data_frame(self):
        df = self._read_source()
        df["encoded_meal"] = self._label_encoder.fit_transform(df["meal"])

        return df

    @abstractmethod
    def _read_source(self):
        pass

class CsvSource(Source):
    def __init__(self, label_encoder, path):
        super().__init__(label_encoder)
        self._path = path
    
    def _read_source(self):
        return pd.read_csv(self._path)
    
class SqlSource(Source):
    def __init__(self, label_encoder, path):
        super().__init__(label_encoder)
        self._path = path
    
    def _read_source(self):
        # TODO: Error check
        con = sqlite3.connect(self._path)
        df = pd.read_sql("SELECT id,meal,complexity,soup,takeaway," \
            "sweet,meat,cold,remains,fish,salad,fast,vegetarian,meatloaf," \
            "noodles,mushrooms,broccoli,shrimps,zucchini,ham,rice,pizza,fruits," \
            "gnocci,spinach,beans,sugar,apples,cauliflower,feta,chicken,eggs,tuna," \
            "curd_cheese,lentils,cheese,yeast,sweet_potatoes,sausage,gorgonzola," \
            "pineapple,potatoes,dumplings,cabbage,tomatoes FROM planner_meal ORDER BY id", con, "id")
        con.close()

        return df