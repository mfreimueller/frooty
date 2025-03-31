from sklearn.preprocessing import LabelEncoder
from .models import SqlSource
from .utils import Predictor, SetupHelper

def predict_meals(family_id: int):
    label_encoder = LabelEncoder()
    source = SqlSource(label_encoder, "db.sqlite3")

    setupHelper = SetupHelper(source)
    data = setupHelper.create_data(family_id)

    predictor = Predictor(data, label_encoder)

    meals = predictor.predict()
    return meals
