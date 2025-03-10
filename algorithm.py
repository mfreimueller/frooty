from sklearn.preprocessing import LabelEncoder

from predictor import Predictor
from source import CsvSource
from creator import Creator

label_encoder = LabelEncoder()
source = CsvSource(label_encoder, "out.csv")

creator = Creator(source)
data = creator.create_data()

predictor = Predictor(data, label_encoder)

meals = predictor.predict()
print(meals)