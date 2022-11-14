# Packages
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import mysql.connector as connection

# Settings
st.set_option('deprecation.showPyplotGlobalUse', False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

st.set_page_config(
    page_title="DS7330 Final Project",
    layout="wide",
)


# Loads and caches the data from DB
@st.cache
def load_data():
    try:
        mydb = connection.connect(
            host="finalproject-7330.cnvyqlbvtb7m.us-east-2.rds.amazonaws.com",
            database = 'DB7330',
            user="onecubed",
            passwd="Mondaymorning15",
            use_pure=True
            )
        query = """
            select
                *
            from StudentDemographics

            left join BodySpecifics
            on BodySpecifics.StudentDemographics_StudentID = StudentDemographics.StudentID

            left join HomeLife
            on HomeLife.StudentDemographics_StudentID = StudentDemographics.StudentID

            left join MiscPreferences
            on MiscPreferences.StudentDemographics_StudentID = StudentDemographics.StudentID

            left join SocialActivity
            on SocialActivity.StudentDemographics_StudentID = StudentDemographics.StudentID

            left join WorldIssues
            on WorldIssues.StudentDemographics_StudentID = StudentDemographics.StudentID;
        """
        student_body = pd.read_sql(query,mydb)

        mydb.close() #close the connection
        return student_body
    except Exception as e:
        mydb.close()
        return print(str(e))

df = load_data()

# Show variables and data types
# df.dtypes

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
age_order = pd.unique(df['AgeSurveyed'])
age_order.sort()

## plotly charts
# https://plotly.com/python/plotly-express/

# Dashboard Layout

# Title
st.title("Student Census Data")


with st.sidebar:
    st.write("Filters")
    month_filter = st.multiselect("Birth Month", month_order, default=month_order)
    df = df[df["BirthMonth"].isin(month_filter)]

    age_filter = st.select_slider("Age Range",options=age_order, value=(min(df['AgeSurveyed']),max(df['AgeSurveyed'])))
    df = df[df["AgeSurveyed"].between(min(age_filter), max(age_filter))]

co11, col2 = st.columns(2)
# Histogram of Height
with co11:
    fig = px.histogram(df, x="Height", color="Gender", marginal="rug")
    st.markdown("Histogram - Height by Gender")
    st.plotly_chart(fig, use_container_width=True)
# Scatter plot Time w/ Family vs. Time Gaming
with col2:
    fig2 = px.scatter(df, x="HrsSpentWithFamily", y="HrsGames", color="Gender")
    st.markdown("Scatter plot - Hours with Family vs Hours Gaming")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4  = st.columns(2)

with col3:
    fig3 = px.parallel_categories(df, dimensions=['Gender','BirthMonth'],color="AgeSurveyed", color_continuous_scale=px.colors.sequential.Inferno)
    st.markdown("Parallel Categories - Gender, Birth Month")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.scatter(df, x="YearSurveyed", y="Armspan", size="HrsChores", log_x=True, size_max=60)
    st.markdown("Bubble Plot - Armspan vs Chores by YearSurveyed")
    st.plotly_chart(fig4, use_container_width=True)