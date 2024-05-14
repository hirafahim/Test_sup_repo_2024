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
    
    st.header('Booking Analysis By Agents')
    st.markdown('''---''')
    

    # # Top level Filter
    # st.subheader('Supplier')
    # supplier_filter = st.selectbox('Select the Supplier', pd.unique(df['Provider']))


    # ## Second level filter
    # st.subheader('Booking Date')
    # Define min and max date values
    min_date = df['Booking Date'].min().date()  # Convert to date object
    max_date = df['Booking Date'].max().date()  # Convert to date object

    # Set up date inputs with default values within the allowable range
    default_start_date = min_date
    default_end_date = max_date
    
    col1,col2,col3 = st.columns(3)
    with col1:
        # st.subheader('Supplier')
        supplier_filter = st.selectbox('Select the Supplier', pd.unique(df['Provider']))
    
    with col2:
        # st.subheader('Booking Date')
        start_date = st.date_input('Booking - Start Date', default_start_date, min_value=min_date, max_value=max_date)
    
    with col3:
        # st.subheader('')
        end_date = st.date_input('Booking - End Date', default_end_date, min_value=min_date, max_value=max_date)

    st.markdown('---')
    #*************************************************************************************************************************************************
    # FILTER DATAFRAME BASED ON  SELECTED DATE RANGE AND SUPPLIER
    filtered_df = df[(df['Provider'] == supplier_filter) & (df['Booking Date'] >= pd.Timestamp(start_date)) & (df['Booking Date'] <= pd.Timestamp(end_date))]

    # create a booking column
    filtered_df['Booking'] = filtered_df.groupby('Agent Name')['Agent Name'].transform('count') # Create a booking column agent wise
    
    #**********************************************************************************************************************************************  

    # PLOTs 
    
    st.markdown("### Top 10 Booking Hotels (Most Bookings) ")
    # Sort the filtered DataFrame by 'Booking' column in descending order
    filtered_df['Bookings hotel']=df.groupby('Hotel Name')['No Of Night'].transform('count')
    fil_df = filtered_df[['Hotel Name','Bookings hotel']]
    fil_df = fil_df.drop_duplicates()
    fil_df.rename(columns={'Bookings hotel':'Bookings'},inplace=True)
    fil_df = fil_df.sort_values(by='Bookings', ascending=False)

    # Select top 10 hotels
    top_10_hotels = fil_df.head(20)
    

    st.dataframe(top_10_hotels,
                    column_order=("Hotel Name", "Bookings"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "Hotel Name": st.column_config.TextColumn(
                            "Hotel Name",
                        ),
                        "Bookings": st.column_config.ProgressColumn(
                            "Bookings",
                            format="%f",
                            min_value=0,
                            max_value=max(top_10_hotels.Bookings),
                        )}
                    )
    