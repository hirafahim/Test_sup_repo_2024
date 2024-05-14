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
    
    st.header('Performance Snapshot')
    st.markdown('''---''')
    

    # Top level Filter
    st.subheader('Supplier')
    supplier_filter = st.selectbox('Select the Supplier', pd.unique(df['Provider']))
    #st.markdown('''---''')

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
    st.markdown('''---''')
    st.subheader('Key Indicators')
    #*************************************************************************************************************************************************
    # FILTER DATAFRAME BASED ON  SELECTED DATE RANGE AND SUPPLIER
    filtered_df = df[(df['Provider'] == supplier_filter) & (df['Booking Date'] >= pd.Timestamp(start_date)) & (df['Booking Date'] <= pd.Timestamp(end_date))]

    # create a booking column
    filtered_df['Booking'] = filtered_df.groupby('Agent Name')['Agent Name'].transform('count') # Create a booking column agent wise
    #*************************************************************************************************************************************************
    # FOR KPIs
    # Create INDICATORS

    # Calculate the start date of last week
    start_date_last_week = end_date - timedelta(days=end_date.weekday() + 7)
    start_date_last_week = pd.Timestamp(start_date_last_week)

    end_date = pd.Timestamp(end_date)

    # Filter the DataFrame using .apply() method
    filtered_data = df[(df['Provider'] == supplier_filter) & (df['Booking Date'].apply(lambda x: start_date_last_week <= x <= end_date))]
    # create a booking column
    filtered_data['Booking'] = 1

    #filtered_data.to_excel('last7days.xlsx',index=False) # Save last 7days data in an excel file

    # Get the list of  last 7 days' dates 
    last_7_days_dates = filtered_data['Booking Date'].sort_values(ascending=False).unique()[:7]
    # Initialize an empty dictionary to store the results
    sums_by_date = {'Booking Date': [],'Booking':[], 'No Of Night': [], 'No Of Room': [], 'Amount_GBP':[],'Supplier Amount_GBP':[]}

    for dates in last_7_days_dates:
        Sum_Booking = filtered_data[filtered_data['Booking Date'] == dates]['Booking'].sum()
        sum_nights = filtered_data[filtered_data['Booking Date'] == dates]['No Of Night'].sum() 
        sum_rooms = filtered_data[filtered_data['Booking Date'] == dates]['No Of Room'].sum()
        sum_amount = filtered_data[filtered_data['Booking Date'] == dates]['Amount_GBP'].sum()
        sum_supplier_amount = filtered_data[filtered_data['Booking Date'] == dates]['Supplier Amount_GBP'].sum()
        
        sums_by_date['Booking Date'].append(dates)
        sums_by_date['Booking'].append(Sum_Booking)
        sums_by_date['No Of Night'].append(sum_nights)
        sums_by_date['No Of Room'].append(sum_rooms)
        sums_by_date['Amount_GBP'].append(sum_amount)
        sums_by_date['Supplier Amount_GBP'].append(sum_supplier_amount)

    # Convert the dictionary into a DataFrame
    result_df = pd.DataFrame(sums_by_date)

    # Last week average values
    old_NOB = result_df['Booking'].mean()
    old_NON = result_df['No Of Night'].mean()
    old_NOR = result_df['No Of Room'].mean()
    old_TTV_price = result_df['Amount_GBP'].mean()
    old_TTV_sup = result_df['Supplier Amount_GBP'].mean()

    # Filter data based on today
    today_df = df[(df['Provider'] == supplier_filter) & (df['Booking Date'] == pd.Timestamp(end_date))]
    # Create a booking column
    #today_df['Booking'] = today_df.groupby('Agent Name')['Agent Name'].transform('count') 


    new_NOB = len(today_df)
    new_NON = today_df['No Of Night'].sum()
    new_NOR = today_df['No Of Room'].sum()
    new_TTV_price = today_df['Amount_GBP'].sum()
    new_TTV_sup = today_df['Supplier Amount_GBP'].sum()

    # calculate difference between today values and last week values
    diff_NOB = (new_NOB - old_NOB)
    diff_NON = (new_NON - old_NON)
    diff_NOR = (new_NOR - old_NOR)
    diff_TTV_price = (new_TTV_price - old_TTV_price)
    diff_TTV_sup  = (new_TTV_sup - old_TTV_sup)

    # Calculate KPI values
    #bookings_value = len(filtered_df['Booking'])
    bookings_value = len(filtered_df)
    no_of_night_value = filtered_df['No Of Night'].sum()
    no_of_room_value = filtered_df['No Of Room'].sum()
    ttv_value = round(filtered_df['Amount_GBP'].sum(), 2)

    # Calculate percentage changes
    percentage_change_NOB = round((diff_NOB / old_NOB) * 100, 2)
    percentage_change_NON = round((diff_NON / old_NON) * 100, 2)
    percentage_change_NOR = round((diff_NOR / old_NOR) * 100, 2)
    percentage_change_TTV = round((diff_TTV_price / old_TTV_price) * 100, 2)

    #**************************************************#
    st.caption('Overview')
    kpi1,kpi2,kpi3,kpi5,kpi6,kpi7 = st.columns(6)

        # Define KPIs
        
    kpi1.metric(label="Bookings", value=bookings_value)
    kpi2.metric(label="No. of Night", value=no_of_night_value)
    kpi3.metric(label="No. of Room", value=no_of_room_value)
    #kpi4.metric(label="TTV", value=f"{ttv_value} GBP")

    hotels = filtered_data['Hotel Name'].nunique()
    clients = filtered_df['Agent Name'].nunique()
    country = filtered_df['Country Name'].nunique()

    kpi5.metric(label="No. of Hotels", value=hotels)
    kpi6.metric(label="No. of Agents", value=clients)
    kpi7.metric(label="No. of Countries", value=country)

    st.markdown('''---''')

    #**********************************************************************************************************************************
    st.caption('Today vs Last week')


    kpi8,kpi9,kpi10,kpi11 = st.columns(4)
    bookings = len(today_df)
    nights = today_df['No Of Night'].sum()
    Rooms = today_df['No Of Room'].sum()
    TTV_price = round(today_df['Amount_GBP'].sum(),2)

    kpi8.metric(label="Bookings", value=bookings, delta=f"{percentage_change_NOB}%")
    kpi9.metric(label="Total Nights", value=nights, delta=f"{percentage_change_NON}%")
    kpi10.metric(label="Total Rooms", value=Rooms, delta=f"{percentage_change_NOR}%")
    kpi11.metric(label="TTV", value=f"{TTV_price} GBP", delta=f"{percentage_change_TTV}%")
    