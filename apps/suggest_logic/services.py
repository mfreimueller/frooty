from sklearn.preprocessing import LabelEncoder
from .models import SqlSource
from .utils import Predictor, SetupHelper

def predict_meals():
    label_encoder = LabelEncoder()
    source = SqlSource(label_encoder, "db.sqlite3")

    setupHelper = SetupHelper(source)
    data = setupHelper.create_data()

    predictor = Predictor(data, label_encoder)

    meals = predictor.predict()
    return meals
