import seaborn as sns
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import streamlit as st
import numpy as np
import helper
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import ast

# Given string
# input_string = "[Selected Chart: 'Bar Chart'], [Selected Brands: ['Treat Jam POP', 'Croissant']], [Selected States: ['Jharkhand', 'Karnataka']]"

# Convert string to list of lists
# output_list = ast.literal_eval(f"[{input_string}]")
# Sample data
df = pd.read_csv('Innovation_24.csv')

question_string = "draw a Scatter Plot for Sales and PDO of Treat Jam Pop in the states Jharkhand and Karnataka"
response3 = helper.get_gemini_response3(question_string,helper.prompt3)
st.write(response3)
elements = response3.split("; ")
output_list = []
for element in elements:
    key_value = element.split(": ")
    if len(key_value) == 2:
        key = key_value[0].strip("[]").strip()
        value = key_value[1].strip("[]").replace("'", "")
        if "," in value:
            value = [item.strip() for item in value.split(",")]
        output_list.append((key, value))
st.write(str(output_list[1][1]))

if st.sidebar.checkbox('Graphics'):
    df = helper.df_maker(df)
    cat_columns = ['Month', 'State', 'Brand']
    num_columns = ['TotalSalesRate', 'ECO', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate', 'PDO']
    # chart = st.sidebar.selectbox("Select Graph/Chart", ['Table','Line Chart','Bar Chart','Pie Chart','Scatter Plot','Heat Map','Pair Plot'])
    chart = output_list[0][1]
    if chart == 'Table':
        final_df = helper.filtered_df(df)
        st.dataframe(final_df, hide_index=True)

    if chart == 'Line Chart':
        final_df = helper.filtered_df2(df)
        col1, col2 = st.columns(2)
        with col1:
            selected_cat_1 = st.selectbox("Select First Variable", num_columns)
        with col2:
            selected_cat_2 = st.selectbox("Select Second Variable", num_columns)

        fig, ax = plt.subplots(figsize=(20,20))
        sns.lineplot(data=final_df, x='Month_Year', y=selected_cat_1, color="r", ax=ax, marker='o', label=selected_cat_1)
        ax2 = ax.twinx()
        sns.lineplot(data=final_df, x='Month_Year', y=selected_cat_2, color="b", ax=ax2,marker='o',label=selected_cat_2)
        plt.legend(fontsize='large')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.tick_params(axis='both', which='major', labelsize=15)
        st.pyplot(fig)

    if chart == 'Pie Chart':
        brands = output_list[1][1]
        states = output_list[2][1]
        final_df = helper.filtered_df(df, brands, states)
        selected_cat = output_list[3][1]
        category_column = st.selectbox("Select a categorical column", ['Brand', 'State'])
        numerical_column = selected_cat
        if category_column == 'Brand':
            selected_categories = brands
        elif category_column == 'State':
            selected_categories = states
        helper.create_pie_chart(final_df, category_column, numerical_column, selected_categories)

    if chart == 'Bar Chart':
        brands = output_list[1][1]
        states = output_list[2][1]
        final_df = helper.filtered_df(df,brands,states)
        # selected_cat = st.selectbox("Select Aggregate Variable", num_columns)
        selected_cat = output_list[3][1]
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.barplot(data=final_df, x='State', y=selected_cat[0], hue='Brand', errorbar=('ci', 5))

        # Calculate font size based on data or plot size
        data_range = final_df[selected_cat].max() - final_df[selected_cat].min()
        plot_size = min(fig.get_figwidth(), fig.get_figheight())
        fontsize = 25

        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, fontsize), textcoords='offset points', rotation=0)

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=fontsize)
        ax.tick_params(axis='both', which='major', labelsize=fontsize)
        ax.legend(fontsize=fontsize)
        st.pyplot(fig)

    if chart == 'Scatter Plot':
        st.write(output_list[1].dtype())
        if isinstance(output_list[1], tuple):
            brands = output_list[1]
        else:
            brands = output_list[1][1]
        states = output_list[2][1]
        final_df = helper.filtered_df(df, brands, states)
        selected_cat = output_list[3][1]
        col1, col2 = st.columns(2)
        with col1:
            # selected_cat_x = st.selectbox("Select X axis Variable", num_columns)
            selected_cat_x = selected_cat[0]
        with col2:
            # selected_cat_y = st.selectbox("Select Y axis Variable", num_columns)
            selected_cat_y = selected_cat[1]


        # Calculate the number of unique values in x and y axes
        # num_unique_x = final_df[selected_cat_x].nunique()
        # num_unique_y = final_df[selected_cat_y].nunique()

        # Calculate font size based on the number of unique values
        fontsize_x = 30
        fontsize_y = 30
        fig, ax = plt.subplots(figsize=(40, 20))
        ax = sns.scatterplot(x=selected_cat_x, y=selected_cat_y, hue='Brand', data=final_df, s=100, style="State")

        # Set font sizes for x and y tick labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=fontsize_x)
        ax.set_xlabel(selected_cat_x, fontsize=fontsize_x)

        ax.set_yticklabels(ax.get_yticklabels(), fontsize=fontsize_y)
        ax.set_ylabel(selected_cat_y, fontsize=fontsize_y)

        ax.legend(fontsize=max(fontsize_x, fontsize_y))

        st.pyplot(fig)

    if chart == 'Heat Map':
        fig, ax = plt.subplots(figsize=(40, 40))
        brands = output_list[1][1]
        states = output_list[2][1]
        final_df = helper.filtered_df(df, brands, states)
        selected_num = output_list[3][1]
        # selected_num = st.selectbox("Select Aggregate Variable", num_columns)
        data_range = final_df[selected_num].max() - final_df[selected_num].min()
        plot_size = min(fig.get_figwidth(), fig.get_figheight())
        fontsize = 35
        if len(final_df) > 0:
            pt = final_df.pivot_table(index='State', columns='Brand', values=selected_num[0],aggfunc=lambda x: round(sum(x), 2)).fillna(0)
            fig, ax = plt.subplots(figsize=(80, 80))
            ax = sns.heatmap(pt, annot=True, fmt='.2f', cmap="YlGnBu", ax=ax, annot_kws={"size": fontsize})
            ax.set_yticklabels(ax.get_yticklabels(), rotation=45)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            ax.set_xlabel('Brand', fontsize=fontsize)
            ax.set_ylabel('State', fontsize=fontsize)
            ax.tick_params(axis='both', which='major', labelsize=fontsize)
            st.pyplot(fig)

    if chart == 'Pair Plot':
        df = df[['State', 'Brand', 'TotalSalesRate', 'ECO', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate','PDO']]
        brands = output_list[1][1]
        states = output_list[2][1]
        final_df = helper.filtered_df(df, brands, states)
        ax = sns.pairplot(final_df, hue="Brand")
        st.pyplot(ax)