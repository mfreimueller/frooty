from django.db import models
from rest_framework import serializers

class Meal(models.Model):
    meal = models.CharField(max_length=200)
    complexity = models.PositiveSmallIntegerField()
    soup  = models.PositiveSmallIntegerField()
    takeaway = models.PositiveSmallIntegerField()
    sweet = models.PositiveSmallIntegerField()
    meat = models.PositiveSmallIntegerField()
    cold = models.PositiveSmallIntegerField()
    remains = models.PositiveSmallIntegerField()
    fish = models.PositiveSmallIntegerField()
    salad = models.PositiveSmallIntegerField()
    fast = models.PositiveSmallIntegerField()
    vegetarian = models.PositiveSmallIntegerField()
    meatloaf = models.PositiveSmallIntegerField()
    noodles = models.PositiveSmallIntegerField()
    mushrooms = models.PositiveSmallIntegerField()
    broccoli = models.PositiveSmallIntegerField()
    shrimps = models.PositiveSmallIntegerField()
    zucchini = models.PositiveSmallIntegerField()
    ham = models.PositiveSmallIntegerField()
    rice = models.PositiveSmallIntegerField()
    pizza = models.PositiveSmallIntegerField()
    fruits = models.PositiveSmallIntegerField()
    gnocci = models.PositiveSmallIntegerField()
    spinach = models.PositiveSmallIntegerField()
    beans = models.PositiveSmallIntegerField()
    sugar = models.PositiveSmallIntegerField()
    apples = models.PositiveSmallIntegerField()
    cauliflower = models.PositiveSmallIntegerField()
    feta = models.PositiveSmallIntegerField()
    chicken = models.PositiveSmallIntegerField()
    eggs = models.PositiveSmallIntegerField()
    tuna = models.PositiveSmallIntegerField()
    curd_cheese = models.PositiveSmallIntegerField()
    lentils = models.PositiveSmallIntegerField()
    cheese = models.PositiveSmallIntegerField()
    yeast = models.PositiveSmallIntegerField()
    sweet_potatoes = models.PositiveSmallIntegerField()
    sausage = models.PositiveSmallIntegerField()
    gorgonzola = models.PositiveSmallIntegerField()
    pineapple = models.PositiveSmallIntegerField()
    potatoes = models.PositiveSmallIntegerField()
    dumplings = models.PositiveSmallIntegerField()
    cabbage = models.PositiveSmallIntegerField()
    tomatoes = models.PositiveSmallIntegerField()

class MealSerialize(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id', 'name']
    
    def get_name(self, obj):
        return obj.meal