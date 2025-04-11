
from .source import MariaDBSource
from .utils import Predictor, SetupHelper

def predict_meals(connector, label_encoder, family_id: int):
    source = MariaDBSource(label_encoder, connector)

    setupHelper = SetupHelper(source)
    data = setupHelper.create_data(family_id)

    predictor = Predictor(data, label_encoder)

    meals = predictor.predict()
    return meals
