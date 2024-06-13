import seaborn as sns
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import os
import sqlite3
import google.generativeai as genai


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text
def get_gemini_response2(question2, prompt2, answer):
    model2 = genai.GenerativeModel("gemini-pro")
    response2 = model2.generate_content([prompt2[0], question2, answer])
    return response2.text
def get_gemini_response3(question3, prompt3):
    model3 = genai.GenerativeModel("gemini-pro")
    response3 = model3.generate_content([prompt3[0], question3])
    return response3.text
def get_gemini_chat(question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    return response.text
def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)

    column_names = [description[0] for description in cur.description]

    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows, column_names
def create_sql_db(df):
    connection = sqlite3.connect('GT.db')
    test = pd.read_csv("GT_Sales_Report.csv")
    print("Database Created")
    test.to_sql("GT", connection, if_exists='replace', index=False)
    cursor = connection.cursor()
    data = cursor.execute('''Select * from GT''')
    connection.commit()
    connection.close()
def update_page_and_query_params(new_page):
    st.experimental_set_query_params(page=new_page)
    st.experimental_rerun()


prompt = [
        """
        You are a machine learning engineer in a FMCG firm and are good at performing mathematical calculations and drawing summaries from csv data and generating insights from huge databases and also you are an expert in converting English questions to SQL query!
        Your task is to generate sql queries based on user questions in natural language and make sure to give the correct columns based on the question.     
        I will be providing you with some instructions, based on which you need to convert the prompts written by the user in English to SQL query. Following are the instructions:
        -> The SQl query should not have '''sql at the beginning and ''' at the end.. For example, if SQL code is ```sql SELECT State, SUM(TotalSalesRate) FROM INNOVATION WHERE Brand = '50-50 Jeera' AND State NOT IN ('India','Region') GROUP BY State; ``` . remove ```sql from start and ```  from end.
        -> You have to convert all the Upper Case and Lower Case input into Camel Case and then execute the query.
        -> Brand List: ['50-50 Golmal', '50-50 Jeera', '50-50 Potazoz', 'BC Coffee', 'Butter Rusk', 'Coconut Water', 'Croissant', 'Flavoured Milk', 'GD Harmony', 'Groovy Chips', 'MG Jeera', 'Marble Cake', 'Milk Bikis Classic', 'Muffils', 'Multi Grain', 'NC IMM Herbs', 'NC Protein', 'NC Seed', 'Paneer', 'Plum Cake', 'Puff', 'Richshake', 'Sticks', 'Swiss Roll', 'Treat Jam POP', 'Treat Low Den']. 
        Whenever a user searches or writes any brand, try to match items in the Brand List. Any filter on Brand should be a subset of this list only. Users may misspell some of the brands while asking, try to find its nearest match from the above Brand list and then create a sql query based on that. For example, If I have asked for an analysis of 'bc cofee', then its nearest match in BRAND LIST is 'BC Coffee'. So SQL Code should have something like WHERE Brand = 'BC Coffee' in its final code.
        -> Whenever user wants North analysis,then show the total sales of North1 and North2 states. Question: Show the total sales of north region, SQL Query should be: SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE State IN ('North1', 'North2') 
        -> Whenever user wants South analysis,then show the total sales of South1 and South2 states. Question: Show the total sales of south region, SQL Query should be: SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE State IN ('South1', 'South2')
        -> State List: ['India', 'East', 'Central', 'South1', 'North2', 'West', 'South2', 'North1','West Bengal', 'Sikkim', 'Assam', 'Meghalaya', 'Arunachal Pradesh', 'Tripura','Nagaland', 'Mizoram', 'Manipur', 'Orissa', 'Bihar', 'Jharkhand','Jammu and Kashmir', 'Tamil Nadu', 'Telangana', 'Madhya Pradesh', 'Karnataka','Chattisgarh', 'Chandigarh', 'Seemandhra', 'Uttar Pradesh', 'Maharashtra','Gujarat', 'Goa', 'Dadra and Nagar Hav.', 'Kerala', 'Puducherry','Daman and Diu', 'Rajasthan', 'Delhi', 'Haryana', 'Punjab', 'Himachal Pradesh','Uttaranchal', 'LADAKH']. Whenever user searches or writes any state, try to match it items in State List. Any filter on State should be a subset of this list only. Users may misspell some of the states while asking, try to find its nearest match from the above State list and then create a sql query based on that. For example, IF I have asked for an analysis of 'haryan', then its nearest match in BRAND LIST is 'Haryana'. So SQL Code should have something like WHERE Brand = 'Haryana' in its final code.
        -> Users may spell some words incorrectly, but you should take care while responding to them. If an exact match is found, then it's okay and you can show that result. If an exact match is not found then what you need to do is find the nearest or closest word to the user input and then produce output. For eg, If the user inputs '50-50 Golmaal' or '50-50 golmal', then give results for its nearest match brand, '50-50 Golmal'. Similarly do for rest.
        -> The SQL database has the name INNOVATION which contains the purchasing history of consistent retailers over the years from 2019 to 2024 for various brands and has the following columns listed in the column list below.
        -> Column List: ['Month', 'repeat_L3M', 'UniqueRetCumulative', 'Repeat_last_month','TotalSalesRate', 'TotalPurchaseRate', 'Sales_Quantity_CBB', 'Sales_Quantity_Pkts', 'Sales_Volume_KG', 'ECO', 'PDO', 'Brand', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate', 'Monthly_Consistent_Group_pur_rate', 'Set', 'State', 'Filename']  
        -> Now I will help you understand the meanings and usage of each column one by one:
        -> 'Month' column gives information about the specific data about those retailers history.
        -> 'repeat_L3M' demonstrates the number of trusted retailers who have bought the product at least 4 times in last 3 months.
        -> 'UniqueRetCumulative' demonstrates cumulative unique retailers count on monthly basis.
        -> 'Repeat_last_month' shows count of unique retailers who are consistent from last month.
        -> 'TotalSalesRate' and 'TotalPurchaseRate' are numerical sums for sales happening in those months at that level. Only difference between them is it depends upon which side of the transaction you are on. 'TotalPurchaseRate' is the price for which the retailer buys the product from us. 'TotalSalesRate' is the price at which the retailer sells the product to end user.
        -> 'Sales_Quantity_CBB', 'Sales_Quantity_Pkts' and 'Sales_Volume_KG' are information on different measurement quantities like CBB are number of Boxes, Pkts are number of Packets, Volume_Kg is volume in Mass Kg.
        -> 'ECO' is the number of Unique Retailer.
        -> 'Brand' will give the name of that particular brand.
        -> 'Consistent_Group_Ret' is the number of unique consistent retailers.
        -> 'Consistent_Group_pur_rate' is the sum of their purchase rates.
        -> 'Monthly_Consistent_Group_pur_rate' is the same sum on a monthly basis.
        -> 'Set' will tell us about at which level the information is about, Overall 'India' level' or 'State' level .
        -> 'State' will give more information about this set, and tell the more info for that level id set is India or State.
        ->  Show Sales results in comma separated format and upto two decimal points. 
        -> Whenever I use the word 'Summarize' show the totals of 'Consistent_Group_Ret', 'TotalSalesRate', 'PDO', 'ECO' and 'Consistent_Group_pur_rate' from the table. Also calculate month on month growth and show it in another column. For example, Question: Summarize the data for the month september 2022 for brand 50-50 golmal, SQL Code: SELECT SUM(TotalSalesRate),SUM(Consistent_Group_Ret),SUM(PDO),SUM(Consistent_Group_pur_rate), SUM(ECO) FROM INNOVATION WHERE Brand = '50-50 Golmal' AND Month LIKE '2022-09-01' GROUP BY Month;

        -> If I ask two columns and out of those two columns, one has non-numeric values and one has numeric, then always display non numeric column first and then after that the numeric column.
        -> If I mention sales, always show Sum of TotalSalesRate at that granularity/level.
        -> If I mention any month(mm) with year(yyyy) also, then only check for day 01 month mm and year yyyy, like, yyyy-mm-01 in the Months column. For example, if I ask for total sales for the month of September 2023 or Sept 2023, then check for 2023-09-01 only in the Month column. SQL Code should be like - SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE Month =='2023-09-01' AND Brand = '50-50 Golmal';
        -> If I mention any month(mm) without year, then take sum of that month for all the years from the month column. For example, if I ask total sales for sept or September then find the sum of sales of sept from 2020,2021,2022,2023. SQL Code be like - SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE Month LIKE '____-09-01' AND Brand = '50-50 Golmal';
        -> If any day, month, year is mentioned first convert it into datetime64 format as 'yyyy-mm' and then run the query.
        -> If asked for a particular month take only 1st day of that month like if asked for sept 2023 sql code should have something like - WHERE MONTH LIKE '2023-09-01' and if asked for a particular year take all the months(only first days of each month) of that particular year,for example if asked for 2022, sql should have something like -  WHERE MONTH LIKE '2022-__-01'. If asked for a particular month without mentioning year then search for all the years for that month, for example if I asked for september only, then sql code have something like - WHERE MONTH LIKE '____-09-01';

        -> Only Consistent_Group_Ret should be used to calculate Month on Month growth.

        -> Now, second type of question can be asked to find month on month growth for all the months of over the months. For such cases use below two points to generate a appropriate code. It should not be mixed with the code where user asks for mon on month growth for a particular month.
                    1 -> To calculate month on month growth for all the months, subtract the latest month's Consistent_Group_Ret from previous month's Consistent_Group_Ret and divide by previous month's Consistent_Group_Ret. For example if I asked for month on month growth for all the months , SQL code will be something like SELECT Month, SUM(Consistent_Group_Ret) AS Total_Consistent_Group_Ret, (SUM(Consistent_Group_Ret) - LAG(SUM(Consistent_Group_Ret), 1, 0) OVER (ORDER BY Month))*100 / LAG(SUM(Consistent_Group_Ret), 1, 1) OVER (ORDER BY Month) AS Month_on_Month_Growth FROM INNOVATION GROUP BY Month ORDER BY Month;
                    2 -> To calculate month on month growth for all months for a particular state and brand, subtract the latest month's Consistent_Group_Ret from previous month's Consistent_Group_Ret and divide by previous month's Consistent_Group_Ret and filter out for that state and brand. For example if I asked for month on month growth for only India state and 50-50 golmal brand, SQL code will be something like: SELECT Month, SUM(Consistent_Group_Ret) AS Total_Consistent_Group_Ret, (SUM(Consistent_Group_Ret) - LAG(SUM(Consistent_Group_Ret), 1, 0) OVER (ORDER BY Month))*100 / LAG(SUM(Consistent_Group_Ret), 1, 1) OVER (ORDER BY Month) AS Month_on_Month_Growth FROM INNOVATION WHERE Brand = '50-50 Golmal' AND State = 'India' GROUP BY Month ORDER BY Month;

        -> Whenever I ask for Complete States analysis or Something like show me the sales over the states, always exclude 'India' and 'Region' from the States column and then show. For example, if I want total sales rate for milkshake over the states, sql code should be like this SELECT State ,  SUM(TotalSalesRate) FROM INNOVATION WHERE Brand = 'Milkshake' AND State NOT IN ('India','Region') GROUP BY State;
        -> If a user asks something like difference between total sales or total purchase rate between two months or two brands or two states, first calculate sum of these two months/brands/regions and then take difference between them. For example if I ask for difference between total sales of february 2022 and march 2022 for brands sticks, SQL Code should be like SELECT (SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE month = '2020-02-01' AND brand = 'sticks') - (SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE month = '2020-03-01' AND brand = 'sticks') AS sales_difference;
        -> To calculate profit for a particular state and brand, take the sum of difference of TotalSalesRate by TotalPurchaseRate and then divide the result by sum of TotalPurchaseRate and then multiply the result with 100 and order by month. For example, if I ask for profit of brand '50-50 Golmal' in State 'India' for the month of August 2023, SQL Code should be like something SELECT Month, Brand, (SUM(Sales_rate - TotalPurchaseRate) / SUM(TotalPurchaseRate)) * 100 AS Profit_Margin_Percentage FROM Innovation WHERE Brand = '50-50 Golmal' AND State = 'India' AND Month = '2023-08' GROUP BY Month, Brand;
        -> If I ask for a comparison between two or more brands or states, always compare their TotalSalesRate,if nothing is mentioned by the user. For example, if I ask which brand is better performing - Treat Low Den or BC Coffee or 50-50 Golmal or Milkshake, arrange them in decreasing order of their total sales and then show the name of the top ranked brand in this table with its total sales. Example - Question: which brand is better performing - 'Treat Low Den' or 'BC Coffee' SELECT Brand, SUM(TotalSalesRate) AS Total_Sales_Rate FROM INNOVATION WHERE Brand IN ('Treat Low Den', 'BC Coffee') GROUP BY Brand ORDER BY Total_Sales_Rate DESC LIMIT 1;
        -> If I ask the top performing brand for a particular state or month, then first compare all the brands on the basis of their TotalSalesRate and then show this brand name and its TotalSalesRate.  Example: Question: show me the top performing brand for the month of september 2022. SQL CODE: SELECT Brand, SUM(TotalSalesRate) AS Total_Sales_Rate FROM INNOVATION WHERE Month = '2022-09-01' GROUP BY Brand ORDER BY Total_Sales_Rate DESC LIMIT 1;
        -> If a table has multiple columns out of which there is one one categorical or day-date column and other are numerical quantitative columns, then always show the categorical column at first column, and then numerical columns. Also try to show result columns or user asked columns in the second column.
        -> If I ask for total sales of two or more different brands/regions over the months, then create total_sales_(brand/region) columns for these brands/regions for all the months and show it. Example - Question: show me the sales of brands - milkshake, 50-50 golmal and treat low den over the months. SQL Code: SELECT Month, SUM(CASE WHEN Brand = 'Milkshake' THEN TotalSalesRate ELSE 0 END) AS Milkshake_TotalSalesRate, SUM(CASE WHEN Brand = '50-50 Golmal' THEN TotalSalesRate ELSE 0 END) AS `50-50_Golmal_TotalSalesRate`, SUM(CASE WHEN Brand = 'Treat Low Den' THEN TotalSalesRate ELSE 0 END) AS `Treat_Low_Den_TotalSalesRate` FROM INNOVATION WHERE Brand IN ('Milkshake', '50-50 Golmal', 'Treat Low Den') GROUP BY Month ORDER BY Month;
        -> If I ask total sales of two or more different brands/regions over the months and also which brand/region is best for each month, then create total_sales_(brand/region) columns for these brands/regions for all the months and then create extra column which will show the name of brand/region with highest sale for that month. Example - Question: show me the sales of brands - milkshake, 50-50 golmal and treat low den over the months and also show which brand is best for each month. SQL Code: SELECT Month, SUM(CASE WHEN Brand = 'Milkshake' THEN TotalSalesRate ELSE 0 END) AS Milkshake_TotalSalesRate, SUM(CASE WHEN Brand = '50-50 Golmal' THEN TotalSalesRate ELSE 0 END) AS `50-50_Golmal_TotalSalesRate`, SUM(CASE WHEN Brand = 'Treat Low Den' THEN TotalSalesRate ELSE 0 END) AS `Treat_Low_Den_TotalSalesRate`, (SELECT Brand FROM INNOVATION WHERE MONTH = t1.Month AND TotalSalesRate = (SELECT MAX(TotalSalesRate) FROM INNOVATION WHERE MONTH = t1.Month)) AS Highest_Selling_Brand FROM INNOVATION t1 WHERE Brand IN ('Milkshake', '50-50 Golmal', 'Treat Low Den') GROUP BY Month ORDER BY Month;
        -> If I ask to find months where one of the brand is performing well than the other brand, then first create total_sales_(brand) columns for both these brands for all the months, then create extra column which will show the name of brand/region with highest sale for each month, and then at least filter those months where required month is performing better than the other, Example: Question: during which months brand-milkshake had more total sales than 50-50 golmal. SQL Code: SELECT Month, SUM(CASE WHEN Brand = 'Milkshake' THEN TotalSalesRate ELSE 0 END) AS Milkshake_TotalSalesRate, SUM(CASE WHEN Brand = '50-50 Golmal' THEN TotalSalesRate ELSE 0 END) AS `50-50_Golmal_TotalSalesRate` FROM INNOVATION WHERE Brand IN ('Milkshake', '50-50 Golmal') GROUP BY Month HAVING Milkshake_TotalSalesRate > `50-50_Golmal_TotalSalesRate`;
        -> If no State is mentioned in the user query then always take filter for State = India. For Example, Question: Give summary for Croissant brand for september 2023. SQL CODE: SELECT SUM(TotalSalesRate) AS TotalSales,SUM(Consistent_Group_Ret) AS ConsistentGroupRet,SUM(PDO) AS PDO,SUM(Consistent_Group_pur_rate) AS ConsistentGroupPurRate, SUM(ECO) AS ECO FROM INNOVATION WHERE Brand = 'Croissant' AND State = 'India' AND Month = '2023-09-01' GROUP BY Month;
        -> Always end SQL Code with ; 
        -> also the sql code should not have ``` in beginning and end and sql word in output.

        Take help from these examples and exceptions to understand and then make your own queries
        \n\nFor example,
        -> Example 1 - How many entries of records are present?, the SQL command will be something like this : SELECT COUNT(*) FROM INNOVATION ;
        -> Example 2 - Tell me all the data for brand Croissant, the SQL command will be something like this :  SELECT * FROM INNOVATION where BRAND='Croissant';
        -> Example 3 - Give me data for Swiss Roll Brand for August-2023 Month, the SQL command will be something like this:  SELECT * FROM INNOVATION WHERE Month LIKE '2023-08-__'; 
        -> Example 4 - find difference between total sales of treat low den and bc coffee over the months,the SQL command will be something like this : SELECT Month,(SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE Brand = 'Treat Low Den' AND Month = t1.Month) - (   SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE Brand = 'BC Coffee' AND Month = t1.Month) AS Sales_Difference FROM INNOVATION t1 WHERE Brand IN ('Treat Low Den', 'BC Coffee') GROUP BY Month ORDER BY Month;
        -> Example 5 - Question: Give me consistent retailers for 50-50 Golmal for Oct 23 for India. SQL Code: SELECT State, SUM(Consistent_Group_Ret) FROM INNOVATION WHERE Brand = '50-50 Golmal' AND State = 'India' AND Month = '2023-10-01' GROUP BY State;
        -> Example 6 - Question: Summarize the data for brand milkshake in the state haryana over the months, SQL Code: SELECT Month, SUM(TotalSalesRate) AS Milkshake_TotalSalesRate, SUM(Consistent_Group_Ret) AS Consistent_Group_Ret, SUM(PDO) AS PDO, SUM(Consistent_Group_pur_rate) AS Consistent_Group_Pur_Rate, SUM(ECO) AS ECO FROM INNOVATION WHERE Brand = 'Milkshake' AND State = 'Haryana' GROUP BY Month ORDER BY Month;


        """

    ]
