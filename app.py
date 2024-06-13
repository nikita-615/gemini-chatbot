import graph_non_nlp
import helper2
from dotenv import load_dotenv

load_dotenv()
import pandas as pd
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import numpy as np
import helper

# col1, col3 = st.sidebar.columns([6, 3])
# with col1:
#     st.image('https://www.britannia.co.in/_next/image?url=https%3A%2F%2Fwww.britannia.co.in%2Fdata%2FBritannia_Logo_fcce3225c0.png&w=1080&q=100')
# with col3:
#     st.image('https://i.imgur.com/IsxqyCy.png')
st.sidebar.title("#AskBritInsightSphere💬")
user_menu = st.sidebar.radio('Select an Option',('Consistent', 'KATs', 'Control Tower'))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
df = helper2.load_data()
df2 = df.copy()


if user_menu == 'KATs':
    st.subheader("Retrieve Data")
    question = st.text_input("Input: ", key="input")
    submit = st.button("SUBMIT")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if submit or question:
        try:
            question_string = "Question: " + question
            print(question_string)
            response = helper.get_gemini_response(question=question, prompt=helper.prompt4)
            print("SQL Query provided by Gemini \n", response)
            response_df, column_names = helper.read_sql_query(response, "GT.db")
            print("The Response df that we got from the database\n ", response_df)
            st.subheader("The Response is")
            # st.write(response,response_df)
            if len(response_df) == 1:
                result = response_df
                question_string = "Question: " + question
                answer_string = "Answer: " + str(result)
                # st.write(answer_string)
                response2 = helper.get_gemini_response2(question_string, helper.prompt2, answer_string)
                # st.write(str(result))
                st.write(response2)
                st.session_state['chat_history'].append(("Bot", response2))
                st.session_state['chat_history'].append(("You", question))
            else:
                df = pd.DataFrame(response_df, columns=column_names)
                response2 = helper.get_gemini_response2(question_string, helper.prompt2, "Dataframe")
                st.write(response2)
                st.dataframe(df, hide_index=True)
                st.line_chart(df, x=column_names[0], y=column_names[1:])
                st.session_state['chat_history'].append(("Bot", df))
                st.session_state['chat_history'].append(("You", question))
        except Exception as e:
            print(f"Exception Triggered. {e}")
            st.write("Sorry, I am unable to understand you query. Please provide more information. Thank you!")


if user_menu == 'Consistent':

    st.header("#AskBritInsightSphere💬")
    question = st.text_input("Input: ", key="input")
    submit = st.button("SUBMIT")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if submit or question:
        try:
            question_string = "Question: " + question
            print(question_string)
            response = helper.get_gemini_response(question=question, prompt=helper.prompt)
            print("SQL Query provided by Gemini \n", response)
            response_df, column_names = helper.read_sql_query(response, "innovation.db")
            # if ("growth" in question_string.lower()):
            
            print("The Response df that we got from the database\n ", response_df)
            st.subheader("The Response is")

            # st.write(len(response_df))
            # st.write(response_df)
            if len(response_df) == 1:
                result = response_df
                question_string = "Question: " + question
                answer_string = "Answer: " + str(result)
                # st.write(answer_string)
                response2 = helper.get_gemini_response2(question_string, helper.prompt2, answer_string)
                # st.write(str(result))
                st.write(response2)
                st.session_state['chat_history'].append(("Bot", response2))
                st.session_state['chat_history'].append(("You", question))
            else:
                df = pd.DataFrame(response_df, columns=column_names)
                response2 = helper.get_gemini_response2(question_string, helper.prompt2, "Dataframe")
                st.write(response2)
                st.dataframe(df, hide_index=True)
                st.line_chart(df, x=column_names[0], y=column_names[1:])
                st.session_state['chat_history'].append(("Bot", df))
                st.session_state['chat_history'].append(("You", question))
        except Exception as e:
            print(f"Exception Triggered. {e}")
            st.write("Sorry, I am unable to understand you query. Please provide more information. Thank you!")


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

    if st.sidebar.checkbox('Graphics'):
        st.header("")
        st.subheader("Data Visualization")
        visual = graph_non_nlp.visuals(df2)
