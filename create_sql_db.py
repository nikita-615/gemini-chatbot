import sqlite3
import pandas as pd

# Your existing code to create the 'Innovation' table
connection = sqlite3.connect('innovation.db')
# test = pd.read_excel("Innovation_24.xlsx")
# brand_list = ['50-50 Golmal', '50-50 Jeera', '50-50 Potazoz', 'BC Coffee', 'Butter Rusk', 'Coconut Water', 'Croissant', 'Flavoured Milk', 'GD Harmony', 'Groovy Chips', 'MG Jeera', 'Marble Cake', 'Milk Bikis Classic', 'Muffils', 'Multi Grain', 'NC IMM Herbs', 'NC Protein', 'NC Seed', 'Paneer', 'Plum Cake', 'Puff', 'Richshake', 'Sticks', 'Swiss Roll', 'Treat Jam POP', 'Treat Low Den','Winkin Milkshake']
# test = test[test["Brand"].isin(brand_list)]
# col_list = test.columns
# col_list = [x.strip() for x in col_list]
# test.columns = col_list
# test["Month"] = pd.to_datetime(test["Month"])
# test["Month"] = test["Month"].dt.date
# print("Database Created")
# test.to_sql("Innovation", connection, if_exists='replace', index=False)

cursor = connection.cursor()
data = cursor.execute('''SELECT DISTINCT(MONTH) FROM INNOVATION WHERE Brand = 'Treat Jam POP' AND State = 'Gujarat';''')
# SELECT SUM(TotalSalesRate) AS Total_Sales_Rate FROM INNOVATION WHERE Brand = 'Treat Jam POP' AND State = 'Kerala' AND Month = '2023-09-01';
for row in data:
    print(row)

connection.commit()
connection.close()