prompt2 = [
    """
    You are an expert in understanding English Language and presenting it in a very formal professional way. A question will be asked to you with its result. You need to present this result in a professional form to the user. 
    If the result is a number or a string or not in data frame format then simply paraphrase the question and adjust the result in a single sentence. For example, If the user asks - Show me the total sales for 50-50 Golmal in the month of August 2023 and result provided is 234567, then you should reply something like "Total sales for 50-50 Golmal in the month of August 2023 accounted to 2,34,567 rupees.
    If the result passed is:"Dataframe", simply just paraphrase the question and tell that the required dataset is represented below, but don't show any dataframe from your side. I repeat, do NOT show any table or dataset or dataframe from your side, just paraphrase the question and say the answer is presented below. For example, if a user asks to show me the total sales for unique brands, simply write " According to the data Total sales for each of the unique brands are shown below." 
    Show currency values in comma separated format.
    Show all decimal values until only 2 decimal points and don't change any Integer value.
    Whenever "summarize" is used in the question, the answer will contain 5 parameters - Total Sales, Consistent Group Retailers, PDO, Consistent Group Purchase Rate and ECO, that too, in the same order as I wrote. So answer accordingly.
    Whenever user is asking for any type of 'contribution', always show results with percentage sign. Don't do any calculation from your side.
    
    Example1: Question - Give me consistent retailers for 50-50 Golmal for Oct 23 for India. Answer passed-[(India, 83237.0)].Your Output: Consistent retailers for 50-50 Golmal in India for Oct 23 accounted for 83,237
    Example2: Question - Give me a brand which has the most consistent retailers and sales in India in Oct-23. Answer passed-[('50-50 Golmal', 83237.0, 107051826.143)]. Your Output: Brand 50-50 Golmal has the most consistent retailers and sales in India in Oct-23 with 83,237 consistent retailers and total sales revenue of 107,051,826.14 rupees.
    Example3: Question - summarize the data for the month september 2022 for brand 50-50 golmal. Answer Passed - [(163108179.76, 55497.0, 64219.050409263284, 162860985.63, 292185)]. Your Output: Sales revenue for brand 50-50 Golmal for the month of September 2022 was 16.31 crores with 55,497 consistent retailers and 64,219.05 total PDO. Total Consistent Group Purchase Rate recorded for the brand was 16.28 crores with an ECO total of 2,92,185.
    Example4: Question - Give the month on month growth of croissant brand for oct 22 to nov 22. Answer Passed -  [('2022-11-01', 0.6967381480568564)]. Your Output: The month on month growth for Croissant brand from Oct'22 to Nov'22 was 0.69%
    Please do not round off numbers ffs. Example - Do not round off 5,18,46,099 to 5,00,00,000 or 5 lakh rupees. Just keep it as 5,18,46,099.

    """
]
prompt3 = [
    """
    You are an expert in understanding English Language and excellent model who will help me to build a perfect data visualization model.
    User will ask a question like show me visualization for a particular type of graph and we will have to use user's question to find what type of chart or graph he wants as well as between which variables the chart should be plotted.
    --> So first thing we will look into it will be type of chart user is demanding for. There can be 7 types of charts, which is presented in this - Chart_list : ['Table','Line Chart','Pie Chart','Bar Chart','Scatter Plot','Heat Map','Pair Plot']. Whenever user asks for any plot, search in this chart list only. User may misspell some chart's name or use different cases, your job is to adjust and search for nearest chart match in this list as store it as Variable "Selected Chart". So for example, if user asks to draw a bar chart for sales of 50-50 Golmal and Croissant in the states Jharkhand and Karnataka. So search bar chart in chart list and store "Selected Chart" as 'Bar Chart'.
    --> Second thing will be the brands user has selected for analysis. this is to be searched in the list - Brands: ['50-50 Golmal', '50-50 Jeera', '50-50 Potazoz', '50-50 Potazoz_Chilli', '50-50 Potazoz_Mint', '50-50 Potazoz_Plain', 'BC Coffee', 'Britannia Wafers', 'Butter Rusk', 'Cheese', 'Coconut Water', 'Croissant', 'Croissant_Mixed Fruit', 'Croissant_Orange', 'Flavoured Milk', 'Flavoured Milk_Badam', 'GD Harmony', 'Groovy Chips', 'Groovy Chips_Masala', 'Groovy Chips_Pudina', 'Groovy Chips_Tomato', 'MG Jeera', 'Marble Cake', 'Marble Cake_Choco Vanilla', 'Marble Cake_Red Velvet', 'Milk Bikis Classic', 'Muffils', 'Multi Grain', 'NC IMM Herbs', 'NC Protein', 'NC Seed', 'Paneer', 'Plum Cake', 'Puff', 'Puff_Cheesy Tubes', 'Puff_Cheesy Tubes_Onion', 'Puff_Cheesy Tubes_Tomato', 'Puff_Tic Tac Toe', 'Puff_Tic Tac Toe_Masala', 'Puff_Tic Tac Toe_Tomato', 'Pure Magic Choco Lush', 'Pure Magic Choco Lush_75g', 'Pure Magic Choco Lush_12g', 'Richshake', 'Richshake_Cold Coffee', 'Sticks', 'Sticks_Masala', 'Sticks_Tomato', 'Swiss Roll', 'Swiss Roll_Big', 'Swiss Roll_Triple Choco', 'Time Pass', 'Treat Jam POP', 'Treat Low Den', 'Treat Low Den_27G', 'Winkin Milkshake']. Whatever brands user may select, store them in a list called Selected_brands. Like if user asks to draw a bar chart for sales of 50-50 Golmal and Croissant in the states Jharkhand and Karnataka, Then Selected_brands will be : ['50-50 Golmal','Croissant'].
    --> Third thing will be the states user have selected and this is to be searched in the list States: - ['India', 'East', 'Central', 'South1', 'North2', 'West', 'South2', 'North1', 'West Bengal', 'Sikkim', 'Assam', 'Meghalaya', 'Arunachal Pradesh', 'Tripura', 'Nagaland', 'Mizoram', 'Manipur', 'Orissa', 'Bihar', 'Jharkhand', 'Jammu and Kashmir', 'Tamil Nadu', 'Telangana', 'Madhya Pradesh', 'Karnataka', 'Chattisgarh', 'Chandigarh', 'Seemandhra', 'Uttar Pradesh', 'Maharashtra', 'Gujarat', 'Goa', 'Dadra and Nagar Hav.', 'Kerala', 'Puducherry', 'Daman and Diu', 'Rajasthan', 'Delhi', 'Haryana', 'Punjab', 'Himachal Pradesh', 'Uttaranchal', 'LADAKH']. Whatever states user may select, store them in a list called Selected_states. Like if user asks to draw a bar chart for sales of 50-50 Golmal and Croissant in the states Jharkhand and Karnataka, Then Selected_states will be : ['Jharkhand','Karnataka']
    --> Fourth thing which user can ask for is the aggregated value onto which the whole analysis will work upon. It has to be searched in the list num_columns = ['TotalSalesRate', 'ECO', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate', 'PDO']. Whatever aggregate user may select,match with the nearest aggregate in the list and store them in another list called Value. Like if user asks to draw a bar chart for sales of 50-50 Golmal and Croissant in the states Jharkhand and Karnataka, Then Value will be : ['TotalSalesRate']
    Now pass these variables in seperate nested list format. Like if user asks to draw a bar chart for sales of 50-50 Golmal and Croissant in the states Jharkhand and Karnataka, then pass it like this: [Selected Chart: 'Bar Chart']; [Selected Brands: ['50-50 Golmal', 'Croissant']]; [Selected States: ['Jharkhand', 'Karnataka']]; [Value : ['TotalSalesRate']]
    """
]
prompt4 = ["""
        You are a machine learning engineer in a FMCG firm and are good at performing mathematical calculations and drawing summaries from csv data and generating insights from huge databases and also you are an expert in converting English questions to SQL query!
        Your task is to generate sql queries based on user questions in natural language and make sure to give the correct columns based on the question. Database upon which code should be made is also paased. Like in this case "GT" is database name, and you should generate code for that table only and forget all previous codes from another database.   
        I will be providing you with some instructions, based on which you need to convert the prompts written by the user in English to SQL query. Following are the instructions:
        The SQl query should NOT have '''sql at the beginning and ''' at the end.. For example, if SQL code is  ```sql SELECT * FROM GT```. remove ```sql from start and ```  from end. Update it to: SELECT * FROM GT
        -> Every Sql code has to be generated from only these tables: ['GT']
        -> You have to convert all the Upper Case and Lower Case input into Camel Case and then execute the query.
        -> The data contains the following column names as mentioned in column list Column list: ['Month', 'Region', 'Total_Sales', 'GT_Sales', 'KATS_Sales', 'Year', 'Month-Year','LYTS', 'LYGTS', 'LYKS']
        -> The region column contains one of the following regions mentioned in region list. There are chances that the user may spell the region incorrectly in that case give the value of the closest spelled region. Region List: [‘North 1’, ‘North 2’, ‘Çentral’, ’West’ ,’East’, ‘South 1’, ‘South 2’ ]
        -> The year column contains the Year of that specific sales.
        -> The month column contains the specific month of that sales. Current month means latest or last month ongoing in months column.
        -> Region Column specifies the place for that sales.
        -> If the user asks Total Sales of current month, look into the 'Total_Sales' column, Total Sales is the Total Sales of Particular Region at Particular Year of Current Month.
        -> If the user asks GT_Sales, look into the 'GT_Sales' column, GT_Sales is the GT_Sales of Particular Region at Particular Year of Current Month. For Example, What is the GT_Sales for December 2023 for central region, the SQL Query would be like: SELECT GT_Sales FROM GT WHERE Month = 'Dec' AND Region = 'Central' AND Year = 2023;
        -> If the user asks KATS_Sales, look into the 'KATS_Sales' column, KATS_Sales is the KATS_Sales of Particular Region at Particular Year of Current Month. For Example, What is the KATS_Sales for December 2023 for central region, the SQL Query would be like: SELECT KATS_Sales FROM GT WHERE Month = 'Dec' AND Region = 'Central' AND Year = 2023;
        -> If the user asks ‘Total Sales of last year’ go to 'LYTS' column, LYTS is the Total_Sales of Particular Region of Last Year Current Month.
        -> If the user asks 'GT Sales of last year' go to 'LYGTS' column, LYGTS is the GT_Sales of Particular Region of Last Year Current Month.
        -> If the user asks 'KATS Sales of last year' look into the 'LYKS' column it is the KATS_Sales of Particular Region of Last Year Current Month.
        -> If the user asks GT contribution to total for any specific month, year and Region; take GT_Sales and divide it by Total_Sales and then multiply it by 100 for that specific region month, year and Region. For example, if user asks GT contribution to total for June 2022 in Central region, SQL Code: SELECT Month, Year, Region, SUM(GT_Sales)*100 / SUM(Total_Sales) AS GT_Contribution FROM GT WHERE Month = 'Jun' AND Year = 2022 AND Region = 'Central’ GROUP BY Month, Year, Region;
        -> If the user asks KATS contribution to total for any specific month, year and Region; take KATS_Sales and divide it by Total_Sales and then multiply it by 100 for that specific region month, year and Region. For example, if user asks KATs contribution to total for June 2022 in Central region, SQL Code:  SELECT Month, Year, Region, SUM(KATS_Sales)*100 / SUM(Total_Sales) AS KATS_Contribution FROM GT WHERE Month = 'Jun' AND Year = 2022 AND Region = 'Central’ GROUP BY Month, Year, Region;
        -> If the user asks KATS contribution to GT for any specific month, year and Region; take KATS_Sales and divide it by GT_Sales and then multiply it by 100 for that specific region month, year and Region. For example, if user asks KATs contribution to GT for June 2022 in Central region, SQL Code:  SELECT Month, Year, Region, SUM(KATS_Sales)*100 / SUM(GT_Sales) AS KATS_Contribution_GT FROM GT WHERE Month = 'Jun' AND Year = 2022 AND Region = 'Central’ GROUP BY Month, Year, Region;
        -> If the user asks GT contribution to total for any specific month and year and region is not specified, take the sum of GT_Sales for every region and then divide it by sum of Total_Sales for every region for that specific month and year. For Example, What is the GT Contribution to total for Nov 2023, the SQL Query would be like: SELECT Month, Year, SUM(GT_Sales)*100 / SUM(Total_Sales) AS GT_Contribution FROM GT WHERE Month = 'Nov' AND Year = ‘2023’ GROUP BY Month, Year;
        -> If the user asks KATS contribution to total for any specific month and year and region is not specified, take the sum of KATS_Sales for every region and then divide it by sum of Total_Sales for every region for that specific month and year. For Example, What is the KATS Contribution to total for Jan 2022, the SQL Query would be like: SELECT Month, Year, SUM(KATS_Sales)*100 / SUM(Total_Sales) AS KATS_Contribution FROM GT WHERE Month = 'Jan' AND Year = ‘2022’ GROUP BY Month, Year;
        -> If the user asks KATS contribution to GT for any specific month and year and region is not specified, take the sum of KATS_Sales for every region and then divide it by sum of GT_Sales for every region for that specific month and year. For Example, What is the KATS Contribution to GT for Jan 2022, the SQL Query would be like: SELECT Month, Year, SUM(KATS_Sales)*100 / SUM(GT_Sales) AS KATS_Contribution_GT FROM GT WHERE Month = 'Jan' AND Year = ‘2022’ GROUP BY Month, Year;
        -> If the user asks for increament or decreament from last year for any of the parameters like [Total Sales,GT Sales, KATS Sales, GT contribution to total, KATS contribution to total,KATS contribution to GT] then first calculate this parameters as per the above definitions/ formulas and then compare it with LYTS if comparison is for Total Sales, LYGTS if comparison is for GT Sales, LYKS if comparioson is for KATS Sales.
        -> There can be two types for increament/decreament questions: Understand them with these examples:
            1-> When absolute values of change is asked. Question-> What is the chnage of Total Sales from last year, SQL Code: 
            2-> When Percentage change is asked. Question-> What is the percentage change of Total Sales from last year, SQL Code: 
        -> If the user asks Total Sales without specifying any region take the sum of all regions Total Sales for a specific month and year. For Example, What is the Total Sales in December 2023, SQL query would be like: SELECT SUM(Total_Sales) AS Total_Sales_December_2023 FROM GT WHERE Month = 'Dec' AND Year = 2023;
        I am saying this again. The SQl query should NOT have '''sql at the beginning and ''' at the end.If it has it, please REMOVE it. For example, if SQL code is  ```sql SELECT * FROM GT```. remove ```sql from start and ```  from end. Update it to: SELECT * FROM GT
        
        
        Take help from this Examples:
        1.Question-> What is the total sales for jan 2024 . SQL Code: SELECT SUM(Total_Sales) AS Total_Sales_Jan_2024 FROM GT WHERE Month = 'Jan' AND Year = 2024
        2.Question-> What are the total sales for each region for December 2023, SQL Code: SELECT Region, SUM(Total_Sales) AS Total_Sales_December_2023 GT WHERE Month = 'Dec' AND Year = 2023 GROUP BY Region;
        """]
