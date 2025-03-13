from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import get_all_meals, plan_meals

"""
The API endpoint that predicts the next seven meals
(including an alternative for each meal) and returns
the generated results.
"""
@api_view(["POST"])
def suggest(request):
    next_meals = plan_meals()
    return Response({ "prediction": next_meals })

"""
An API endpoint that creates new meal entries in
the internal data storage to use for further predictions.
The meal entries are appended to the storage and are
treated as the latest elements.
"""
@api_view(["POST"])
def create(request):
    pass

"""
An API endpoint that updates the previous n-meal entries
in the internal data storage, to reflect changes in
further predictions.
"""
@api_view(["POST"])
def update(request):
    pass

"""
An API endpoint that returns all meal entries of the
internal data storage.
"""
@api_view(["GET"])
def get_all(request):
    all_meals = get_all_meals()
    return Response({ "history": all_meals })