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

#automatic employees number increase
def emp_numb(): 
    new_numb = ( len(df) +1 )
    return new_numb

# make every chart have same color
def style_fig(fig, bg="#5fc5dc", font_color="black"):
    fig.update_layout(
        paper_bgcolor=bg, #paper color
        plot_bgcolor=bg, # chart background color
        font=dict(color=font_color), #font color
        xaxis=dict(title_font=dict(color=font_color), tickfont=dict(color=font_color)), #font color for title and labels
        yaxis=dict(title_font=dict(color=font_color), tickfont=dict(color=font_color)), #font color for title and labels
        legend_title=dict(font=dict(color=font_color)) #change legend color
    )
    return fig


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
    dynFig1 = style_fig(dynFig1)
    st.plotly_chart(dynFig1, use_container_width=True)

    #dynamic fig - pie chart
    dynFig2 = px.pie(filterDF,
                     names="JobRole",
                     values="MonthlyIncome",
                     title="MONTHLY INCOME BY JOBROLE")
    dynFig2 = style_fig(dynFig2)
    st.plotly_chart(dynFig2, use_container_width=True)
    
    #dynamic fig - scatter
    dynFig3 = px.scatter(filterDF,
                         x = "TotalWorkingYears" , y = "MonthlyIncome",
                         color = "TotalWorkingYears",
                         title="Income vs Total Working Years"
    )
    dynFig3 = style_fig(dynFig3)
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
    dynFig4 = style_fig(dynFig4)
    st.plotly_chart(dynFig4, use_container_width=True)

    #dynamic fig - stacked histogram 
    dynFig5 = px.histogram(filterDF,
                            x="JobRole", color="OverTime",
                            title="Overtime by Job Role"
    )
    dynFig5 = style_fig(dynFig5)
    st.plotly_chart(dynFig5, use_container_width=True)

    #TABLE
    st.dataframe(filterDF.set_index("EmployeeNumber"))
#####################################################

with tab2:
    st.title("MANAGE EMPLOYEES")
    st.markdown("----------------------------------------------------------------------")
    st.header("ADD EMPLOYEES")
    
    col1 , col2 = st.columns(2) #to split page

    
    with col1:
        #select department
        dep = st.selectbox("Department", 
                            sorted(df["Department"]
                            .unique())
            )
        #role filter 
        rolesFilter = df.loc[df["Department"] == dep , 
                            "JobRole"].unique()
        #select role
        roleSELECT = st.selectbox("JobRole",(rolesFilter))
        #income
        income = st.number_input("Income",1000 , 1000000 ,step = 50)
    with col2:
        #select age 
        age = st.number_input("Age",15 , 100)
        #education filter
        eduFilter = df.groupby("EducationField")
        #education
        edu = st.selectbox("Eduction",eduFilter)
        #gender
        gender = st.pills("Gender", ("Male" , "Female"))

        #Add button to database
        add_btn = st.button("ADD")
        if add_btn:
            new_emp_numb = emp_numb()
            try:
                add_sql = """
                    INSERT INTO employees
                        (EmployeeNumber, Department, JobRole, MonthlyIncome, Age, EducationField, Gender)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                add_vals = (new_emp_numb, dep, roleSELECT, int(income), int(age), edu, gender) #value
                conn.execute(add_sql, add_vals)
                conn.commit()
                st.success("Employee added!")
                st.rerun()
            except Exception as e:
                st.error(f"There error : {e}")
        
        #UPDATE INCOME
    st.markdown("--------------------------------------------------------")
    st.header("UPDATE INCOME")
    emp_numb_update = st.number_input("Enter employees number", step=1,  format="%d")
    emp_income_update = st.number_input("Enter new income", step = 50 , min_value= 500)
    update_btn = st.button("UPDATE")

    if update_btn:
        try:
            update_sql = """
                UPDATE employees SET MonthlyIncome = ? WHERE EmployeeNumber = ?
            """
            update_vals = (int(emp_income_update), int(emp_numb_update))  # fixed
            cursor = conn.cursor()
            cursor.execute(update_sql, update_vals)

            if cursor.rowcount == 0:  #if no rows affected
                st.warning(f"Employee number {emp_numb_update} not found.")
            else:
                conn.commit()
                st.success(f"Income update to {emp_income_update} for emplyees number: {emp_numb_update}")
                st.rerun()
        except Exception as e:
            st.error(f"There error : {e}")


            #####################################################


with tab3:
    st.header("MORE USEFUL CHART")
    st.markdown("-----------------------------------------------------------")

    col3 , col4 = st.columns(2) #split page
    
    with col3:
        #Q2/ What is the employee count for each department?
        dept_counts_sql = pd.read_sql_query("""SELECT Department , COUNT(*) AS EMPLOYEES
                            FROM employees 
                            GROUP BY Department;""",conn)
        #bar chart
        fig1 = px.bar(dept_counts_sql, x="Department", y="EMPLOYEES",
                    title="EMPLOYEES IN EVERY DEPARMENT",
                    text="EMPLOYEES",
                    color="Department")
        fig1 = style_fig(fig1)
        st.plotly_chart(fig1, use_container_width=True)

        #Q8/ What is the average monthly income by education level?
        avg_income_edu_sql = pd.read_sql_query("""SELECT Education, AVG(MonthlyIncome) AS AVG_MonthlyIncome
                            FROM employees 
                            GROUP BY Education;""",conn)  
        fig2 = px.area(avg_income_edu_sql, 
                            x="Education",
                            y="AVG_MonthlyIncome",
                            title="AvgMonthly Income by Education Level"
        )
        fig2 = style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col4:
        #Q3/ What is the average monthly income by job role?
        avg_income_byJob_sql = pd.read_sql_query("""SELECT JobRole , AVG(MonthlyIncome) AS AVG_MonthlyIncome
                            FROM employees 
                            GROUP BY JobRole;""",conn)
        #pie chart
        fig3 = px.pie(avg_income_byJob_sql,
                    values="AVG_MonthlyIncome",
                    names="JobRole",
                    title="average monthly income by job role")
        fig3 = style_fig(fig3)
        st.plotly_chart(fig3, use_container_width=True)

        #Q12/ Avarage Performance rating by years at company (loyalty vs performance) ?
        per_byYear_sql = pd.read_sql_query("""SELECT YearsAtCompany, AVG(PerformanceRating) AS AVG_PerformanceRating 
                                FROM employees 
                                GROUP BY YearsAtCompany 
                                ORDER BY YearsAtCompany DESC;""",conn)
        #line chart
        fig4 = px.line(per_byYear_sql,
                    x="YearsAtCompany",
                    y="AVG_PerformanceRating",
                    title="loyalty vs performance",
                    markers=True,
                    color_discrete_sequence=["#FFD700"])
        fig4 = style_fig(fig4)
        st.plotly_chart(fig4, use_container_width=True)