prompt_kats = ["""
        You are a machine learning engineer in a FMCG firm and are good at performing mathematical calculations and drawing summaries from csv data and generating insights from huge databases and also you are an expert in converting English questions to SQL query!
        Your task is to generate sql queries based on user questions in natural language and make sure to give the correct columns based on the question. Database upon which code should be made is also paased. Like in this case "GT" is database name, and you should generate code for that table only and forget all previous codes from another database.   
        I will be providing you with some instructions, based on which you need to convert the prompts written by the user in English to SQL query. Following are the instructions:
        The SQl query should NOT have '''sql at the beginning and ''' at the end.. For example, if SQL code is  ```sql SELECT * FROM GT```. remove ```sql from start and ```  from end. Update it to: SELECT * FROM GT
        -> Every Sql code has to be generated from only these tables: ['KATS']
        -> You have to convert all the Upper Case and Lower Case input into Camel Case and then execute the query.
        -> The data contains the following column names as mentioned in column list Column list: ['Retailer UID', 'Child UID', 'Retailer Name', 'First Name', 'Last Name', 'Contact No', 'AW Code', 'AW Name', 'Region', 'T 35', 'SOM', 'SOM Name', 'ASM', 'ASE', 'Final Tier', 'Final ULPO Target', 'Ghee Final Value Target', 'Feb-24', 'Nov-23 MTD', 'Dec-23 MTD', 'Jan-24 MTD', 'Feb-24 MTD', 'LYMTD', 'SSG Check', 'SLY', 'Seq%', 'L3M Seq%', 'MSL QUL', 'On Track', 'Apr-23', 'May-23', 'Jun-23', 'Jul-23', 'Aug-23', 'Sep-23', 'Apr-22', 'May-22', 'Jun-22', 'Jul-22', 'Aug-22', 'Sep-22', 'Oct-22', 'Nov-22', 'Dec-22', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'May-23', 'Jun-23', 'Jul-23', 'Aug-23', 'Sep-23', 'Oct-23', 'Nov-23', 'Dec-23', 'FOB LM', 'FOB LMTD', 'FOB MTD', 'FOB Gap', 'Aug-23', 'Sep-23', 'Jan-24', 'LMTD', 'MTD', 'Jun-23', 'Jul-23', 'Aug-23', 'Growth Status', 'Unbilled Check', 'Customer Facing', 'Total Facing', 'SOS%', 'Degrowing KATs']
        -> The region column contains one of the following regions mentioned in region list. There are chances that the user may spell the region incorrectly in that case give the value of the closest spelled region. Region List: [‘North 1’, ‘North 2’, ‘Çentral’, ’West’ ,’East’, ‘South 1’, ‘South 2’ ]
        -> The year column contains the Year of that specific sales.
        -> The month column contains the specific month of that sales. Current month means latest or last month ongoing in months column.
        -> Region Column specifies the place for that sales.
        -> If the user asks Total Sales of current month, look into the 'Total_Sales' column, Total Sales is the Total Sales of Particular Region at Particular Year of Current Month.
        -> If the user asks GT_Sales, look into the 'GT_Sales' column, GT_Sales is the GT_Sales of Particular Region at Particular Year of Current Month. For Example, What is the GT_Sales for December 2023 for central region, the SQL Query would be like: SELECT GT_Sales FROM GT WHERE Month = 'Dec' AND Region = 'Central' AND Year = 2023;
        -> If the user asks KATS_Sales, look into the 'KATS_Sales' column, KATS_Sales is the KATS_Sales of Particular Region at Particular Year of Current Month. For Example, What is the KATS_Sales for December 2023 for central region, the SQL Query would be like: SELECT KATS_Sales FROM GT WHERE Month = 'Dec' AND Region = 'Central' AND Year = 2023;
        -> If the user asks ‘Total Sales of last year’ go to 'LYTS' column, LYTS is the Total_Sales of Particular Region of Last Year Current Month.
        -> If the user asks 'GT Sales of last year' go to 'LYGTS' column, LYGTS is the GT_Sales of Particular Region of Last Year Current Month.
        -> If the user asks 'KATS Sales of last year' look into the 'LYKS' column it is the KATS_Sales of Particular Region of Last Year Current Month.
        -> If the user asks GT contribution to total for any specific month and year, take GT_Sales and divide it by Total_Sales and then multiply it by 100 for that specific region month and year. SELECT Month, Year, Region, SUM(GT_Sales) / SUM(Total_Sales) AS GT_Contribution FROM GT WHERE Month = 'Jun' AND Year = 2022 AND Region = 'Central’ GROUP BY Month, Year, Region;
        -> If the user asks KATS contribution to total for any specific month and year, take KATS_Sales and divide it by Total_Sales and then multiply it by 100 for that specific region month and year. SELECT Month, Year, Region, SUM(KATS_Sales) / SUM(Total_Sales) AS KATS_Contribution FROM GT WHERE Month = 'Jun' AND Year = 2022 AND Region = 'Central’ GROUP BY Month, Year, Region;
        -> If the user asks GT contribution to total for any specific month and year and region is not specified, take the sum of GT_Sales for every region and then divide it by sum of Total_Sales for every region for that specific month and year. For Example, What is the GT Contribution for Nov 2023, the SQL Query would be like: SELECT Month, Year, SUM(GT_Sales) / SUM(Total_Sales) AS GT_Contribution FROM GT WHERE Month = 'Nov' AND Year = ‘2023’ GROUP BY Month, Year;
        -> If the user asks KATS contribution to total for any specific month and year and region is not specified, take the sum of KATS_Sales for every region and then divide it by sum of Total_Sales for every region for that specific month and year. For Example, What is the KATS Contribution for Jan 2022, the SQL Query would be like: SELECT Month, Year, SUM(KATS_Sales) / SUM(Total_Sales) AS KATS_Contribution FROM GT WHERE Month = 'Jan' AND Year = ‘2022’ GROUP BY Month, Year;
        -> If the user asks Total Sales without specifying any region take the sum of all regions Total Sales for a specific month and year. For Example, What is the Total Sales in December 2023, SQL query would be like: SELECT Region, SUM(Total_Sales) AS Total_Sales_December_2023 FROM GT WHERE Month = 'Dec' AND Year = 2023 GROUP BY Region;
        I am saying this again. The SQl query should NOT have '''sql at the beginning and ''' at the end.If it has it, please REMOVE it. For example, if SQL code is  ```sql SELECT * FROM GT```. remove ```sql from start and ```  from end. Update it to: SELECT * FROM GT

        """]
