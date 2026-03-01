🔗 Live Dashboard
👉 https://indian-education-inequality-analysis-by-tanishkamhatre.streamlit.ap


Indian Education Inequality Analytics 
A State-wise Data-Driven Study

Developed by: Tanishka Dnyaneshwar Mhatre
B.Tech – Computer Science & Business Systems

Project Overview

Education inequality in India is not just about enrollment numbers. While access to education has improved over the years, deep structural disparities still exist across:

Secondary-level dropout

Gender literacy gap

School infrastructure availability

Rural–Urban enrollment divide

This project builds a composite Education Inequality Index and an interactive Streamlit dashboard to identify high-risk states and analyze the structural drivers behind inequality.

Key Objectives

This project answers the following critical questions:

Which states are facing the highest education inequality?

Is dropout after elementary school the main driver?

Does infrastructure reduce inequality?

Are gender gaps strongly linked to inequality?

Can AI-based clustering group similar states for better policy planning?

Methodology
Feature Engineering

Gender Gap (Literacy) = Male Literacy − Female Literacy

Transition Loss (Dropout Proxy) =
1 − (Secondary Enrollment / Elementary Enrollment)

Infrastructure Index = Average of:

% Schools with Internet

% Schools with Electricity

% Schools with Library

% Schools with Handwash Facility

📊 Composite Education Inequality Index

Higher value = Worse inequality

Education Inequality Index =
0.35 × Transition Loss
+ 0.30 × Gender Gap
+ 0.20 × Rural–Urban Divide
+ 0.15 × Infrastructure Deficit

Key Findings
Highest Inequality States

Uttar Pradesh

Bihar

Odisha

Assam

Delhi


Lowest Inequality States

Punjab

Tamil Nadu

Puducherry

Maharashtra

Andaman & Nicobar Islands


Strongest Structural Driver

Secondary-level Transition Loss (Correlation = 0.54)

Infrastructure alone does not eliminate inequality — dropout prevention and gender equity are critical.


AI-Based Clustering

Using KMeans Clustering, states were grouped into structural patterns:

High Dropout + Weak Infrastructure

Strong Infrastructure + Low Inequality

Moderate Gender Gap Clusters

This supports cluster-based policy design instead of one-size-fits-all intervention.



Dashboard Features

Dynamic state ranking

Correlation visualization

AI clustering scatter plots

Infrastructure trend analysis (2013–2016)

Downloadable CSV tables


Tech Stack

Python

Pandas & NumPy

Plotly

Streamlit

Scikit-learn (KMeans)

Matplotlib & Seaborn
