import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
                    #to give title to  page             to give icon to page
st.set_page_config(page_title="HR Analytics Dashboard", page_icon="📊") 

col_logo, col_header = st.columns([1, 3])  # 1 جزء يسار, 5 أجزاء يمين

with col_logo:
    st.image("assets\stc_logo_pink_frame.png", width=250)  # صغّر الحجم بالـ width

with col_header:
    st.title("HR Analytics Dashboard")

#SETUP DATASET
conn = sqlite3.connect("hr.db") # connect with database
df = pd.read_sql_query("SELECT * FROM employees", conn) #copy database to df

backGroundColor = "#4F008C"
fontColor = "#FF375E"
fig_font_color = "#ffffff"

#STYLE to make taps better
st.markdown(
    f"""
    <style>
    .stTabs [role="tab"] {{
        flex: 1; /* each tab takes equal width */
        text-align: center; /* make text in center */
        font-size: 18px; /* make font bigger */
        color: {fontColor}; /* font color */
    }}

    .stApp {{
        background-color: {backGroundColor}; /* change background color */
        color: {fontColor}; /* font color */
    }}

    /* Titles and Headers , label for selectbox and number input */
    .stMarkdown, .stText, 
    .stSelectbox label, .stNumberInput label {{
        color: {fontColor};
    }}

    [data-testid="stWidgetLabel"] * {{
        color: {fontColor};
    }}

    /* Metric + Subheader (h3) */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    h3 {{
        color: {fig_font_color} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


#automatic employees number increase
def emp_numb(): 
    new_numb = ( len(df) +1 )
    return new_numb

# make every chart have same color
def style_fig(fig, bg=backGroundColor, font_color=fig_font_color):
    fig.update_layout(
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        font = dict(color=font_color),
        title = dict(font=dict(color=font_color)),
        xaxis = dict(title_font=dict(color=font_color), tickfont=dict(color=font_color)),
        yaxis = dict(title_font=dict(color=font_color), tickfont=dict(color=font_color)),
        legend = dict(title_font=dict(color=font_color), font=dict(color=font_color)),
        hoverlabel = dict(font_color=font_color, bgcolor=bg, bordercolor=font_color)
    )
    for tr in fig.data:
        tr.textfont = dict(color="white")
    return fig


#SPLIT TAP'S
tab1, tab2 ,tab3 = st.tabs(["DASHBOARD","EMPLOYEES MANAGMENT","CHART"])

#####################################################
# tab1 - for dynamic dashboard
#####################################################

with tab1: #dynamic dashboard tab
    st.title("DYNAMIC DASHBOARD")

    #SelectBox for filter
    selectDep = st.selectbox("Select Department",
                             ("All","Human Resources","Research & Development","Sales"))
    st.write(f"**You Select {selectDep} Department**")

    #department filter
    if selectDep != "All":
        filterDF = df[df["Department"] == selectDep]
    else:
        filterDF = df
    
    #dynamic fig - bar chart
    dynFig1 = px.bar(
        filterDF.groupby("Department").size().reset_index(name = "Employees"),
        x="Department",
        y="Employees",
        title="Employees in every department",
        text="Employees",
        color="Department"
    )        #style_fig is funcation to make every chart have same color
    dynFig1 = style_fig(dynFig1) 
    st.plotly_chart(dynFig1, use_container_width=True)

    #dynamic fig - pie chart
    dynFig2 = px.pie(filterDF,
                     names="JobRole",
                     values="MonthlyIncome",
                     title="Monthly income by jobrole")
    dynFig2 = style_fig(dynFig2)
    st.plotly_chart(dynFig2, use_container_width=True)
    
    #dynamic fig - scatter
    dynFig3 = px.scatter(filterDF,
                         x = "TotalWorkingYears" , y = "MonthlyIncome",
                         color = "TotalWorkingYears",
                         title="Income vs total working years",
                         color_continuous_scale=["yellow", "red"]
    )
    dynFig3 = style_fig(dynFig3)
    st.plotly_chart(dynFig3, use_container_width=True)

    #make avg for monthly income group by age = want for dynfig4
    avgIncome_byAge = (
    filterDF.groupby("Age")["MonthlyIncome"]
            .mean()
            .reset_index(name= "AvgMonthlyIncome")
    )

    #dynamic fig - histogram with box
    dynFig4 = px.line(avgIncome_byAge,
                      x = "Age",
                      y = "AvgMonthlyIncome",
                      title="Avg income by age",
                      color_discrete_sequence=["#f7e8d2"]
    )
    dynFig4 = style_fig(dynFig4)
    st.plotly_chart(dynFig4, use_container_width=True)

    #dynamic fig - stacked histogram 
    dynFig5 = px.histogram(filterDF,
                            x="JobRole", color="OverTime",
                            title="Overtime by jobrole",
                            color_discrete_sequence=["#edb96d","#e68c0b"]
    ) 
    dynFig5 = style_fig(dynFig5)
    st.plotly_chart(dynFig5, use_container_width=True)

    #TABLE for employees work with department filter
    st.subheader("Employees Table")
    st.dataframe(filterDF.set_index("EmployeeNumber"))

#############################################################
# tab2 - for manage employees add emp or update he is income
#############################################################

with tab2: # employees managment tab page
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

    #to enter employees number
    emp_numb_update = st.number_input("Enter employees number", step=1,  format="%d")

    #to enter new income to update it
    emp_income_update = st.number_input("Enter new income", step = 50 , min_value= 500)
    
    #update button
    update_btn = st.button("UPDATE")
    if update_btn:
        try:
            update_sql = """
                UPDATE employees SET MonthlyIncome = ? WHERE EmployeeNumber = ?
            """
            update_vals = (int(emp_income_update), int(emp_numb_update))
            cursor = conn.cursor()
            cursor.execute(update_sql, update_vals)

            #to see if employees exist or not
            if cursor.rowcount == 0:  #if no rows affected
                st.warning(f"Employee number {emp_numb_update} not found.")
            else:
                conn.commit()
                st.success(f"Income update to {emp_income_update} for emplyees number: {emp_numb_update}")
                st.rerun()
        except Exception as e:
            st.error(f"There error : {e}")

#####################################################
# tab 3 - more chart and include the questions
#####################################################

with tab3: # tabs for more chart it's helpful for hr
    st.title("MORE USEFUL CHART")
    st.markdown("-----------------------------------------------------------")

    #Q1/ How many total employees are there?
    total_employees = pd.read_sql_query("""SELECT COUNT(*) AS ALL_EMPLOYEES FROM employees;""", conn)
    st.metric(label="Q1: How many total employees are there?",
            value=int(total_employees["ALL_EMPLOYEES"]))

    #Q2/ What is the employee count for each department?
    dept_counts = pd.read_sql_query("""SELECT Department , COUNT(*) AS EMPLOYEES
                                    FROM employees GROUP BY Department;""", conn)
    fig2 = px.bar(dept_counts, x="Department", y="EMPLOYEES",
                title="Q2: Employee count for each department",
                text="EMPLOYEES", color="Department")
    st.plotly_chart(style_fig(fig2), use_container_width=True)

    #Q3/ What is the average monthly income by job role?
    avg_income_byJob = pd.read_sql_query("""SELECT JobRole , AVG(MonthlyIncome) AS AVG_MonthlyIncome
                                            FROM employees GROUP BY JobRole;""", conn)
    fig3 = px.pie(avg_income_byJob, values="AVG_MonthlyIncome", names="JobRole",
                title="Q3: Average monthly income by job role")
    st.plotly_chart(style_fig(fig3), use_container_width=True)

    #Q4/ Who are the top 5 employees by performance rating?
    top5_Performance = pd.read_sql_query("""SELECT EmployeeNumber, Department, JobRole, PerformanceRating, MonthlyIncome 
                                        FROM employees ORDER BY PerformanceRating DESC LIMIT 5;""", conn)
    st.subheader("Q4: Top 5 employees by performance rating")
    st.dataframe(top5_Performance)

    #Q5/ Which department has the highest average performance rating?      CTE
    highAVG_dep = pd.read_sql_query("""WITH AvgDeptPerformance AS (
    SELECT Department, AVG(PerformanceRating) as Avg_Performance
    FROM employees
    GROUP BY Department
    )
    SELECT Department, Avg_Performance
    FROM AvgDeptPerformance
    ORDER BY Avg_Performance DESC
    LIMIT 3;""", conn)
    st.subheader("Q5: Department with highest average performance rating")
    st.dataframe(highAVG_dep)

    #Q6/ What Average age of employees for each Department?
    avgAGE_Emp = pd.read_sql_query("""SELECT Department, AVG(Age) AS AVG_Age 
                                    FROM employees GROUP BY Department;""", conn)
    fig6 = px.bar(avgAGE_Emp, x="Department", y="AVG_Age",
                title="Q6: Average age of employees by department",
                text="AVG_Age", color="Department")
    st.plotly_chart(style_fig(fig6), use_container_width=True)

    #Q7/ What Average monthly income by gender ?
    avg_income_gender = pd.read_sql_query("""SELECT Gender, AVG(MonthlyIncome) AS AVG_MonthlyIncome
                                             FROM employees GROUP BY Gender;""", conn)
    fig7 = px.bar(avg_income_gender, x="Gender", y="AVG_MonthlyIncome",
                  title="Q7: Average monthly income by gender",
                  text="AVG_MonthlyIncome", color="Gender")
    st.plotly_chart(style_fig(fig7), use_container_width=True)

    #Q8/ What is the average monthly income by education level?
    avg_income_edu = pd.read_sql_query("""SELECT Education, AVG(MonthlyIncome) AS AVG_MonthlyIncome
                                          FROM employees GROUP BY Education;""", conn)
    fig8 = px.area(avg_income_edu, x="Education", y="AVG_MonthlyIncome",
                   title="Q8: Average monthly income by education level")
    st.plotly_chart(style_fig(fig8), use_container_width=True)

    #Q9/ Which job role works the most overtime?           CTE
    mostOvertime = pd.read_sql_query("""WITH OvertimeCounts AS (
    SELECT JobRole, COUNT(*) AS Number_Overtime
    FROM employees
    WHERE OverTime = 'Yes'
    GROUP BY JobRole
    )
    SELECT *
    FROM OvertimeCounts
    ORDER BY Number_Overtime DESC;
""", conn)
    fig9 = px.bar(mostOvertime, x="JobRole", y="Number_Overtime",
                  title="Q9: Job roles with most overtime",
                  text="Number_Overtime", color="JobRole")
    st.plotly_chart(style_fig(fig9), use_container_width=True)

    #Q10/ What Average years at company by department ?
    avg_year_byDep = pd.read_sql_query("""SELECT Department, AVG(YearsAtCompany) AS AVG_YearsAtCompany
                                          FROM employees GROUP BY Department;""", conn)
    fig10 = px.bar(avg_year_byDep, x="Department", y="AVG_YearsAtCompany",
                   title="Q10: Average years at company by department",
                   text="AVG_YearsAtCompany", color="Department")
    st.plotly_chart(style_fig(fig10), use_container_width=True)

    #Q11/ What Average monthly income by job level ?
    avg_income_joblevel = pd.read_sql_query("""SELECT Joblevel, AVG(MonthlyIncome) AS AVG_MonthlyIncome
                                               FROM employees GROUP BY Joblevel;""", conn)
    fig11 = px.bar(avg_income_joblevel, x="JobLevel", y="AVG_MonthlyIncome",
                title="Q11: Average monthly income by job level",
                text="AVG_MonthlyIncome", color="JobLevel")
    st.plotly_chart(style_fig(fig11), use_container_width=True)


    #Q12/ Avarage Performance rating by years at company (loyalty vs performance) ?
    per_byYear = pd.read_sql_query("""SELECT YearsAtCompany, AVG(PerformanceRating) AS AVG_PerformanceRating 
                                      FROM employees GROUP BY YearsAtCompany 
                                      ORDER BY YearsAtCompany DESC;""", conn)
    fig12 = px.line(per_byYear, x="YearsAtCompany", y="AVG_PerformanceRating",
                    title="Q12: Average performance rating by years at company (loyalty vs performance)",
                    markers=True, color_discrete_sequence=["#FFD700"])
    st.plotly_chart(style_fig(fig12), use_container_width=True)
    