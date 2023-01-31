import pandas as pd
import pyodbc as po
import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pyhocon.converter import HOCONConverter
from pyhocon import ConfigFactory

import warnings
warnings.filterwarnings('ignore')

from query import get_history

## get config
path = os.getcwd()
read_file = path + "/config/config.conf"
conf = ConfigFactory.parse_file(read_file)

## setup connection sql server
server = conf.get("SQL_SERVER.HOST")
driver = conf.get("SQL_SERVER.DRIVER")
database = conf.get("SQL_SERVER.DBNAME")
username = conf.get("SQL_SERVER.USERNAME")
password = conf.get("SQL_SERVER.PASSWORD")


## setup connection  google sheet
path_connection = path + '/connection/'
filename = "project-bram-376319-5129d92e6f6a.json"

def ingest_data_to_gsheet():
        
    conn = po.connect(f'DRIVER={driver};SERVER=' +
        server+';DATABASE='+database+';UID='+username+';PWD=' + password)

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] 
    creds = ServiceAccountCredentials.from_json_keyfile_name(path_connection  + filename, scope) 
    client = gspread.authorize(creds) 

    query = get_history()
    df_history = pd.read_sql(query,conn)

    df_history['StartDate'] = pd.to_datetime(df_history['StartDate']).dt.strftime('%Y-%m-%d')
    df_history['EndDate'] = pd.to_datetime(df_history['EndDate']).dt.strftime('%Y-%m-%d')

    ## Connection Google Sheet
    table_name = conf.get("GOOGLE_SHEET.SHEET_TABLE")
    sheet_name = conf.get("GOOGLE_SHEET.SHEET_NAME")
    file = client.open(table_name) 
    worksheet = file.worksheet(sheet_name) 

    ## export Data to Google Sheet
    worksheet.update([df_history.columns.values.tolist()] + df_history.values.tolist())

    return print("sended to gsheet")


if __name__ == "__main__":
    ingest_data_to_gsheet()