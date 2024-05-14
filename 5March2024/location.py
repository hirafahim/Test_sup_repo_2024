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

    st.header("Booking Analysis by Location")
    st.markdown('''---''')

    # Top level Filter
    # st.subheader('Supplier')
    # supplier_filter = st.selectbox('Select the Supplier', pd.unique(df['Provider']))
    # st.markdown('''---''')

    ## Second level filter
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

    #*************************************************************************************************************************************************
    # FILTER DATAFRAME BASED ON  SELECTED DATE RANGE AND SUPPLIER
    filtered_df = df[(df['Provider'] == supplier_filter) & (df['Booking Date'] >= pd.Timestamp(start_date)) & (df['Booking Date'] <= pd.Timestamp(end_date))]

    # create a booking column
    filtered_df['Booking'] = filtered_df.groupby('Agent Name')['Agent Name'].transform('count') # Create a booking column agent wise
    
    #******************************************************************************************************************************************
    
    # Create Json file for countries list
    # Provided countries in the data
    country_names = list(df['Country Name'].unique())

    # Convert the list to JSON format
    json_data = json.dumps(country_names, indent=4)
    # Write the JSON data to a file
    with open("country_names.json", "w") as json_file:
        json_file.write(json_data)
        
    # CHOROPLETH HEATMAP 
    # Create choropleth map using built-in country names and world map
    filtered_df['Agent Bookings'] = filtered_df.groupby('Country Name')['No Of Night'].transform('count')
    
    fig = px.choropleth(locations=filtered_df['Country Name'], 
                        locationmode="country names",
                        color=filtered_df['Agent Bookings'],
                        color_continuous_scale=px.colors.sequential.Reds)
     
                        
    # Display the map
    fig.update_layout(width=1000, height=600)  # Set width and height of the plot
    fig.update_layout(coloraxis_colorbar=dict(title="Bookings"))# define color legend title to "Bookings"
    fig.update_traces(hovertemplate='<b>Country:</b> %{location}<br><b>Bookings:</b> %{z}')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('''---''')