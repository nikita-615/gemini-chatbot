Developed an interactive web application that allows users to analyze Britannia data via generating SQL queries from natural language input and Few-shot prompting. This application can analyze and summarize data stored in CSV files by creating visual graphs and performing various analysis. The main technologies used in this project include a Large Language Model (LLM) for natural language processing, a web framework-Streamlit for creating the user interface, and a database management system for handling data, visualizing it through various charts and graphs.

Aim of the Project:
Create a Conversational-Analytical Chatbot which can perform various kinds of analytical operations and also summarize the data at a particular granularity.
Create a Data Visualization model to represent required data in a much more interactive and easy-to-analyze way.

Key Components and Features
1. Large Language Model (LLM) Integration:
Google’s Gemini Pro Model: This advanced LLM is used to interpret natural language input provided by users and generate corresponding SQL queries. By providing detailed instructions in natural language prompts, the model can construct accurate and effective SQL queries.
Generative AI: This technology ensures precise conversion of user input into SQL queries. Users can input complex analytical requests in plain English, and the AI translates these into the appropriate SQL statements.

2. Web Application Development:
Streamlit Framework: Streamlit is employed to create the web application, offering a user-friendly interface that makes it easy for users to interact with the application. Streamlit’s simplicity and effectiveness in creating interactive web apps make it an ideal choice for this project.
User Interface (UI): The UI allows users to input natural language queries, and view the generated SQL queries and results. The design ensures that users with minimal technical knowledge can use the application efficiently.

3. Database Integration:
SQLite Databases: The application uses SQLite for managing and querying the data. SQLite is a lightweight, disk-based database that doesn't require a separate server process, making it suitable for this type of application.
Database Creation from CSV Files: When a user uploads a CSV file, the application automatically creates an SQLite database from the CSV data. This involves reading the CSV file, determining the schema, and populating the database with the data from the CSV.

4. Data Analysis and Visualization:
SQL Query Execution: Once the LLM generates the SQL query, it is executed against the SQLite database. The results are then fetched and displayed to the user.
Summary Graphs and Calculations: The application can generate various types of summary graphs (e.g., bar charts, line graphs, pie plot, pair plot, scatter plot, heat map) and perform calculations (e.g., averages, sums) based on the SQL query results. These visualizations help users gain insights from their data quickly and effectively.
