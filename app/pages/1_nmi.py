import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

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
    
    #middle page container


nmi_page()