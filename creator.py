from data import Data
import numpy as np
import keras
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

"""
The class responsible for creating the data and model
for Tensorflow and Keras.

TODO: Find a better name.
"""
class Creator:
    def __init__(self, source):
        self._source = source
    
    def create_data(self):
        df = self._source.create_data_frame()
        shape, values, labels = self._prepare_data(df)

        onehot_encoder = OneHotEncoder(sparse_output=False)
        labels_encoded = onehot_encoder.fit_transform(labels.reshape(-1, 1))

        print("One-Hot-kodierte Mahlzeiten:")
        print(labels_encoded)

        n_classes = labels_encoded.shape[1]
        model = self._create_model(shape, n_classes, values, labels_encoded)

        return Data(df, values, model)

    def _create_model(self, shape, n_classes, values, labels_encoded):
        sequence_length = 7
        model = keras.Sequential([
            keras.layers.LSTM(64, activation="relu", input_shape=(sequence_length, shape[1]), return_sequences=False),
            keras.layers.Dense(32, activation="relu"),
            keras.layers.Dense(n_classes, activation="softmax")  # Vorhersage einer Mahlzeit
        ])

        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

        model.fit(values, labels_encoded, epochs=50, batch_size=4)
        return model
    
    def _prepare_data(self, df):
        raw_values = df.drop(columns=["meal"]).values
        raw_labels = df["encoded_meal"].values 

        sequence_length = 7
        values = []
        labels = []

        for i in range(len(raw_values) - sequence_length):
            values.append(raw_values[i:i + sequence_length])
            labels.append(raw_labels[i + sequence_length])

        values = np.array(values)
        labels = np.array(labels)

        return raw_values.shape, values, labels
    
