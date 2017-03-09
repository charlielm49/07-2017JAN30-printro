# -*- coding: utf-8 -*-

# automatic import with pylab
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 100)
#import manually
import pandas as pd
import seaborn as sns
import pprint

from datetime import datetime
#USB = "TOSH08"
USB = "KING08-NTFS"
#def main():


#----------BEG: READ DATA
# Ruta para PC
#event = pd.read_csv('/ul/UTEL/07-2017JAN30-printro/data/eventos/\
#eventos_bloqueAv42016.csv',

#Previo: leemos catalogo de tipos de curso
event = pd.read_csv('/media/clm/' + USB + '/\
07-2017JAN30-printro/data/eventos/\
eventos_bloqueAv42016.csv',
header = 0,
#usecols = ['catid', 'catknd'],
sep=',')
'''
In [6]: event.head()
Out[6]: 
  crsname  crsid  usrid                        eventname component
0     NaN      0   2928       \core\event\message_viewed      core
1     NaN      0   2928       \core\event\message_viewed      core
2     NaN      0   3021        \core\event\user_loggedin      core
3     NaN      0   3021  \core\event\user_profile_viewed      core
4     NaN      0   3021  \core\event\user_profile_viewed      core
'''

listaTmp = []
for item in event['eventname']:
    #print("before", item)
    #print("find", item.find("\event"))
    item = item.replace("\event", "", 1)
    item = item.replace("\\", "", 1)
    item = item.replace("\\", "-", 2)
    item = item.replace("mod_", "", 1)
    item = item.replace("course", "crs")
    item = item.replace("user", "usr")
    item = item.replace("viewed", "view")
    item = item.replace("submitted", "log")
    item = item.replace("logged", "submit")
    item = item.replace("module", "mod")
    item = item.replace("message", "msg")
    #print("after", item)
    listaTmp.append(item)
    
event['eventname'] = listaTmp


# Se construye una nueva variable conformada por crsid + evento
event['crsevntname'] = ""
listaTmp = []
item = ""
for i in range(len(event['crsevntname'])):
    item = str(event['crsid'][i]) + "-" + event['eventname'][i]
    print(item)
    listaTmp.append(item)
    
event['crsevntname'] = listaTmp


# analisis

event2 = event[['usrid', 'crsevntname', 'component']].\
groupby(['usrid', 'crsevntname']).count()
# converts pandas dataframe multiindex to columns
event2.reset_index(inplace = True)
'''
all are columns:
   usrid              crsevntname  component
0   2928          0-core-msg_view          2
1   3021  0-core-usr_profile_view          4
2   3021      0-core-usr_submitin          1
3   3021          1-core-crs_view          6
4   3021       2666-core-crs_view          1
'''
tmp = event2.pivot_table('component', 'usrid', 'crsevntname')

tmp.to_csv('/media/clm/' + USB + '/\
07-2017JAN30-printro/data/eventos1.csv', index = True)
