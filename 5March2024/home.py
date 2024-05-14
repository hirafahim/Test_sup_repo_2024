# IMPORT LIBRARIES
#### IMPORT LIBRARIES
import streamlit as st  # For web development
import pandas as pd  # For data manipulation
import plotly.express as px  # For data visualization
import json
import requests
from datetime import datetime, timedelta
import numpy as np
import altair as alt


def app():
    
    alt.themes.enable("dark")

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    #******************************************************************************************************************************************

    ### IMPORT DATA
    # Read the Excel file into a DataFrame (Pre - Processed Data)
    df = pd.read_excel("SupplierBookingReport_With_currency_exchanged.xlsx")
    #df = pd.read_csv("SupplierBookingReport_With_currency_exchanged.csv")

    #******************************************************************************************************************************************

    # Dashboard Title
    
    # st.header('   Supplier Booking Report Live Dashboard')
    # st.markdown('''---''')
    st.header("Detailed Overiew of Supplier Bookings")
    st.markdown('''---''')

    # Top level Filter
    st.subheader('Supplier')
    supplier_filter = st.selectbox('Select the Supplier', pd.unique(df['Provider']))
    

    ## Second level filter
    st.subheader('Booking Date')
    # Define min and max date values
    min_date = df['Booking Date'].min().date()  # Convert to date object
    max_date = df['Booking Date'].max().date()  # Convert to date object

    # Set up date inputs with default values within the allowable range
    default_start_date = min_date
    default_end_date = max_date
    col1,col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', default_start_date, min_value=min_date, max_value=max_date)
    
    with col2:
        end_date = st.date_input('End Date', default_end_date, min_value=min_date, max_value=max_date)

    #*************************************************************************************************************************************************
    # FILTER DATAFRAME BASED ON  SELECTED DATE RANGE AND SUPPLIER
    filtered_df = df[(df['Provider'] == supplier_filter) & (df['Booking Date'] >= pd.Timestamp(start_date)) & (df['Booking Date'] <= pd.Timestamp(end_date))]

    # create a booking column
    filtered_df['Booking'] = filtered_df.groupby('Agent Name')['Agent Name'].transform('count') # Create a booking column agent wise
    #*************************************************************************************************************************************************
    # Detailed View of DataFrame
    df1 = filtered_df[['Reference No.','Country Name', 'Hotel Name','Agent Name','Provider','Check In Date','Check Out Date','Total Price','Supplier Total Price']]
    st.subheader('Overview')
    st.write(df1)
    st.markdown('''---''')