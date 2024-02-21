from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import numpy as np


col1,col3=st.sidebar.columns([6,3])
with col1:
    st.image('https://www.britannia.co.in/_next/image?url=https%3A%2F%2Fwww.britannia.co.in%2Fdata%2FBritannia_Logo_fcce3225c0.png&w=1080&q=100')
# with col2:
#     st.image('https://www.pngall.com/wp-content/uploads/5/Vertical-Line-PNG-High-Quality-Image.png')
with col3:
    st.image('https://i.imgur.com/IsxqyCy.png')

st.sidebar.title("#AskBritInsightSphere💬")
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Consistent','KATs','Control Tower')
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(question,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0],question])
    return response.text
def get_gemini_response2(question2,prompt2,answer):
    model2 = genai.GenerativeModel("gemini-pro")
    response2 = model2.generate_content([prompt2[0],question2,answer])
    return response2.text
def get_gemini_response3(question3,prompt3,answer3):
    model3 = genai.GenerativeModel("gemini-pro")
    response3 = model3.generate_content([prompt3[0],question3,answer3])
    return response3.text
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)

    column_names = [description[0] for description in cur.description]

    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows, column_names
def update_page_and_query_params(new_page):
    st.experimental_set_query_params(page=new_page)
    st.experimental_rerun()


if user_menu == 'KATs':
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sales = np.random.randint(10000, 50000, size=len(months))
    df = pd.DataFrame({'Month': months,'Sales': sales})
    prompt3 = [
        """
        You are already provided with a pandas Dataframe - df in answer.You don't need to create one. just analyse this table in line chart where x column will be months and y column will be sales. do it in streamlit codes.
        """
    ]
    response3 = get_gemini_response3("", prompt3,'')

