import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import folium
import plotly.express as px
from streamlit import session_state

#global variables
reading_type =['Select a reading type','Export kWh', 'Import kWh', 'Export kVARh', 'Import kVARh', 'Cost ex GST', 'Carbon kg']
nmi_list =['Select a NMI','nmi1','nmi2','nmi3']

def init_session_state():
    
    if 'sub_key' not in session_state:
        session_state['sub_key'] = False

    return session_state


# Page: NMI Details

def nmi_page():
    submit_valid = init_session_state()
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
                submit_valid.sub_key=False

            else:
                st.write('Valid submission')
                submit_valid.sub_key=True

    #middle page container
    with st.container():
        if submit_valid.sub_key:
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

    #bottom page container
    with st.container():
        if submit_valid.sub_key:

            #setup cols
            col1, col2 = st.columns(2)

            with col1:

                #responsible party table
                resp_pty ={
                    'Party': ['placeholder'],
                    'Last Role': ['placeholder'],
                    'Latest From Date': ['placeholder']
                }

                resp_pty_df = pd.DataFrame(resp_pty)

                st.table(resp_pty_df)

            with col2:
                
                #sample data
                data ={
                    'date': pd.date_range(start='2023-01-01',end='2023-12-31',freq='D'),
                    'value': range(365)
                }

                chart_df = pd.DataFrame(data)

                # Create line chart with Plotly
                fig = px.line(chart_df, x='date', y='value', title=f'{nmi_in} {read_in}')

                #render fig
                st.plotly_chart(fig)

nmi_page()