# -*- coding: utf-8 -*-
"""Google Sheets API.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZDjUhkUfdCyiHpdUv9qDqQX83vlv3gl3
"""

import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from pandas.io.json import json_normalize

import os
import pathlib

# Set-up environment variables
SCOPE = ['https://spreadsheets.google.com/feeds']
SPREADSHEET_ID = '1pbqhF89ldy350pyidcUQGONrjSoeLKgaJRiZV5oVVOw'

# Credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', SCOPE)

# More setups
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

#from app import cell_line
cell_line = 1

def extract_all(cell_line):
    # Create a table from the sheets
    range_name = f'{cell_line}!A1:N999'
    result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    
    #Create panda dataframe
    df = pd.DataFrame(result['values'])

    #grab the first row for the header
    new_header = df.iloc[0] 
    df.columns = new_header

    #take the data less the header row
    df = df[1:]
    return df

#extract_all(f'Cell Line {cell_line}')


#Extract specific information from certain criovial name
def extract_spec(cell_line, criov_name):
    """
    """
    df = extract_all(cell_line)
    return df[df.iloc[:,0] == criov_name]

#extract_spec("Cell Line 1","abc")

## Append values into sheets
def create_data(criov_name,date,cell_passage,viability,init_conc,init_vol,fin_conc,fin_vol,obs,info):
    """
    Aim: Add '' spaces in between variables. Create a list that can directly update into google sheets
    """
    data = [criov_name,date,'',cell_passage,viability,init_conc,init_vol,'',fin_conc,fin_vol,'','',obs,info]
    return data

def append(cell_line, new_data):
    """
    Aim: Update new_data into a specific cell line in our google sheets
    """
    #specify range name: From column A to N, after row 2
    range_name = f'{cell_line}!A2:N2' 
    data = new_data
    #print(data)
    #update google sheet
    res = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=range_name,valueInputOption = "USER_ENTERED",insertDataOption = "INSERT_ROWS",body={"values":[data]}).execute()


#TEST
cell_line = "Cell Line 1"
test_data = create_data('abc1',
        '22/05/22',
        'hello',
        '94',
        '0.95',
        '10',
        '0.95',
        '10',
        'Medium yellow. Change of medium. '
        ,'hello')

append(cell_line,test_data)

#append("Cell Line 1",)
#print(extract_all('Cell line 1'))

def retrieve_titles():
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    titles = [sheets[i].get("properties", {}).get("title", "Sheet1") for i in range(0,len(sheets))]
    return titles

#import numpy as np
#print(list(np.unique(extract_all('Cell Line 1')['Criovial information'].values)))