import pyodbc as po
import pandas as pd
import gspread as gs
import os

from pandas.io import gbq
from pyhocon.converter import HOCONConverter
from pyhocon import ConfigFactory

from query import get_employee

path = os.getcwd()
read_file = path + "/config/config.conf"
conf = ConfigFactory.parse_file(read_file)

## setup connection sql server
server = conf.get("SQL_SERVER.HOST")
driver = conf.get("SQL_SERVER.DRIVER")
database = conf.get("SQL_SERVER.DBNAME")
username = conf.get("SQL_SERVER.USERNAME")
password = conf.get("SQL_SERVER.PASSWORD")

path_connection = path + '/connection/'
url = conf.get("GOOGLE_SHEET.URL")
s_name = conf.get("GOOGLE_SHEET.SHEET_NAME")

def send_to_bigquery():
    conn = po.connect(f'DRIVER={driver};SERVER=' +
    server+';DATABASE='+database+';UID='+username+';PWD=' + password)

## get data from sql server 
    query = get_employee()

    ## get data from google sheet
    filename = "project-bram-376319-5129d92e6f6a.json"
    gsheet_url = url
    sheet_name = s_name

    gc = gs.service_account(path_connection + filename)
    sh = gc.open_by_url(gsheet_url)
    ws = sh.worksheet(sheet_name)

    data_history = pd.DataFrame(ws.get_all_records())
    data_employee = pd.read_sql(query,conn)

    ## Transform and join section
    data_employee['BirthDate'] = pd.to_datetime(data_employee['BirthDate']).dt.strftime('%Y-%m-%d')
    data_history['EmployeeId'] = data_history['EmployeeId'].apply(str)

    df = data_employee.merge(data_history,
                    left_on='EmployeeId', right_on='EmployeeId', how='inner')
                    
    df.to_gbq(destination_table="report_dataset.reporting",
                        project_id="project-bram-376319",
                        if_exists='replace')

    return print("Successfully Ingest Data To Big Query")