import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard", page_icon="📊")
st.title("📊HR Analytics Dashboard") # title

#SETUP DATASET
conn = sqlite3.connect("hr.db") # connect with database
df = pd.read_sql_query("SELECT * FROM employees", conn) #copy database to df
