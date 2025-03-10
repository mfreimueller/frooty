from abc import abstractmethod
import pandas as pd

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