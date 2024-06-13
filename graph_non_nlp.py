import seaborn as sns
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import streamlit as st
import numpy as np
import helper2
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Sample data
def visuals(df):
        df = df[['Month', 'State', 'Brand', 'TotalSalesRate', 'ECO', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate','PDO']]
        df['Month'] = pd.to_datetime(df['Month'], format='%d-%m-%Y')
        df['Year'] = df['Month'].dt.year
        df['Month_no.'] = df['Month'].dt.month
        df['Month_Year'] = df['Month'].dt.strftime('%b-%y')
        df = df.sort_values(by=['Year','Month_no.'])
        month_year = df['Month_Year'].dropna().unique().tolist()
        slider_month = st.select_slider("Pick a Month-year", month_year)
        df = df[['Year', 'Month_no.', 'Month_Year', 'State', 'Brand', 'TotalSalesRate', 'ECO', 'Consistent_Group_Ret','Consistent_Group_pur_rate', 'PDO']]
        df_ss= df[df['Month_Year']==slider_month][['Year', 'Month_no.']].drop_duplicates()
        row_values_iloc = df_ss.iloc[0].values
        year = row_values_iloc[0]
        month = row_values_iloc[1]
        df = df[(df['Year'] >= year)]
        df = df[(df['Year'] > year) | (df['Month_no.'] >= month)]


        cat_columns = ['Month', 'State', 'Brand']
        num_columns = ['TotalSalesRate', 'ECO', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate', 'PDO']
        chart = st.sidebar.selectbox("Select Graph/Chart", ['Table','Line Chart','Bar Chart','Pie Chart','Scatter Plot','Heat Map','Pair Plot'])
        if chart == 'Table':
            final_df = helper2.filtered_df(df)
            final_df['Year'] = final_df['Year'].astype(str)
            final_df['Year'] = final_df['Year'].str.replace(',', '')
            st.dataframe(final_df, hide_index=True)
        if chart == 'Line Chart':
            final_df = helper2.filtered_df2(df)
            selected_cat_1 = st.sidebar.selectbox("Select First Variable", num_columns)
            selected_cat_2 = st.sidebar.selectbox("Select Second Variable", num_columns)
            fig, ax = plt.subplots(figsize=(20,20))
            sns.lineplot(data=final_df, x='Month_Year', y=selected_cat_1, color="r", ax=ax, marker='o', label=selected_cat_1)
            ax2 = ax.twinx()
            sns.lineplot(data=final_df, x='Month_Year', y=selected_cat_2, color="b", ax=ax2,marker='o',label=selected_cat_2)
            # sns.lineplot(data=date_df, x='Month_Year', y='Consistent_Group_pur_rate', color="r", ax=ax2,marker='o')
            # ax.set_ylabel('Total Sales Rate', color='g')
            # ax2.set_ylabel('ECO', color='b')
            # ax.set_xlabel('Month')
            # ax.set_title('Total Sales Rate and ECO Over Time')
            plt.legend(fontsize='large')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        if chart == 'Pie Chart':
            category_column = st.selectbox("Select a categorical column", ['Brand', 'State'])
            numerical_column = st.selectbox("Select a numerical column", num_columns)
            if category_column == 'Brand':
                selected_categories = st.multiselect("Select specific brands", df['Brand'].unique())
            elif category_column == 'State':
                selected_categories = st.multiselect("Select specific states", df['State'].unique())
            helper2.create_pie_chart(df, category_column, numerical_column, selected_categories)
        if chart == 'Bar Chart':
            final_df = helper2.filtered_df(df)
            fig, ax = plt.subplots(figsize=(20, 20))
            ax = sns.barplot(data=final_df, x='State', y='TotalSalesRate', hue='Brand',errorbar=('ci', 5))
            for p in ax.patches:ax.annotate(format(p.get_height(), '.0f'),(p.get_x() + p.get_width() / 2., p.get_height()),ha='center', va='center',xytext=(0, 10),textcoords='offset points', fontsize=25, rotation=0)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            ax.tick_params(axis='both', which='major', labelsize=25)
            st.pyplot(fig)
        if chart == 'Scatter Plot':
            fig, ax = plt.subplots(figsize=(20, 20))
            final_df = helper2.filtered_df(df)
            selected_cat_x = st.sidebar.selectbox("Select X axis Variable", num_columns)
            selected_cat_y = st.sidebar.selectbox("Select Y axis Variable", num_columns)
            ax = sns.scatterplot(x=selected_cat_x, y=selected_cat_y, hue='Brand', data=final_df, s=100,style="State")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            ax.tick_params(axis='both', which='major', labelsize=25)
            st.pyplot(fig)
        if chart == 'Heat Map':
            fig, ax = plt.subplots(figsize=(20, 20))
            final_df = helper2.filtered_df(df)
            selected_num = st.sidebar.selectbox("Select Aggregate Variable", num_columns)
            if len(final_df) > 0:
                pt = final_df.pivot_table(index='State', columns='Brand', values=selected_num,aggfunc=lambda x: round(sum(x), 2)).fillna(0)
                fig, ax = plt.subplots(figsize=(40, 20))
                ax = sns.heatmap(pt, annot=True, fmt='.2f', cmap="YlGnBu", ax=ax, annot_kws={"size": 55})
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                ax.tick_params(axis='both', which='major', labelsize=55)
                st.pyplot(fig)
        if chart == 'Pair Plot':
            df = df[['State', 'Brand', 'TotalSalesRate', 'ECO', 'Consistent_Group_Ret', 'Consistent_Group_pur_rate','PDO']]
            final_df = helper2.filtered_df(df)
            ax = sns.pairplot(final_df, hue="Brand")
            st.pyplot(ax)