from .data import Data
import torch
from sklearn.preprocessing import LabelEncoder

"""
Predicts a list of 7 meals, based on the existing
list of meals, creating alternatives for each meal.
"""
def predict(data: Data, label_encoder: LabelEncoder):
    meals = []

    for _ in range(7):
        sequence = data.last(365)

        predictions = data.model.predict([sequence])
        top_2 = torch.topk(predictions, k=2)
        top_2_indices = top_2.indices.numpy()

        predicted_meals = label_encoder.inverse_transform(top_2_indices.flatten())[:2]

        meals.append(predicted_meals[0]) # TODO: implement alternatives

        meal_feature = data.get_features(predicted_meals[0])
        data.append(meal_feature)
    
    return meals