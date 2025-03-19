from apps.suggest_logic.services import predict_meals

def plan_meals():
    predicted_meals = predict_meals()
    return predicted_meals
