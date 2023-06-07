import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import folium
import plotly.express as px
from streamlit import session_state
import mtatk
import sys

sys.path.insert(0,'..')

from modules.utils import api_con 


#global variables
reading_type =['Select a reading type','Export kWh', 'Import kWh', 'Export kVARh', 'Import kVARh', 'Cost ex GST', 'Carbon kg']
nmi_list =['Select a NMI','2001000645','3050623770','3116638123']



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
                session_state.sub_key=False

            else:
                st.write('Valid submission')
                session_state.sub_key=True

    #middle page container
    with st.container():
        if session_state.sub_key:
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

                #responsible party table
                resp_pty ={
                    'Party': ['placeholder'],
                    'Last Role': ['placeholder'],
                    'Latest From Date': ['placeholder']
                }

                resp_pty_df = pd.DataFrame(resp_pty)

                st.table(resp_pty_df)

    #bottom page container
    with st.container():
        if session_state.sub_key:

            meter_data_df= api_con.get_interval_meter_data(nmi=nmi_in,start_date=start_dt_in, end_date=end_dt_in, grouped_by_nmi=True, drop_estimates=False)
   
            #filter for reading type
            if read_in =='Export kWh':
                export_df=meter_data_df.loc[meter_data_df['nmi_suffix']=='export_kwh']
            else:
                export_df=meter_data_df.loc[meter_data_df['nmi_suffix']=='export_kwh']
            

            # Create line chart with Plotly
            fig = px.line(export_df, x='settlement_datetime', y='reading', title=f'{nmi_in} - {read_in}')

            #render fig
            st.plotly_chart(fig, use_container_width=True)

nmi_page()