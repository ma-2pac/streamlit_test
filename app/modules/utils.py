'''
Utilities module to assist the streamlit app
'''
from mtatk.api_lib.aemo_api_connector import APIConnector

cert=r"C:\Users\Marco Tupaz\MTA Energy\MTA Energy - Documents\IT\AEMO_CSRs/kv-mta-MTAENERGY-Prod-20221111.pem"


def setup_API_con():

    #create API Connector object
    api_connector=APIConnector(cert=cert)

    return api_connector



api_con = setup_API_con()