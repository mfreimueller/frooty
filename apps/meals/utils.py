from .models import Meal

def copy_meal_to(source: Meal, destination: Meal) -> Meal:
    destination.meal = source.meal
    destination.complexity = source.complexity
    destination.soup  = source.soup
    destination.takeaway = source.takeaway
    destination.sweet = source.sweet
    destination.meat = source.meat
    destination.cold = source.cold
    destination.remains = source.remains
    destination.fish = source.fish
    destination.salad = source.salad
    destination.fast = source.fast
    destination.vegetarian = source.vegetarian
    destination.meatloaf = source.meatloaf
    destination.noodles = source.noodles
    destination.mushrooms = source.mushrooms
    destination.broccoli = source.broccoli
    destination.shrimps = source.shrimps
    destination.zucchini = source.zucchini
    destination.ham = source.ham
    destination.rice = source.rice
    destination.pizza = source.pizza
    destination.fruits = source.fruits
    destination.gnocci = source.gnocci
    destination.spinach = source.spinach
    destination.beans = source.beans
    destination.sugar = source.sugar
    destination.apples = source.apples
    destination.cauliflower = source.cauliflower
    destination.feta = source.feta
    destination.chicken = source.chicken
    destination.eggs = source.eggs
    destination.tuna = source.tuna
    destination.curd_cheese = source.curd_cheese
    destination.lentils = source.lentils
    destination.cheese = source.cheese
    destination.yeast = source.yeast
    destination.sweet_potatoes = source.sweet_potatoes 
    destination.sausage = source.sausage
    destination.gorgonzola = source.gorgonzola
    destination.pineapple = source.pineapple
    destination.potatoes = source.potatoes
    destination.dumplings = source.dumplings
    destination.cabbage = source.cabbage
    destination.tomatoes = source.tomatoes

    return destination