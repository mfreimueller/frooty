import collections.abc
import json
import sys

if len(sys.argv) < 4:
    print("USAGE: python importer.py FOOD_DATA.CSV CATEGORIES.JSON OUT.CSV")
    exit(1)

foodPath = sys.argv[1]
jsonPath = sys.argv[2]
csvPath = sys.argv[3]

foodFile = open(foodPath, "r")

jsonFile = open(jsonPath, "r")
foods = json.load(jsonFile)
jsonFile.close()

# first we want to read all possible values from the JSON
# to add the corresponding headers

types = { type.lower() for meal in foods.values() for type in meal.get("type", []) }
ingredients = { ingredient.lower() for meal in foods.values() for ingredient in meal.get("ingredients", []) }

template = {
    "meal": "0",
    "complexity": "0",
    # "weekday": "0"
}

for type in types:
    template[type] = "0"

for ingredient in ingredients:
    template[ingredient] = "0"

# next we create the templates for the categories

categories = []
for name in foods.keys():
    meal = foods[name]

    category = template.copy()
    category["meal"] = name
    category["complexity"] = str(meal["complexity"])
    
    for types in meal.get("type", []):
        category[types] = "1"

    for ingredient in meal.get("ingredients", []):
        category[ingredient] = "1"
    
    categories.append(category)

# finally we iterate over our food csv file and write the lines

csvFile = open(csvPath, "w")
csvFile.write(",".join(template.keys()) + "\n")

foodFile.readline() # skip the header
for line in foodFile:
    meals_of_week = line.split(",")

    for idx, meal in enumerate(meals_of_week):
        serialized = [category for category in categories if category["meal"] == meal.strip()][0].copy()

        # serialized["weekday"] = idx
        csvFile.write(",".join(list(serialized.values())) + "\n")

foodFile.close()
csvFile.close()