import sys
import sqlite3

if len(sys.argv) < 3:
    print("USAGE: python csv_to_sqlite.py CSV_PATH SQLITE_PATH")
    exit(1)

csvPath = sys.argv[1]
sqlitePath = sys.argv[2]

csv = open(csvPath, "r")
conn = sqlite3.connect(sqlitePath)

csv.readline() # skip header

# read csv file line by line and insert into SQLite file
for line in csv:
    first_separator_idx = line.find(",")
    meal_name = line[:first_separator_idx]
    flags = line[first_separator_idx + 1:]

    sql = "INSERT INTO planner_meal (meal,complexity,soup,takeaway," \
            "sweet,meat,cold,remains,fish,salad,fast,vegetarian,meatloaf," \
            "noodles,mushrooms,broccoli,shrimps,zucchini,ham,rice,pizza,fruits," \
            "gnocci,spinach,beans,sugar,apples,cauliflower,feta,chicken,eggs,tuna," \
            "curd_cheese,lentils,cheese,yeast,sweet_potatoes,sausage,gorgonzola," \
            "pineapple,potatoes,dumplings,cabbage,tomatoes) VALUES ('" + meal_name + "'," + flags + ")"
    
    # because this script is for the initial population process of the db, we don't have
    # to use prepared statements etc.
    conn.execute(sql)

conn.commit()

conn.close()
csv.close()