def brand_df_single(df):
    brand_df = df.copy()
    brands = brand_df['Brand'].dropna().unique().tolist()
    brands.sort()
    brands.insert(0, 'All')
    selected_brand = st.selectbox("Select brands", brands)
    if selected_brand != 'All':
        temp_df = brand_df[brand_df['Brand'] == selected_brand]
        return temp_df
    else:
        return brand_df
def state_df_single(df):
    state_df = df.copy()
    states = df['State'].dropna().unique().tolist()
    states.sort()
    states.insert(0, 'All')
    selected_state = st.selectbox("Select states", states)
    if selected_state != 'All':
        temp_df = state_df[state_df['State'] == selected_state]
        return temp_df
    else:
        return state_df
def filtered_df2(df):
    col1, col2 = st.columns(2)
    with col1:
        brand_df = brand_df_single(df)
    with col2:
        state_df = state_df_single(brand_df) if len(brand_df) > 0 else state_df_single(df)
    if (len(brand_df) == 0 | len(state_df) == 0):
        final_df = df
    elif len(state_df) == 0:
        final_df = brand_df
    else:
        final_df = state_df
    return final_df
def brand_df_multi(df,brands):
    brand_df = df.copy()
    # brands = brand_df['Brand'].dropna().unique().tolist()
    # brands.sort()
    # brands.insert(0, 'All')
    # selected_brand = st.multiselect("Select brands", brands)
    if brands != 'All':
        temp_df = brand_df[brand_df['Brand'].isin(brands)]
        return temp_df
    else:
        return brand_df
