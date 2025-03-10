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

        for day_idx in range(7):
            sequence = self._data.last(7)

            predictions = self._data.model.predict([sequence])
            top_2 = tf.nn.top_k(predictions, k=2)
            top_2_indices = top_2.indices.numpy()

            predicted_meals = self._label_encoder.inverse_transform(top_2_indices.flatten())[:2]

            meals.append(predicted_meals[:2])

            meal_feature = self._data.get_features(predicted_meals[0])
            self._data.append(meal_feature)
        
        return meals
