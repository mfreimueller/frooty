from django.db import models
from rest_framework import serializers

class Meal(models.Model):
    meal = models.CharField(max_length=200)
    complexity = models.PositiveSmallIntegerField()
    soup  = models.PositiveSmallIntegerField(default=0)
    takeaway = models.PositiveSmallIntegerField(default=0)
    sweet = models.PositiveSmallIntegerField(default=0)
    meat = models.PositiveSmallIntegerField(default=0)
    cold = models.PositiveSmallIntegerField(default=0)
    remains = models.PositiveSmallIntegerField(default=0)
    fish = models.PositiveSmallIntegerField(default=0)
    salad = models.PositiveSmallIntegerField(default=0)
    fast = models.PositiveSmallIntegerField(default=0)
    vegetarian = models.PositiveSmallIntegerField(default=0)
    meatloaf = models.PositiveSmallIntegerField(default=0)
    noodles = models.PositiveSmallIntegerField(default=0)
    mushrooms = models.PositiveSmallIntegerField(default=0)
    broccoli = models.PositiveSmallIntegerField(default=0)
    shrimps = models.PositiveSmallIntegerField(default=0)
    zucchini = models.PositiveSmallIntegerField(default=0)
    ham = models.PositiveSmallIntegerField(default=0)
    rice = models.PositiveSmallIntegerField(default=0)
    pizza = models.PositiveSmallIntegerField(default=0)
    fruits = models.PositiveSmallIntegerField(default=0)
    gnocci = models.PositiveSmallIntegerField(default=0)
    spinach = models.PositiveSmallIntegerField(default=0)
    beans = models.PositiveSmallIntegerField(default=0)
    sugar = models.PositiveSmallIntegerField(default=0)
    apples = models.PositiveSmallIntegerField(default=0)
    cauliflower = models.PositiveSmallIntegerField(default=0)
    feta = models.PositiveSmallIntegerField(default=0)
    chicken = models.PositiveSmallIntegerField(default=0)
    eggs = models.PositiveSmallIntegerField(default=0)
    tuna = models.PositiveSmallIntegerField(default=0)
    curd_cheese = models.PositiveSmallIntegerField(default=0)
    lentils = models.PositiveSmallIntegerField(default=0)
    cheese = models.PositiveSmallIntegerField(default=0)
    yeast = models.PositiveSmallIntegerField(default=0)
    sweet_potatoes = models.PositiveSmallIntegerField(default=0)
    sausage = models.PositiveSmallIntegerField(default=0)
    gorgonzola = models.PositiveSmallIntegerField(default=0)
    pineapple = models.PositiveSmallIntegerField(default=0)
    potatoes = models.PositiveSmallIntegerField(default=0)
    dumplings = models.PositiveSmallIntegerField(default=0)
    cabbage = models.PositiveSmallIntegerField(default=0)
    tomatoes = models.PositiveSmallIntegerField(default=0)

class MealSerialize(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id', 'name']
    
    def get_name(self, obj):
        return obj.meal