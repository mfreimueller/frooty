from abc import abstractmethod
import pandas as pd
import sqlite3

class Source:
    def __init__(self, label_encoder):
        self._label_encoder = label_encoder

    def create_data_frame(self, group_id: int):
        df = self._read_source(group_id)
        df["encoded_meal"] = self._label_encoder.fit_transform(df["meal"])

        return df

    @abstractmethod
    def _read_source(self, family_idgroup_id: int):
        pass

class CsvSource(Source):
    def __init__(self, label_encoder, path):
        super().__init__(label_encoder)
        self._path = path
    
    def _read_source(self, group_id: int):
        return pd.read_csv(self._path)
    
class SqLightSource(Source):
    def __init__(self, label_encoder, path):
        super().__init__(label_encoder)
        self._path = path
    
    def _read_source(self, group_id: int):
        # TODO: Error check
        con = sqlite3.connect(self._path)
        df = pd.read_sql("SELECT h.id,meal,complexity,soup,takeaway," \
            "sweet,meat,cold,remains,fish,salad,fast,vegetarian,meatloaf," \
            "noodles,mushrooms,broccoli,shrimps,zucchini,ham,rice,pizza,fruits," \
            "gnocci,spinach,beans,sugar,apples,cauliflower,feta,chicken,eggs,tuna," \
            "curd_cheese,lentils,cheese,yeast,sweet_potatoes,sausage,gorgonzola," \
            "pineapple,potatoes,dumplings,cabbage,tomatoes FROM meals_meal m INNER JOIN history_history h ON name = meal WHERE h.family_id = ? ORDER BY h.date", con, "id", params=[group_id])
        con.close()

        return df
    
class MariaDBSource(Source):
    def __init__(self, label_encoder, connector):
        super().__init__(label_encoder)
        self._connector = connector
    
    def _read_source(self, group_id):
        df = pd.read_sql(
            "SELECT id, scheduled_on, rating, meal, complexity, category FROM `history_view` WHERE group_id = ? ORDER BY scheduled_on",
            self._connector,
            "id",
            params=[group_id]
        )

        return df
