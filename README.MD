# 📊 HR Analytics Dashboard
An interactive HR analytics dashboard that transforms **IBM’s HR dataset** into actionable insights with **Python**, **SQL**, and **Streamlit**, empowering managers to explore data and manage employees with ease.

---

## Table of Contents
- [Visual Demo](#visual-demo)  
- [Project Overview](#project-overview)  
- [Data Source & Dictionary](#data-source--dictionary)  
- [Data Analysis Purpose](#data-analysis-purpose)  
- [Features](#features)  
- [Technology Stack](#technology-stack)  
- [Installation](#️-installation)  
- [Author](#author)  
- [License](#license)

---

## 📷 Visual Demo

![Dashboard Screenshot-1](assets\Screenshot1.png)
![Dashboard Screenshot-2](assets\Screenshot2.png)

---

## 📖 Project Overview

An interactive HR analytics dashboard built with **Python** and **Streamlit** using IBM’s HR dataset.  
The main goal of this project was to analyze HR data and answer key business questions using Python (Pandas) and SQL.
The dashboard provides insights into employee data, allows HR managers to explore key metrics, and includes simple employee management features.  
Data analysis was performed using **Python and SQL**, and the dashboard was built with **Streamlit**.

---

## 📊 Data Source & Dictionary

### Dataset
The project uses the IBM HR Analytics Employee Attrition & Performance dataset.
🔗 Dataset URL: [Kaggle - IBM HR Analytics](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

### Key columns
| Column | Description | Column | Description |
|---|---|---|---|
| `Age` | Age of the employee | `Attrition` | Whether the employee left the company (Yes/No) |
| `BusinessTravel` | Frequency of business travel | `DailyRate` | Daily salary rate |
| `Department` | Department name | `DistanceFromHome` | Distance from home to office (km) |
| `Education` | Education level (1–5) | `EducationField` | Field of education |
| `EmployeeCount` | Always 1 (constant) | `EmployeeNumber` | Unique employee ID |
| `EnvironmentSatisfaction` | Work environment satisfaction (1–4) | `Gender` | Gender (Male/Female) |
| `HourlyRate` | Hourly salary rate | `JobInvolvement` | Job involvement level (1–4) |
| `JobLevel` | Level of the job role | `JobRole` | Employee role (e.g., Sales Executive) |
| `JobSatisfaction` | Job satisfaction (1–4) | `MaritalStatus` | Marital status (Single/Married/Divorced) |
| `MonthlyIncome` | Monthly salary (numeric) | `MonthlyRate` | Monthly salary rate |
| `NumCompaniesWorked` | Number of companies worked at | `Over18` | Whether the employee is over 18 (Yes) |
| `OverTime` | Overtime flag (Yes/No) | `PercentSalaryHike` | Percentage salary increase |
| `PerformanceRating` | Performance rating (1–4) | `RelationshipSatisfaction` | Relationship satisfaction (1–4) |
| `StandardHours` | Standard working hours (80) | `StockOptionLevel` | Stock option level (0–3) |
| `TotalWorkingYears` | Total working years | `TrainingTimesLastYear` | Trainings attended last year |
| `WorkLifeBalance` | Work-life balance rating (1–4) | `YearsAtCompany` | Years spent at the company |
| `YearsInCurrentRole` | Years in current role | `YearsSinceLastPromotion` | Years since last promotion |
| `YearsWithCurrManager` | Years with current manager |  |  |

---

## 📉 Data Analysis Purpose

This project was built to answer important business questions from the HR dataset, such as:
- Q1/ How many total employees are there?
- Q2/ What is the employee count for each department?
- Q3/ What is the average monthly income by job role?
- Q4/ Who are the top 5 employees by performance rating?
- Q5/ Which department has the highest average performance rating?
##### EXTRA QUESTIONS
- Q6/ What Average age of employees for each Department?
- Q7/ What Average monthly income by gender ?
- Q8/ What is the average monthly income by education level?
- Q9/ Which job role works the most overtime?
- Q10/ What Average years at company by department ?
- Q11/ What Average monthly income by job level ?
- Q12/ Performance rating by years at company (loyalty vs performance) ?

---

## 🚀 Features
- **Multi-tabs:** Organized navigation across pages.  
- **Dynamic Dashboard:** Interactive charts and KPIs filtered by department.  
- **Employee Management:** Add new employees or update salary with validation.  
- **Consistent Styling:** Unified design across all charts for a clean look.  
- **User-Friendly:** Simple, attractive, and easy to use.

---

## 🛠 Technology Stack

### 🔧 Technologies
- **Python 3.10** – Core programming language  
- **SQLite3** – Lightweight relational database  
- **Streamlit** – Web framework for building interactive dashboards  

### 📦 Libraries
- `Pandas` – Data manipulation and analysis  
- `Plotly Express` – Interactive data visualization

---

## ⚙️ Installation
- **IN TERMINAL**

1. Clone the repository:
   ```bash
   git clone https://github.com/ibrahim-alatyan/HR_Analysis_DASHBOARD.git
   cd HR_Analysis_DASHBOARD

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt

3. Run the app:
    ```bash
    streamlit run src/app.py

    OR

    python -m streamlit run src/app.py

---

## 👨‍💻 Author
- Ibrahim Al-Atyan

---

## 📄 License
This project is released under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.