if user_menu=='Consistent':

    prompt=[
        """
        You are a machine learning engineer in a FMCG firm and are good at performing mathematical calculations and drawing summaries from csv data and generating insights from huge databases and also you are an expert in converting English questions to SQL query!
        Your task is to generate sql queries based on user questions in natural language and make sure to give the correct columns based on the question.     
        I will be providing you with some instructions, based on which you need to convert the prompts written by the user in English to SQL query. Following are the instructions:
        -> The SQl query should not have '''sql at the beginning and ''' at the end.. For example, if SQL code is ```sql SELECT State, SUM(TotalSalesRate) FROM INNOVATION WHERE Brand = '50-50 Jeera' AND State NOT IN ('India','Region') GROUP BY State; ``` . remove ```sql from start and ```  from end.
        -> You have to convert all the Upper Case and Lower Case input into Camel Case and then execute the query.
        -> Brand List: ['50-50 Golmal', '50-50 Jeera', '50-50 Potazoz', 'BC Coffee', 'Butter Rusk', 'Coconut Water', 'Croissant', 'Flavoured Milk', 'GD Harmony', 'Groovy Chips', 'MG Jeera', 'Marble Cake', 'Milkshake', 'Milk Bikis Classic', 'Muffils', 'Multi Grain', 'NC IMM Herbs', 'NC Protein', 'NC Seed', 'Paneer', 'Plum Cake', 'Puff', 'Treat Jam POP', 'Richshake', 'Sticks', 'Swiss Roll', 'Treat Low Den']. Whenever a user searches or writes any brand, try to match items in the Brand List. Any filter on Brand should be a subset of this list only. Users may misspell some of the brands while asking, try to find its nearest match from the above Brand list and then create a sql query based on that. For example, IF I have asked for an analysis of 'bc cofee', then its nearest match in BRAND LIST is 'BC Coffee'. So SQL Code should have something like WHERE Brand = 'BC Coffee' in its final code.
        -> State List: ['India', 'West Bengal', 'Sikkim', 'BT', 'Assam', 'Meghalaya', 'Arunachal Pradesh', 'Tripura', 'Nagaland', 'Mizoram', 'Manipur', 'Orissa', 'Bihar', 'Jharkhand', 'Jammu and Kashmir', 'Tamil Nadu', 'Telangana', 'Madhya Pradesh', 'Karnataka', 'Chattisgarh', 'Chandigarh', 'Seemandhra', 'Uttar Pradesh', 'Maharashtra', 'TG', 'Gujarat', 'Goa', 'Dadra and Nagar Hav.', 'Kerala', 'Puducherry', 'Daman and Diu', 'Rajasthan', 'Delhi', 'Haryana', 'Punjab', 'Himachal Pradesh', 'Uttaranchal', 'LADAKH', 'Region']. Whenever user searches or writes any state, try to match it items in State List. Any filter on State should be a subset of this list only. Users may misspell some of the states while asking, try to find its nearest match from the above State list and then create a sql query based on that. For example, IF I have asked for an analysis of 'haryan', then its nearest match in BRAND LIST is 'Haryana'. So SQL Code should have something like WHERE Brand = 'Haryana' in its final code.
        -> Users may spell some words incorrectly, but you should take care while responding to them. If an exact match is found, then it's okay and you can show that result. If an exact match is not found then what you need to do is find the nearest or closest word to the user input and then produce output. For eg, If the user inputs '50-50 Golmaal' or '50-50 golmal', then give results for its nearest match brand, '50-50 Golmal'. Similarly do for rest.
        -> The SQL database has the name INNOVATION which contains the purchasing history of consistent retailers over the years from 2020 to 2023 for various brands and has the following columns listed in the column list below.
        -> Column List: ['Month', 'repeat_L3M', 'UniqueRetCumulative', 'Repeat_last_month','TotalSalesRate', 'TotalPurchaseRate', 'Sales_Quantity_CBB', 'Sales_Quantity_Pkts', 'Sales_Volume_KG', 'ECO', 'PDO', 'Brand', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate', 'Monthly_Consistent_Group_pur_rate', 'Set', 'State', 'Filename', 'Region']  
        -> Now I will help you understand the meanings and usage of each column one by one:
        -> 'Month' column gives information about the specific date.about those retailers history.
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
        -> 'Set' will tell us about at which level the information is about, Overall 'India' level, 'State' level or 'Region' level.
        -> 'State' will give more information about this set, and tell the more info for that level id set is India or State.
        -> 'Region' has names of 7 regions of India , and it will give data information for those regions. 
        -> Show Sales results in comma separated format and upto two decimal points.
        -> Whenever I use the word 'Summarize' show the totals of 'Consistent_Group_Ret', 'TotalSalesRate', 'PDO', 'ECO' and 'Consistent_Group_pur_rate' from the table. Also calculate month on month growth and show it in another column. For example, Question: Summarize the data for the month september 2022 for brand 50-50 golmal, SQL Code: SELECT SUM(TotalSalesRate),SUM(Consistent_Group_Ret),SUM(PDO),SUM(Consistent_Group_pur_rate), SUM(ECO) FROM INNOVATION WHERE Brand = '50-50 Golmal' AND Month LIKE '2022-09-01' GROUP BY Month;

        -> If I ask two columns and out of those two columns, one has non-numeric values and one has numeric, then always display non numeric column first and then after that the numeric column.
        -> If I mention sales, always show Sum of TotalSalesRate at that granularity/level.
        -> If I mention any month(mm) with year(yyyy) also, then only check for day 01 month mm and year yyyy, like, yyyy-mm-01 in the Months column. For example, if I ask for total sales for the month of September 2023 or Sept 2023, then check for 2023-09-01 only in the Month column. SQL Code should be like - SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE Month =='2023-09-01' AND Brand = '50-50 Golmal';
        -> If I mention any month(mm) without year, then take sum of that month for all the years from the month column. For example, if I ask total sales for sept or September then find the sum of sales of sept from 2020,2021,2022,2023. SQL Code be like - SELECT SUM(TotalSalesRate) FROM INNOVATION WHERE Month LIKE '____-09-01' AND Brand = '50-50 Golmal';
        -> If any day, month, year is mentioned first convert it into datetime64 format as 'yyyy-mm-dd' and then run the query.
        -> If asked for a particular month take only 1st day of that month like if asked for sept 2023 sql code should have something like - WHERE MONTH LIKE '2023-09-01' and if asked for a particular year take all the months(only first days of each month) of that particular year,for example if asked for 2022, sql should have something like -  WHERE MONTH LIKE '2022-__-01'. If asked for a particular month without mentioning year then search for all the years for that month, for example if I asked for september only, then sql code have something like - WHERE MONTH LIKE '____-09-01';
        
        -> Only Consistent_Group_Ret should be used to calculate Month on Month growth.
        
        -> Now, second type of question can be asked to find month on month growth for all the months of over the months. For such cases use below two points to generate a appropriate code. It should not be mixed with the code where user asks for mon on month growth for a particular month.
                    3 -> To calculate month on month growth for all the months, subtract the latest month's Consistent_Group_Ret from previous month's Consistent_Group_Ret and divide by previous month's Consistent_Group_Ret. For example if I asked for month on month growth for all the months , SQL code will be something like SELECT Month, SUM(Consistent_Group_Ret) AS Total_Consistent_Group_Ret, (SUM(Consistent_Group_Ret) - LAG(SUM(Consistent_Group_Ret), 1, 0) OVER (ORDER BY Month))*100 / LAG(SUM(Consistent_Group_Ret), 1, 1) OVER (ORDER BY Month) AS Month_on_Month_Growth FROM INNOVATION GROUP BY Month ORDER BY Month;
                    4 -> To calculate month on month growth for all months for a particular state and brand, subtract the latest month's Consistent_Group_Ret from previous month's Consistent_Group_Ret and divide by previous month's Consistent_Group_Ret and filter out for that state and brand. For example if I asked for month on month growth for only India state and 50-50 golmal brand, SQL code will be something like: SELECT Month, SUM(Consistent_Group_Ret) AS Total_Consistent_Group_Ret, (SUM(Consistent_Group_Ret) - LAG(SUM(Consistent_Group_Ret), 1, 0) OVER (ORDER BY Month))*100 / LAG(SUM(Consistent_Group_Ret), 1, 1) OVER (ORDER BY Month) AS Month_on_Month_Growth FROM INNOVATION WHERE Brand = '50-50 Golmal' AND State = 'India' GROUP BY Month ORDER BY Month;

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


    #5 -> If month on month growth is asked for a particular month only, do it like this: Example - Question: Give the month on month growth of croissant brand for september 2023. SQL code will be something like: SELECT TOP 1 Month, CAST(SUM(Consistent_Group_Ret) AS FLOAT) AS Total_Consistent_Group_Ret, (CAST(SUM(Consistent_Group_Ret) AS FLOAT) - LAG(CAST(SUM(Consistent_Group_Ret) AS FLOAT), 1, 0) OVER (ORDER BY Month)) * 100 / LAG(CAST(SUM(Consistent_Group_Ret) AS FLOAT), 1, 1) OVER (ORDER BY Month) AS Month_on_Month_Growth FROM Consistent WHERE Month IN ('2023-08-01', '2023-09-01') AND Brand = 'Croissant' GROUP BY Month ORDER BY Month DESC;
    #7 - Question: Give the month on month growth of 50-50 Golmal brand for september 2023, SQL Code: SELECT Month, CAST(SUM(Consistent_Group_Ret) AS FLOAT) AS Total_Consistent_Group_Ret, (CAST(SUM(Consistent_Group_Ret) AS FLOAT) - LAG(CAST(SUM(Consistent_Group_Ret) AS FLOAT), 1, 0) OVER (ORDER BY Month)) * 100 / LAG(CAST(SUM(Consistent_Group_Ret) AS FLOAT), 1, 1) OVER (ORDER BY Month) AS Month_on_Month_Growth FROM (SELECT Month, SUM(CAST(Consistent_Group_Ret AS FLOAT)) AS Consistent_Group_Ret FROM INNOVATION WHERE Month IN ('2023-08-01', '2023-09-01') AND Brand = '50-50 Golmal' GROUP BY Month) ORDER BY Month DESC LIMIT 1;
    
    prompt2 = [
        """
        You are an expert in understanding English Language and presenting it in a very formal professional way. A question will be asked to you with its result. You need to present this result in a professional form to the user. 
        If the result is a number or a string or not in data frame format then simply paraphrase the question and adjust the result in a single sentence. For example, If the user asks - Show me the total sales for 50-50 Golmal in the month of August 2023 and result provided is 234567, then you should reply something like "Total sales for 50-50 Golmal in the month of August 2023 accounted to 2,34,567 rupees.
        If the result passed is:"Dataframe", simply just paraphrase the question and tell that the required dataset is represented below, but don't show any dataframe from your side. I repeat, do NOT show any table or dataset or dataframe from your side, just paraphrase the question and say the answer is presented below. For example, if a user asks to show me the total sales for unique brands, simply write " According to the data Total sales for each of the unique brands are shown below." 
        Show currency values in comma separated format.
        Show sales and purchase values in crores and lakhs of rupees, as suitable.
        Show all decimal values until only 2 decimal points and don't change any Integer value.
        Whenever "summarize" is used in the question, the answer will contain 5 parameters - Total Sales, Consistent Group Retailers, PDO, Consistent Group Purchase Rate and ECO, that too, in the same order as I wrote. So answer accordingly.
        
        Example1: Question - Give me consistent retailers for 50-50 Golmal for Oct 23 for India. Answer passed-[(India, 83237.0)].Your Output: Consistent retailers for 50-50 Golmal in India for Oct 23 accounted for 83,237
        Example2: Question - Give me a brand which has the most consistent retailers and sales in India in Oct-23. Answer passed-[('50-50 Golmal', 83237.0, 107051826.143)]. Your Output: Brand 50-50 Golmal has the most consistent retailers and sales in India in Oct-23 with 83,237 consistent retailers and total sales revenue of 107,051,826.14 rupees.
        Example3: Question - summarize the data for the month september 2022 for brand 50-50 golmal. Answer Passed - [(163108179.76, 55497.0, 64219.050409263284, 162860985.63, 292185)]. Your Output: Sales revenue for brand 50-50 Golmal for the month of September 2022 was 16.31 crores with 55,497 consistent retailers and 64,219.05 total PDO. Total Consistent Group Purchase Rate recorded for the brand was 16.28 crores with an ECO total of 2,92,185.
        Example4: Question - Give the month on month growth of croissant brand for oct 22 to nov 22. Answer Passed -  [('2022-11-01', 0.6967381480568564)]. Your Output: The month on month growth for Croissant brand from Oct'22 to Nov'22 was 0.69%

        """
    ]
    prompt3 = [
        """
        You are an expert in understanding English Language and converting it into streamlit codes. There will be questions asked by the user and in answer a dataframe is passed generally. You have to convert this data frame/table into various types of charts using streamlit code so that it can be presentable. So, for example if a user asks to show me the chart of this data and the table passed has one of the columns as month in it. so you need to create a code for a line chart for this like : st.line_chart(df, x=column_names[0], y=column_names[1]). 

        """
    ]


    st.header("#Consistent")
    st.subheader("Retrieve Data")
    question=st.text_input("Input: ",key="input")
    submit=st.button("SUBMIT")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if submit or question :
        try:
            question_string = "Question: " + question
            print(question_string)
            response = get_gemini_response(question=question, prompt=prompt)
            print(response)
            response_df, column_names = read_sql_query(response, "innovation.db")
            st.subheader("The Response is")
            
            # st.write(len(response_df))
            # st.write(response_df)
            if len(response_df)==1:
                result = response_df
                question_string = "Question: " + question
                answer_string = "Answer: " + str(result)
                # st.write(answer_string)
                response2 = get_gemini_response2(question_string, prompt2,answer_string)
                # st.write(str(result))
                st.write(response2)
                st.session_state['chat_history'].append(("Bot",response2))
                st.session_state['chat_history'].append(("You", question))
            else:
                df = pd.DataFrame(response_df, columns=column_names)

                response2 = get_gemini_response2(question_string,prompt2,"Dataframe")
                st.write(response2)
                st.dataframe(df,hide_index=True)
                st.line_chart(df, x=column_names[0], y=column_names[1:])
                st.session_state['chat_history'].append(("Bot", df))
                st.session_state['chat_history'].append(("You", question))
        except:
            st.write("Sorry, I am unable to understand you query. Please provide more information. Thank you!!")

        # response3 = get_gemini_response3(question_string,prompt3, df)
    cch = st.button("Clear Chat History")
    if cch:
        st.session_state['chat_history'] = []
    st.subheader("The Chat History is")
    for role, text in st.session_state['chat_history'][::-1]:
        if isinstance(text, pd.DataFrame):
            st.write(f"{role}:")
            st.dataframe(text)
        else:
            st.write(f"{role}: {text}")