# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime
import pymysql.cursors

Connection = pymysql.connect(
    host='23.253.104.69',
    port=3307,
    user='luis.herrera', 
    password='wWxrSRQf', 
    db='moodle_auvi_15aa',
    #charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor 
)

cursor = Connection.cursor()


#-----Regresa usuarios inscritos en materias intro bloque A1-2017

sql1 = " SELECT \
    mdl_groups_members.userid as usrid \
    FROM \
    mdl_groups_members \
    INNER JOIN mdl_user ON mdl_user.id = mdl_groups_members.userid \
    INNER JOIN mdl_groups ON mdl_groups_members.groupid  = mdl_groups.id \
    INNER JOIN mdl_course ON mdl_course.id = mdl_groups.courseid \
    INNER JOIN mdl_enrol ON mdl_enrol.courseid = mdl_groups.courseid \
    INNER JOIN mdl_user_enrolments ON mdl_user_enrolments.enrolid = mdl_enrol.id \
    AND mdl_user_enrolments.userid = mdl_groups_members.userid \
    AND mdl_user.id = mdl_user_enrolments.userid \
    INNER JOIN mdl_context ON mdl_context.instanceid = mdl_groups.courseid \
    INNER JOIN mdl_role_assignments \
    ON mdl_role_assignments.contextid = mdl_context.id \
    AND mdl_role_assignments.userid = mdl_groups_members.userid \
    INNER JOIN mdl_role ON mdl_role.id = mdl_role_assignments.roleid \
    WHERE \
    mdl_user.username not like '%demo%'\
    AND mdl_user.id >= 16687 \
    /* AND mdl_course.category = 224 */\
    AND mdl_user_enrolments.`status` = 0 \
    AND mdl_enrol.courseid in (8911, 8915, 8919, 8923) \
    AND mdl_context.contextlevel = 50 \
    AND mdl_role.id in(5,16) \
    group by mdl_groups_members.userid "

cursor.execute(sql1)

rows = [item['usrid'] for item in cursor]
ids = ",".join(map(str, rows))



#-------------Regresa info de EVENTOS--------------
# 1483941600 is UNIX_DATESTAMP for "2017-01-09"
sql2 = "SELECT mdl_logstore_standard_log.courseid as crsid, \
    mdl_logstore_standard_log.userid as usrid, \
    mdl_logstore_standard_log.eventname, \
    FROM mdl_logstore_standard_log \
    where mdl_logstore_standard_log.userid in ({ids}) \
    and mdl_logstore_standard_log.timecreated < 1483941600".\
    format(**{'ids': ids})

'''
# para pruebas:
sql2 = "SELECT mdl_logstore_standard_log.courseid as crsid, \
mdl_logstore_standard_log.userid as usrid, \
mdl_logstore_standard_log.eventname, \
mdl_logstore_standard_log.component \
FROM mdl_logstore_standard_log \
where mdl_logstore_standard_log.userid in (30489,30490,30491,30492) \
and mdl_logstore_standard_log.timecreated < 1483941600"
'''

cursor.execute(sql2)
event = pd.DataFrame([item for item in cursor])



#-------------Procesamiento de EVENTOS--------------

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
    item = item.replace("submitted", "submit")
    item = item.replace("logged", "log")
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


# Convertir filas a columnas:
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

# Usar esto solo para procesamiento en memoria
# convierte el indice "usrid" a columna del dataframe
# necesario para poder hacer merge con usrid
tmp.reset_index(inplace = True)


#-------------Regresa info de USUARIOS--------------

sql3 = " SELECT \
    mdl_user.id as usrid, \
    from_unixtime(mdl_user.timecreated) as dat_matricula, \
    from_unixtime(mdl_user.firstaccess) as dat_firstac, \
    from_unixtime(mdl_user.lastlogin) as dat_lastlog, \
    from_unixtime(mdl_user.lastaccess) as dat_lastac \
    FROM \
    mdl_user \
    WHERE \
    mdl_user.username not like '%demo%' \
    AND mdl_user.id >= 16687 \
    AND mdl_user.id in ({ids}) \
    ".format(**{'ids': ids})

# regresa info de alumnos
cursor.execute(sql3)
usrinfo = pd.DataFrame([item for item in cursor])



#-------------Procesamiento de USUARIOS--------------

listaTmp = []
for i in range(len(usrinfo)):
    diff = (usrinfo.iloc[i]['dat_firstac'] \
    - usrinfo.iloc[i]['dat_matricula']).days
    listaTmp.append(diff)

usrinfo['tmp_entrar'] = listaTmp



#-------------Merge de info usuarios con eventos--------------

tmp = tmp.merge(usrinfo, left_on = 'usrid', right_on = 'usrid', \
how = 'left')



#-------------Salida a archivo--------------

tmp.to_csv('eventos1.csv', index = False)



Connection.close()
        
        
