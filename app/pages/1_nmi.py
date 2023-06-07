import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import folium

#global variables
reading_type =['Select a reading type','Export kWh', 'Import kWh', 'Export kVARh', 'Import kVARh', 'Cost ex GST', 'Carbon kg']
nmi_list =['Select a NMI','nmi1','nmi2','nmi3']


# Page: NMI Details

def nmi_page():
    st.title("NMI Details")

    #top  page container
    with st.container():
        st.header('Enter NMI details here')

        #set page columns
        col1, col2 =st.columns(2)

        with col1:
            nmi_in = st.selectbox("Select a NMI", nmi_list)
            read_in = st.selectbox("Select an option", reading_type)

        with col2:
            start_dt_in = st.date_input("Start Date")
            end_dt_in = st.date_input("End Date")

        #add submit button
        if st.button("Submit"):

            #validate nmi and reading inputs
            if nmi_in =='Select a NMI' or read_in == 'Select a reading type':
                st.write('Invalid submission. Try again')

            else:
                st.write('Valid submission')

    
    with st.container():
        st.header("Display map and nmi deets")

        #setup columns
        col1, col2 = st.columns(2)

        #temp values
        address ='83 Mount Street, North Sydney NSW 2060'

        with col1:
            # Geocode address and display map
            if address:
                geolocator = Nominatim(user_agent="my_app")
                location = geolocator.geocode(address)
                if location:
                    latitude, longitude = location.latitude, location.longitude
                    location_df = pd.DataFrame(data=[[latitude,longitude]],columns=['lat','lon'])
                    st.map(location_df)
    
        customer='test customer'

        with col2:
            #create details table
            table_data ={
                'Detail': ['Master Customer','Site Alias','Customer Classification Code', 'Customer Threshold Code', 'Average Daily Load'],
                'Value': [customer, 'test site','test code', 'test code','test load']
            }

            table_df = pd.DataFrame(table_data)

            st.table(table_df)
    #middle page container


nmi_page()