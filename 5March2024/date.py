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
    
    st.header('TTV by Date')
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
    # AREA CHART   
    plot_data = ['Amount', 'Supplier Amount']
    plot_height = 400  # Set the height of the chart as needed

    plot_data = ['Amount', 'Supplier Amount']

    # Create an area chart using Plotly Express
    fig = px.area(filtered_df, x='Booking Date', y=plot_data)

    # Add title and axis labels
    fig.update_layout(
        width=1500,  # Set the width of the chart
        height=500 , 
        legend_title_text='Price',  # Add title to the legend
        title='Amount vs Supplier Amount',
        xaxis_title='Booking Date',
        yaxis_title='Price'
    )

    # Display the Plotly area chart
    st.plotly_chart(fig)

    # Add a horizontal rule
    st.markdown('''---''')