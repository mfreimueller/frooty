from .models import Data
import numpy as np
import keras
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf

class Predictor:
    def __init__(self, data, label_encoder):
        self._data = data
        self._label_encoder = label_encoder

    """
    Predicts a list of 7 meals, based on the existing
    list of meals, creating alternatives for each meal.
    """
    def predict(self):
        meals = []

        for _ in range(7):
            sequence = self._data.last(7)

            predictions = self._data.model.predict([sequence])
            top_2 = tf.nn.top_k(predictions, k=2)
            top_2_indices = top_2.indices.numpy()

            predicted_meals = self._label_encoder.inverse_transform(top_2_indices.flatten())[:2]

            meals.append(predicted_meals[0]) # TODO: implement alternatives

            meal_feature = self._data.get_features(predicted_meals[0])
            self._data.append(meal_feature)
        
        return meals

"""
The class responsible for creating the data and model
for Tensorflow and Keras.

TODO: Find a better name.
"""
class SetupHelper:
    def __init__(self, source):
        self._source = source
    
    def create_data(self, family_id):
        df = self._source.create_data_frame(family_id)
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
    
