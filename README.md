# Indian Education Inequality Analytics
### A State-wise Data-Driven Study

## Live Dashboard

https://indian-education-inequality-analysis-by-tanishkamhatre.streamlit.app

## Developed By

Tanishka Dnyaneshwar Mhatre  
B.Tech – Computer Science & Business Systems


## Project Overview

Education inequality in India is not only about access to schools or enrollment numbers. Although educational opportunities have improved over the years, significant differences still exist between states due to factors such as dropout rates, gender disparity, infrastructure availability, and regional differences.

This project focuses on analysing these factors to understand the underlying patterns of education inequality across Indian states.

A Composite Education Inequality Index was developed by combining multiple education indicators. An interactive Streamlit dashboard was created to visualise inequality levels, identify high-risk states, and understand the major factors influencing education outcomes.


## Key Objectives

The main objective of this project is to analyse education inequality through a data-driven approach.

This project aims to answer the following questions:

- Which states experience higher levels of education inequality?
- Is secondary-level dropout one of the major contributors to inequality?
- How does school infrastructure impact education outcomes?
- Are gender literacy differences strongly associated with inequality?
- Can machine learning techniques identify groups of states facing similar challenges?


## Dataset and Data Preparation

The analysis uses state-level education indicators related to:

- Literacy rates
- Gender-wise literacy statistics
- Enrollment levels
- School infrastructure facilities
- Rural and urban education differences

Before analysis, the dataset was cleaned and transformed through:

- Handling missing values
- Removing inconsistencies
- Creating meaningful analytical features
- Preparing indicators for comparison across states


## Methodology

### Feature Engineering

To measure education inequality, multiple factors were converted into analytical indicators.


### Gender Literacy Gap

The difference between male and female literacy rates was calculated to understand gender disparity.

Formula:

Gender Gap = Male Literacy − Female Literacy


### Transition Loss (Dropout Proxy)

Student dropout risk was estimated by comparing secondary-level enrollment with elementary-level enrollment.

Formula:

Transition Loss = 1 − (Secondary Enrollment / Elementary Enrollment)


### Infrastructure Index

A combined infrastructure score was created using important school facility indicators:

- Percentage of schools with internet access
- Percentage of schools with electricity
- Percentage of schools with libraries
- Percentage of schools with handwashing facilities


## Composite Education Inequality Index

A weighted index was developed to measure overall inequality across states.

A higher index value represents higher education inequality.

Formula:

Education Inequality Index =

0.35 × Transition Loss

+ 0.30 × Gender Gap

+ 0.20 × Rural–Urban Divide

+ 0.15 × Infrastructure Deficit


This approach combines multiple dimensions of inequality instead of depending on a single education indicator.


## Key Findings


### States with Highest Education Inequality

The analysis identified the following states as having higher inequality levels:

- Uttar Pradesh
- Bihar
- Odisha
- Assam
- Delhi


### States with Lowest Education Inequality

The states showing comparatively lower inequality were:

- Punjab
- Tamil Nadu
- Puducherry
- Maharashtra
- Andaman & Nicobar Islands


### Major Factor Influencing Inequality

The strongest relationship was observed with:

Secondary-level Transition Loss

Correlation: 0.54

The analysis indicates that reducing dropout rates after elementary education is an important factor in improving educational equality.

While infrastructure plays an important role, improving student retention and reducing gender gaps are equally critical.


## Machine Learning Analysis

K-Means clustering was applied to group states based on similar education characteristics.

The clustering approach identified different structural patterns:

High Dropout and Weak Infrastructure

States facing challenges related to student retention and limited facilities.


Strong Infrastructure and Lower Inequality

States showing better education outcomes with stronger facilities.


Moderate Gender Gap Patterns

States where gender-related education differences require targeted improvement.


This clustering approach helps understand that different states require different strategies rather than a single solution for all regions.


## Dashboard Features

The Streamlit dashboard provides:

- State-wise education inequality ranking
- Comparison between states
- Correlation analysis between education factors
- Machine learning clustering visualization
- Infrastructure trend analysis from 2013 to 2016
- Downloadable analysis reports


## Technology Stack

Programming Language:
- Python

Data Analysis:
- Pandas
- NumPy

Visualization:
- Plotly
- Matplotlib
- Seaborn

Machine Learning:
- Scikit-learn (KMeans Clustering)

Dashboard:
- Streamlit


## Dashboard Preview

<table>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/0e98047e-759e-4e88-a156-009875b2c01e" width="450"/>
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/cb131f10-1f54-4cad-a5e4-72e7a0675e32" width="450"/>
    </td>
  </tr>

  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/7f64806b-1af8-4ad3-8ff3-89b07629664e" width="450"/>
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/c1161bfa-245e-474c-b07c-0aac29aa28d9" width="450"/>
    </td>
  </tr>

  <tr>
    <td colspan="2" align="center">
      <img src="https://github.com/user-attachments/assets/4aeb8768-8d40-471a-88c3-d2348d8182cb" width="450"/>
    </td>
  </tr>
</table>

## Project Outcome

This project demonstrates how data analytics and machine learning can be used to identify patterns of educational inequality, understand contributing factors, and generate meaningful insights for better decision-making.

The analysis converts raw educational data into a structured framework that helps researchers, policymakers, and organisations understand regional educational challenges.
