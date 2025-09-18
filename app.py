import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard", page_icon="📊")
st.title("📊HR Analytics Dashboard") # title

#SETUP DATASET
conn = sqlite3.connect("hr.db") # connect with database
df = pd.read_sql_query("SELECT * FROM employees", conn) #copy database to df

#STYLE to make taps better
st.markdown(
    """
    <style>

    .stTabs [role="tab"] {
        flex: 1;  /* each tab takes equal width */
        text-align: center; /* make text in center */
        font-size: 18px; /* make font bigger */
    }
    .stApp {
        background-color: #5fc5dc; /* change background color */
    }

    </style>
    """,
    unsafe_allow_html=True
)


#SPLIT TAP'S
tab1, tab2 ,tab3 = st.tabs(["DASHBOARD","EMPLOYEES MANAGMENT","CHART"])


#####################################################


with tab1:
    st.title("DYNAMIC DASHBOARD")
    #SelectBox for filter
    selectDep = st.selectbox("Select Department",
                             ("All","Human Resources","Research & Development","Sales"))
    st.write(f"**You Select {selectDep} Department**")
    #filter
    if selectDep != "All":
        filterDF = df[df["Department"] == selectDep]
    else:
        filterDF = df
    
    #dynamic fig - bar chart
    dynFig1 = px.bar(
        filterDF.groupby("Department").size().reset_index(name = "Employees"),
        x="Department",
        y="Employees",
        title="EMPLOYEES IN EVERY DEPARTMENT",
        text="Employees",
        color="Department"
    )
    st.plotly_chart(dynFig1, use_container_width=True)

    #dynamic fig - pie chart
    dynFig2 = px.pie(filterDF,
                     names="JobRole",
                     values="MonthlyIncome",
                     title="MONTHLY INCOME BY JOBROLE")
    st.plotly_chart(dynFig2, use_container_width=True)
    
    #dynamic fig - scatter
    dynFig3 = px.scatter(filterDF,
                         x = "TotalWorkingYears" , y = "MonthlyIncome",
                         color = "TotalWorkingYears",
                         title="Income vs Total Working Years"
    )
    st.plotly_chart(dynFig3, use_container_width=True)

    #dynamic fig - histogram with box
    avgIncome_byAge = (
    filterDF.groupby("Age")["MonthlyIncome"]
            .mean()
            .reset_index(name= "AvgMonthlyIncome")
    )
    dynFig4 = px.line(avgIncome_byAge,
                      x = "Age",
                      y = "AvgMonthlyIncome"
    )
    st.plotly_chart(dynFig4, use_container_width=True)

    #dynamic fig - stacked histogram 
    dynFig5 = px.histogram(filterDF,
                            x="JobRole", color="OverTime",
                            title="Overtime by Job Role"
    )
    st.plotly_chart(dynFig5, use_container_width=True)

    #TABLE
    st.dataframe(filterDF.set_index("EmployeeNumber"))
