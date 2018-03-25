#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Saroj Lamichhane
"""

import sqlalchemy
import numpy as np
import pandas as pd


file_name = '//mydir/myfile.csv'

db_server = 'John'
db_name = 'doe'
table_name = 'mytable'

#create sqlalchemy engine

engine = sqlalchemy.create_engine('mssql+pyodbc://'+db_server+'/'+db_name+'?driver=SQL+Server+Native+Client+11.0')

read_dtype = {'Run_date':np.object,
             'Event':np.object,
             'Run_time':np.float64}

#read csv file
df_src = pd.read_csv(file_name, sep = '', header = 0, encoding = 'ISO-8859-1',
                     na_values=['NULL'], keep_default_na = True, engine = 'c',
                     dtype = read_dtype)

#trim last 5 lines of trailer info
df_src = df_src[:-5]

#head(df_src)

#format date column to datetime
df_src['Run_Date'] = pd.to_datetime(df_src['Run_Date'])


#clean up non printable characters in event column
df_src['Event'].str.replace('[^0-9\.\a-z\A-Z]','')


#check for unique run_date in the sql table
chk_date = pd.read_sql_query('SELECT DISTINCT(Run_Date) FROM dbo.'+table_name, engine)

#filter dataframe to exclude any records with the existing run date in DB already
df_fil = df_src.loc[~df_src['Run_Date'].isin(chk_date['Run_Date'].tolist())]

#if filtered dataframe has any valid rows, write to table
if df_fil.count(axis=0)[1]>0:
    df_fil.to_sql(table_name, engine, if_exists = 'append', schema = 'dbo', index = False)
    print('total rows laoded into DB: {}'.format(df_fil.count(axis=0)[1]))
else:
    print('no new dated records available in file.')