def state_df_multi(df,states):
    state_df = df.copy()
    # states = df['State'].dropna().unique().tolist()
    # states.sort()
    # states.insert(0, 'All')
    # selected_state = st.multiselect("Select states", states)
    if states != 'All':
        temp_df = state_df[state_df['State'].isin(states)]
        return temp_df
    else:
        return state_df
def filtered_df(df,brands,states):
    col1, col2 = st.columns(2)
    with col1:
        brand_df = brand_df_multi(df,brands)
    with col2:
        state_df = state_df_multi(brand_df,states) if len(brand_df) > 0 else state_df_multi(df,states)

    if (len(brand_df) == 0 | len(state_df) == 0):
        final_df = df
    elif len(state_df) == 0:
        final_df = brand_df
    else:
        final_df = state_df
    return final_df
def create_pie_chart(data, category_column, numerical_column, selected_categories):
    fig, ax = plt.subplots(figsize=(20, 20))
    filtered_data = data[data[category_column].isin(selected_categories)]
    pie_data = filtered_data.groupby(category_column)[numerical_column].sum()
    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 30})
    st.pyplot(fig)
def df_maker(df):
    df = df[['Month', 'State', 'Brand', 'TotalSalesRate', 'ECO', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate',
             'PDO']]
    df['Month'] = pd.to_datetime(df['Month'], format='%d-%m-%Y')
    df['Year'] = df['Month'].dt.year
    df['Month_no.'] = df['Month'].dt.month
    df['Month_Year'] = df['Month'].dt.strftime('%b-%y')
    df = df.sort_values(by=['Year', 'Month_no.'])
    month_year = df['Month_Year'].dropna().unique().tolist()
    slider_month = st.select_slider("Pick a Month-year", month_year)
    df = df[['Year', 'Month_no.', 'Month_Year', 'State', 'Brand', 'TotalSalesRate', 'ECO', 'Consistent_Group_Ret',
             'Consistent_Group_pur_rate', 'PDO']]
    df_ss = df[df['Month_Year'] == slider_month][['Year', 'Month_no.']].drop_duplicates()
    row_values_iloc = df_ss.iloc[0].values
    year = row_values_iloc[0]
    month = row_values_iloc[1]
    df = df[(df['Year'] >= year)]
    df = df[(df['Year'] > year) | (df['Month_no.'] >= month)]
    return df