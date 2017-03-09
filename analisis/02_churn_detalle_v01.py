# -*- coding: utf-8 -*-

# automatic import with pylab
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_rows', 1000)
#import manually
import pandas as pd
import seaborn as sns
import pprint

from datetime import datetime
#USB = "TOSH08"
USB = "KING08-NTFS"
#def main():

#----------BEG: READ DATA


# ---CATÁLOGO DE TIPO CURSO---

#Previo: leemos catalogo de tipos de curso
#crseid = pd.read_csv('/media/clm/TOSH08/04-2016DEC02-tiempos_de_vida/\
#data/act_iniciales_v2/crse_ids.csv',
crseid = pd.read_csv('/media/clm/' + USB + '/04-2016DEC02-tiempos_de_vida/\
data/act_iniciales_v2/crse_ids.csv',
header = 0,
usecols = ['catid', 'catknd'],
sep=',')



# ---ASSIGNMENT---

#asspre = pd.read_csv('/media/clm/TOSH08/07-2016JAN30-printro/data/\
asspre = pd.read_csv('/media/clm/KING08-NTFS/07-2016JAN30-printro/data/\
ass.csv',
header = 0,
usecols = ['tipo', 'actdate', 'usrid', 'crsid', 'catid'], 
sep=',')
asspre['actdate'] = pd.to_datetime(asspre['actdate'], format='%Y-%m-%d')

# works ok, but it also works without copy:
#ass = ass.drop_duplicates().copy()
asspre = asspre.drop_duplicates()

#pegarle el catknd
#We reassign the field catknd becaise we have some inconsistencies
# crseid = 8267 has Talleres and Curr
ass = asspre.merge(crseid, left_on="catid", right_on="catid", \
    how='left')




# ---EXAMEN---
#exapre = pd.read_csv('/media/clm/TOSH08/07-2016JAN30-printro/data/\
exapre = pd.read_csv('/media/clm/KING08-NTFS/07-2016JAN30-printro/data/\
quiz.csv',
header = 0,
usecols = ['tipo', 'actdate', 'usrid', 'crsid', 'catid'], 
sep=',')
exapre['actdate'] = pd.to_datetime(exapre['actdate'], format='%Y-%m-%d')

# OJO: la información no duplicada nospuede sevir para análisis para
# diferemtes materias
exapre = exapre.drop_duplicates()

exa = exapre.merge(crseid, left_on="catid", right_on="catid", \
    how='left')



# ---FOROS---

#foropre = pd.read_csv('/media/clm/TOSH08/07-2016JAN30-printro/data/\
foropre = pd.read_csv('/media/clm/KING08-NTFS/07-2016JAN30-printro/data/\
foro.csv',
header = 0,
usecols = ['tipo', 'actdate', 'usrid', 'crsid', 'catid'], 
sep=',')
foropre['actdate'] = pd.to_datetime(foropre['actdate'], format='%Y-%m-%d')

foropre = foropre.drop_duplicates()

#pegarle el catknd
foro = foropre.merge(crseid, left_on="catid", right_on="catid", \
    how='left')


#JUNTAMOS TODOS LOS ARCHIVOS
alldat = exa.append(ass).append(foro)



# ------------Analisis para Introductorios 2017----------

##Previo: leemos usrs enrolados de introductorios 2017
#usrintro = pd.read_csv('/media/clm/TOSH08/07-2016JAN30-printro/data/\
usrintro = pd.read_csv('/media/clm/KING08-NTFS/07-2016JAN30-printro/data/\
usrs_introd-A2017.csv',
header = 0,
usecols = ['usrid', 'enroldate'],
sep=',')
usrintro['enroldate'] = pd.to_datetime(usrintro['enroldate'], \
format='%Y-%m-%d')
# ESTE archivo contiene REINGRESOS

# Tenemos que quitar los reingresos
# 1) Esto es para identificar a los reingresos
#le pegamos la fecha de introductorios para identificar activ de introds
alldat2 = alldat.merge(usrintro, left_on='usrid', right_on='usrid', \
how= 'left').copy()
# condiciones para identificar reingresos: 1 actividades 
# de todas las materias (actdate) previas a intro
#ada3 = alldat2[ pd.notnull(alldat2['enroldate']) & \
#(alldat2['actdate'] < "2017-01-02" ) ]
# We need to add the begin date of introductory courses to eliminate
# people with curriculares before begin of introductorias
ada3 = alldat2[ pd.notnull(alldat2['enroldate']) & \
(alldat2['actdate'] < "2017-01-19" ) ] # sumamos 10 dias a fecha inicio
# esto es para detectar a los que estan llevando simultaneamente intro
# con curriculares. Inicio: 2017-01-09

# condiciones para identificar reingresos: 3 actividades en curriculares
reingresos = ada3[ada3['catknd'] == "Curr"]
reingresos = reingresos['usrid'].drop_duplicates() # converts to series

# 2) Quitamos reingresos de archivo de studnts de introd
# 2a) pegamos reingresos a archivo de studnts de introd
reingresos = reingresos.reset_index() # we must convert series to df
# we choose isnull because we just added the reingresos
# so, nulls are the not reingresos
usrintro = usrintro[pd.isnull(usrintro.merge(reingresos, left_on = 'usrid', \
right_on = 'usrid', how = 'left')['index'])]

#En este punto usrintro ya no contiene REINGRESOS
# son usrs unicos antes de empezar introductorios

#Ahora, nos quedamos solamente con actividades de introds
alldat2 = alldat.merge(usrintro, left_on='usrid', right_on='usrid', \
how= 'left').copy()
actintro = alldat2[pd.notnull(alldat2['enroldate'])]

len(actintro['usrid'].drop_duplicates())
# En este punto, tenemos 992 estudiantes que son intro (no reingreso)

# Estos son los que estan activos despues del inico del curso introductorio
len(actintro[actintro['actdate'] > "2017-01-09"]['usrid'].drop_duplicates())
#Out[33]: 976




# ------------Analisis para Introductorios 2016----------

##Previo: leemos usrs enrolados de introductorios 2017
usrintro = pd.read_csv('/media/clm/TOSH08/07-2016JAN30-printro/data/\
usrs_introd-A2016.csv',
header = 0,
usecols = ['usrid', 'enroldate'],
sep=',')
usrintro['enroldate'] = pd.to_datetime(usrintro['enroldate'], \
format='%Y-%m-%d')
# ESTE archivo contiene REINGRESOS


# Tenemos que quitar los reingresos
# 1) Esto es para identificar a los reingresos
#le pegamos la fecha de introductorios para identificar activ de introds
alldat2 = alldat.merge(usrintro, left_on='usrid', right_on='usrid', \
how= 'left').copy()
# condiciones para identificar reingresos: 1 actividades 
# de todas las materias (actdate) previas a inico intro
#ada3 = alldat2[ pd.notnull(alldat2['enroldate']) & \
#(alldat2['actdate'] < "2017-01-02" ) ]
# We need to add the begin date of introductory courses to eliminate
# people with curriculares before begin of introductorias
ada3 = alldat2[ pd.notnull(alldat2['enroldate']) & \
(alldat2['actdate'] < "2016-01-21" ) ] # sumamos 10 dias a fecha inicio
# esto es para detectar a los que estan llevando simultaneamente intro
# con curriculares. Inicio: 2017-01-11

# condiciones para identificar reingresos: 3 actividades en curriculares
reingresos = ada3[ada3['catknd'] == "Curr"]
reingresos = reingresos['usrid'].drop_duplicates() # converts to series
# 2) Quitamos reingresos de archivo de studnts de introd
# 2a) pegamos reingresos a archivo de studnts de introd
reingresos = reingresos.reset_index() # we must convert series to df
# we choose isnull because we just added the reingresos
# so, nulls are the not reingresos
usrintro = usrintro[pd.isnull(usrintro.merge(reingresos, \
left_on = 'usrid', right_on = 'usrid', how = 'left')['index'])]

#En este punto usrintro ya no contiene REINGRESOS
# son usrs unicos antes de empezar introductorios

#Ahora, nos quedamos solamente con actividades de introds
alldat2 = alldat.merge(usrintro, left_on='usrid', right_on='usrid', \
how= 'left').copy()
actintro = alldat2[pd.notnull(alldat2['enroldate'])]

len(actintro['usrid'].drop_duplicates())
'''
In [62]: len(actintro)
Out[62]: 65945

In [63]: len(actintro['usrid'].drop_duplicates())
Out[63]: 829

#guardamos los bloques
actintro['block'] = "A1-2016"
'''
A16.to_csv("/media/clm/TOSH08/07-2016JAN30-printro/data/\
A16-analisis.txt", index=False)


# Estos son los que estan activos despues del inico del curso introductorio
len(actintro[actintro['actdate'] > "2016-01-11"]['usrid'].drop_duplicates())
#Out[33]: 823


#---


# ------------- eventos -----------------

# leemos los eventos y sus usuarios que los realizan
usrevent2016 = pd.read_excel('/media/clm/TOSH08/07-2016JAN30-printro/\
data/eventos_bloque_A-v3.xlsx',
header = 0,
#usecols = ['usrid', 'event', 'component'],
sheetname=0)





















#NUNCAS
# Leemos los nuncas
nuncaspre = pd.read_csv('/media/clm/TOSH08/05-2016DEC19-churn/data/nuncas_c_introd.txt',
header = 0,
usecols = ['usrid', 'crsid'],  
sep='|')


# leemos archivo de materias
matints = pd.read_csv('/media/clm/TOSH08/04-2016DEC02-tiempos_de_vida/data/matints.csv',
header = 0,
usecols = ['crsid', 'inistart', 'catid'],
sep=';')
matints['inistart'] = pd.to_datetime(matints['inistart'], \
format='%d-%b-%y')
# original format: dd-mmm-yy
matints = matints[['crsid', 'inistart']]


#eesto se hizo para pasarle a charlei lo que hicieron solo bienvenida
z = alldat[['usrid', 'catknd', 'crsid']]           
z2 = z.pivot_table(index = 'usrid', columns = 'catknd', values = 'crsid')
z2 = z2[['Bienvenida', 'Curr', 'Intro']]                      
z3 = z2[pd.notnull(z2['Bienvenida']) & pd.isnull(z2['Curr']) & pd.isnull(z2['Intro'])]



# le pegamos la fecha a los nuncas
nuncas = nuncaspre.merge(matints, left_on = "crsid", right_on = "crsid",\
 how = "left")

# le pegamos la fecha correcta de inicio de introductorios
alldat2 = alldat.merge(matints, left_on = "crsid", right_on = "crsid",\
 how = "left")

alldatdedupPre = alldat2[alldat2['catknd'] == "Intro"][['usrid', 'inistart']]
alldatdedup = alldatdedupPre.groupby(['usrid']).max()
alldatdedup.reset_index(level=0, inplace=True)


# Le pegamos los nuncas



'''
# parece que ya teniamos esta informacion en la tabla con IntroIni
# pegar fechas de cursos
fecini = pd.read_excel('/media/clm/TOSH08/04-2016DEC02-tiempos_de_vida/data/materias_introductorias.xlsx',
usecols = ['id', 'FROM_UNIXTI'],
header = 0)


alldat = alldat.merge(fecini, left_on="crsid", \
        right_on="id", how='left')
'''
        

#---OBTENER FECHA MÍNIMA

a = alldat[['usrid', 'date', 'catknd']].groupby(['usrid', 'catknd']).min()
a = a.unstack() # this can be done at the end of the previous line
a.columns = a.columns.droplevel(0)
# to check num records: len(a.index.values)
# solo tomamos 4 [nos quedamos con 3: clm: 2017-JAN-06]
#a = a[['Bienvenida', 'Intro', 'Curr', 'Talleres']]
a = a[['Bienvenida', 'Intro', 'Curr']]
#a.columns = ['BienvMax', 'IntroMax', 'CurrMax', 'TallMax']
a.columns = ['BienvMin', 'IntroMin', 'CurrMin']
# volvemos el índice columna: NOTA: esto solo se hace si NO se guarda 
#el archivo
a['usrid'] = a.index 
# Out[237]: 
# categ_kind Bienvenida      Intro       Curr Talleres
# userid                                              
# 16887             NaT 2015-01-13        NaT      NaT
# 16888             NaT 2015-01-15 2015-03-23      NaT
# ...

#a.to_csv('minDates.csv')



#---OBTENER FECHA MÁXIMA

b = alldat[['usrid', 'date', 'catknd']].groupby(['usrid', 'catknd']).max()
b = b.unstack() # this can be done at the end of the previous line
b.columns = b.columns.droplevel(0)
# to check num records: len(a.index.values)
# solo tomamos 4 [nos quedamos con 3: clm: 2017-JAN-06]
#b = b[['Bienvenida', 'Intro', 'Curr', 'Talleres']]
b = b[['Bienvenida', 'Intro', 'Curr']]
#b.columns = ['BienvMax', 'IntroMax', 'CurrMax', 'TallMax']
b.columns = ['BienvMax', 'IntroMax', 'CurrMax']
# volvemos el índice columna: NOTA: esto solo se hace si NO se guarda 
#el archivo
b['usrid'] = b.index 
# Out[119]: 
# catknd Bienvenida      Intro       Curr Talleres
# usrid                                           
# 16887         NaT 2015-12-01        NaT      NaT
# 16888         NaT 2015-12-01 2015-12-04      NaT
# 16889  2015-12-01 2015-12-01        NaT      NaT


#b.to_csv('maxDates.csv')

'''
#---Pruebas no se usa OBTENER TODAS LAS FECHAS (info para Ricchard) 
# c es el archivo con todas las fechas 
# PRUEBA - no se usa
c['count'] = 1
c = c.pivot_table('count', 'usrid', 'date')
c.reset_index(level = 0, inplace = True) # to convert index to column
# 730 date columns
'''


#---PEGAMOS MÍN y MÁX o TODAS

# abrimos el archivo de alumnos para pegarle maximas y minimas fechas
usr = pd.read_csv('/media/clm/TOSH08/04-2016DEC02-tiempos_de_vida/data/tmpo_vida01-full_v2.csv',
header = 0,
sep=',')
usr['registro'] = pd.to_datetime(usr['registro'], format='%m/%d/%Y')
usr['accessFirst'] = pd.to_datetime(usr['accessFirst'], format='%m/%d/%Y')
usr['introIni'] = pd.to_datetime(usr['introIni'], format='%m/%d/%Y')
usr['activPrim'] = pd.to_datetime(usr['activPrim'], format='%m/%d/%Y')

# CHOOSE according to project: a, b are min & max dates for analysis
# CHOOSE c for richard
usr = usr.merge(a, left_on="usrid", right_on="usrid", how='left')
usr = usr.merge(b, left_on="usrid", right_on="usrid", how='left')
# Esto solo sirve cuando las fechas estan por columnas 
#usr = usr.merge(c, left_on="usrid", right_on="usrid", how='left')

usr = usr.merge(alldatdedup, left_on="usrid", right_on="usrid", how='left')
#tday's date
# datetime.now().strftime('%Y-%b-%d')

# Ponemos valores de bloques
usr['block'] = "NA" # valor default
#usr['block'] = "" # valor default

usr.loc[(usr['IntroMin'] >= "2016-01-11") & \
(usr['IntroMin'] < "2016-01-25") , ['block']] = "A1"
usr.loc[(usr['IntroMin'] >= "2016-01-25") & \
(usr['IntroMin'] < "2016-02-08") , ['block']] = "B1"
usr.loc[(usr['IntroMin'] >= "2016-02-08") & \
(usr['IntroMin'] < "2016-02-22") , ['block']] = "C1"
usr.loc[(usr['IntroMin'] >= "2016-02-22") & \
(usr['IntroMin'] < "2016-03-07") , ['block']] = "D1"

usr.loc[(usr['IntroMin'] >= "2016-03-07") & \
(usr['IntroMin'] < "2016-03-28") , ['block']] = "A2"
usr.loc[(usr['IntroMin'] >= "2016-03-28") & \
(usr['IntroMin'] < "2016-04-11") , ['block']] = "B2"
usr.loc[(usr['IntroMin'] >= "2016-04-11") & \
(usr['IntroMin'] < "2016-04-25") , ['block']] = "C2"
usr.loc[(usr['IntroMin'] >= "2016-04-25") & \
(usr['IntroMin'] < "2016-05-09") , ['block']] = "D2"

usr.loc[(usr['IntroMin'] >= "2016-05-09") & \
(usr['IntroMin'] < "2016-05-23") , ['block']] = "A3"
usr.loc[(usr['IntroMin'] >= "2016-05-23") & \
(usr['IntroMin'] < "2016-06-06") , ['block']] = "B3"
usr.loc[(usr['IntroMin'] >= "2016-06-06") & \
(usr['IntroMin'] < "2016-06-20") , ['block']] = "C3"
usr.loc[(usr['IntroMin'] >= "2016-06-20") & \
(usr['IntroMin'] < "2016-07-04") , ['block']] = "D3"

usr.loc[(usr['IntroMin'] >= "2016-07-04") & \
(usr['IntroMin'] < "2016-07-18") , ['block']] = "A4"
usr.loc[(usr['IntroMin'] >= "2016-07-18") & \
(usr['IntroMin'] < "2016-08-01") , ['block']] = "B4"
usr.loc[(usr['IntroMin'] >= "2016-08-01") & \
(usr['IntroMin'] < "2016-08-15") , ['block']] = "C4"
usr.loc[(usr['IntroMin'] >= "2016-08-15") & \
(usr['IntroMin'] < "2016-09-05") , ['block']] = "D4"

usr.loc[(usr['IntroMin'] >= "2016-09-05") & \
(usr['IntroMin'] < "2016-09-19") , ['block']] = "A5"
usr.loc[(usr['IntroMin'] >= "2016-09-19") & \
(usr['IntroMin'] < "2016-10-03") , ['block']] = "B5"
usr.loc[(usr['IntroMin'] >= "2016-10-03") & \
(usr['IntroMin'] < "2016-10-17") , ['block']] = "C5"
usr.loc[(usr['IntroMin'] >= "2016-10-17") & \
(usr['IntroMin'] < "2016-10-31") , ['block']] = "D5"

usr.loc[(usr['IntroMin'] >= "2016-10-31") & \
(usr['IntroMin'] < "2016-11-14") , ['block']] = "A6"
usr.loc[(usr['IntroMin'] >= "2016-11-14") & \
(usr['IntroMin'] < "2016-11-28") , ['block']] = "B6"
usr.loc[(usr['IntroMin'] >= "2016-11-28") & \
(usr['IntroMin'] < "2016-12-12") , ['block']] = "C6"
usr.loc[(usr['IntroMin'] >= "2016-12-12") & \
(usr['IntroMin'] < "2017-01-09") , ['block']] = "D6"


#Ahora usamos introIni para ponerle algunas de las fechas faltantes a
# introMin

usr.loc[(usr['introIni'] >= "2016-01-11") & \
(usr['introIni'] < "2016-01-25") & \
(usr['block'] == "NA") \
, ['block']] = "A1"
usr.loc[(usr['introIni'] >= "2016-01-25") & \
(usr['introIni'] < "2016-02-08") & \
(usr['block'] == "NA") \
, ['block']] = "B1"
usr.loc[(usr['introIni'] >= "2016-02-08") & \
(usr['introIni'] < "2016-02-22") & \
(usr['block'] == "NA") \
, ['block']] = "C1"
usr.loc[(usr['introIni'] >= "2016-02-22") & \
(usr['introIni'] < "2016-03-07") & \
(usr['block'] == "NA") \
, ['block']] = "D1"

usr.loc[(usr['introIni'] >= "2016-03-07") & \
(usr['introIni'] < "2016-03-28") & \
(usr['block'] == "NA") \
, ['block']] = "A2"
usr.loc[(usr['introIni'] >= "2016-03-28") & \
(usr['introIni'] < "2016-04-11") & \
(usr['block'] == "NA") \
, ['block']] = "B2"
usr.loc[(usr['introIni'] >= "2016-04-11") & \
(usr['introIni'] < "2016-04-25") & \
(usr['block'] == "NA") \
, ['block']] = "C2"
usr.loc[(usr['introIni'] >= "2016-04-25") & \
(usr['introIni'] < "2016-05-09") & \
(usr['block'] == "NA") \
, ['block']] = "D2"

usr.loc[(usr['introIni'] >= "2016-05-09") & \
(usr['introIni'] < "2016-05-23") & \
(usr['block'] == "NA") \
, ['block']] = "A3"
usr.loc[(usr['introIni'] >= "2016-05-23") & \
(usr['introIni'] < "2016-06-06") & \
(usr['block'] == "NA") \
, ['block']] = "B3"
usr.loc[(usr['introIni'] >= "2016-06-06") & \
(usr['introIni'] < "2016-06-20") & \
(usr['block'] == "NA") \
, ['block']] = "C3"
usr.loc[(usr['introIni'] >= "2016-06-20") & \
(usr['introIni'] < "2016-07-04") & \
(usr['block'] == "NA") \
, ['block']] = "D3"

usr.loc[(usr['introIni'] >= "2016-07-04") & \
(usr['introIni'] < "2016-07-18") & \
(usr['block'] == "NA") \
, ['block']] = "A4"
usr.loc[(usr['introIni'] >= "2016-07-18") & \
(usr['introIni'] < "2016-08-01") & \
(usr['block'] == "NA") \
, ['block']] = "B4"
usr.loc[(usr['introIni'] >= "2016-08-01") & \
(usr['introIni'] < "2016-08-15") & \
(usr['block'] == "NA") \
, ['block']] = "C4"
usr.loc[(usr['introIni'] >= "2016-08-15") & \
(usr['introIni'] < "2016-09-05") & \
(usr['block'] == "NA") \
, ['block']] = "D4"

usr.loc[(usr['introIni'] >= "2016-09-05") & \
(usr['introIni'] < "2016-09-19") & \
(usr['block'] == "NA") \
, ['block']] = "A5"
usr.loc[(usr['introIni'] >= "2016-09-19") & \
(usr['introIni'] < "2016-10-03") & \
(usr['block'] == "NA") \
, ['block']] = "B5"
usr.loc[(usr['introIni'] >= "2016-10-03") & \
(usr['introIni'] < "2016-10-17") & \
(usr['block'] == "NA") \
, ['block']] = "C5"
usr.loc[(usr['introIni'] >= "2016-10-17") & \
(usr['introIni'] < "2016-10-31") & \
(usr['block'] == "NA") \
, ['block']] = "D5"

usr.loc[(usr['introIni'] >= "2016-10-31") & \
(usr['introIni'] < "2016-11-14") & \
(usr['block'] == "NA") \
, ['block']] = "A6"
usr.loc[(usr['introIni'] >= "2016-11-14") & \
(usr['introIni'] < "2016-11-28") & \
(usr['block'] == "NA") \
, ['block']] = "B6"
usr.loc[(usr['introIni'] >= "2016-11-28") & \
(usr['introIni'] < "2016-12-12") & \
(usr['block'] == "NA") \
, ['block']] = "C6"
usr.loc[(usr['introIni'] >= "2016-12-12") & \
(usr['introIni'] < "2017-01-09") & \
(usr['block'] == "NA") \
, ['block']] = "D6"



# se eliminan los registros que no pueden entrar a sus curriculares
# fecha ini INTRO >= 31 oct 2016 (estos entran hasta el 9 de enero)
# esto no funciona (?): usr = usr[usr['IntroMin'] <= "2016-10-31"] 
usr = usr[usr['IntroMin'] < "2016-10-31"].append(usr[pd.isnull(usr['IntroMin']) ])





# Aqui analizamos archivo para Richard
'''
INICIOS DE BLOQUES
usr.loc[(usr['introIni'] >= "2016-01-11") & = "A1"
usr.loc[(usr['introIni'] >= "2016-01-25") & = "B1"
usr.loc[(usr['introIni'] >= "2016-02-08") & = "C1"
usr.loc[(usr['introIni'] >= "2016-02-22") & = "D1"

usr.loc[(usr['introIni'] >= "2016-03-07") & = "A2"
usr.loc[(usr['introIni'] >= "2016-03-28") & = "B2"
usr.loc[(usr['introIni'] >= "2016-04-11") & = "C2"
usr.loc[(usr['introIni'] >= "2016-04-25") & = "D2"

usr.loc[(usr['introIni'] >= "2016-05-09") & = "A3"
usr.loc[(usr['introIni'] >= "2016-05-23") & = "B3"
usr.loc[(usr['introIni'] >= "2016-06-06") & = "C3"
usr.loc[(usr['introIni'] >= "2016-06-20") & = "D3"

usr.loc[(usr['introIni'] >= "2016-07-04") & = "A4"
usr.loc[(usr['introIni'] >= "2016-07-18") & = "B4"
usr.loc[(usr['introIni'] >= "2016-08-01") & = "C4"
usr.loc[(usr['introIni'] >= "2016-08-15") & = "D4"

usr.loc[(usr['introIni'] >= "2016-09-05") & = "A5"
usr.loc[(usr['introIni'] >= "2016-09-19") & = "B5"
usr.loc[(usr['introIni'] >= "2016-10-03") & = "C5"
usr.loc[(usr['introIni'] >= "2016-10-17") & = "D5"

usr.loc[(usr['introIni'] >= "2016-10-31") & = "A6"
usr.loc[(usr['introIni'] >= "2016-11-14") & = "B6"
usr.loc[(usr['introIni'] >= "2016-11-28") & = "C6"
usr.loc[(usr['introIni'] >= "2016-12-12") & = "D6"
'''



# REVISAR ESTO Y REPETIR CON: c = usrid, fecha y tipo curso
# Aqui analizamos archivo para Richard

c = alldat[['usrid', 'date']]
blocks = usr[['usrid', 'block']].copy()
# Este merg esolo sepuede hacer si hay renglones unicos por usuario
# en el archivo "c" 
# ^^ - COMENATRIO mal: si se puede para "c" porque el block es solo una 
#etiqueta 
d = c.merge(blocks, left_on="usrid", right_on="usrid", how='left')


####A1###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "A1"]['usrid'].value_counts())
#A1-FINBIM1
#filtramos aquellos con actividad posterior a inicio de introductorio (parti.)
len(d[(d['date'] > "2016-01-11") & (d['block'] == "A1")]['usrid'].value_counts())

####B1###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "B1"]['usrid'].value_counts())
#B1-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-01-25") & (d['block'] == "B1")]['usrid'].value_counts())

####C1###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "C1"]['usrid'].value_counts())
#B1-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-02-08") & (d['block'] == "C1")]['usrid'].value_counts())

####D1###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "D1"]['usrid'].value_counts())
#D1-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-02-22") & (d['block'] == "D1")]['usrid'].value_counts())

####A2###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "A2"]['usrid'].value_counts())
#A2-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-03-07") & (d['block'] == "A2")]['usrid'].value_counts())

####B2###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "B2"]['usrid'].value_counts())
#B2-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-03-28") & (d['block'] == "B2")]['usrid'].value_counts())

####C2###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "C2"]['usrid'].value_counts())
#C2-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-03-11") & (d['block'] == "C2")]['usrid'].value_counts())

####D2###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "D2"]['usrid'].value_counts())
#D2-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-03-25") & (d['block'] == "D2")]['usrid'].value_counts())

#cantidades iniciales de gente en el bloque
len(d[d['block'] == "A3"]['usrid'].value_counts())
#A3-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-05-09") & (d['block'] == "A3")]['usrid'].value_counts())

####B3###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "B3"]['usrid'].value_counts())
#B3-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-05-23") & (d['block'] == "B3")]['usrid'].value_counts())

####C3###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "C3"]['usrid'].value_counts())
#C3-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-06-06") & (d['block'] == "C3")]['usrid'].value_counts())

####D3###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "D3"]['usrid'].value_counts())
#D3-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-06-20") & (d['block'] == "D3")]['usrid'].value_counts())

####A4###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "A4"]['usrid'].value_counts())
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-07-04") & (d['block'] == "A4")]['usrid'].value_counts())

####B4###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "B4"]['usrid'].value_counts())
#B4-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-07-18") & (d['block'] == "B4")]['usrid'].value_counts())

####C4###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "C4"]['usrid'].value_counts())
#C4-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-08-01") & (d['block'] == "C4")]['usrid'].value_counts())

####D4###
#cantidades iniciales de gente en el bloque
len(d[d['block'] == "D4"]['usrid'].value_counts())
#D4-FINBIM2
#filtramos aquellos con actividad posterior a inicio de 2o bim. (parti.)
len(d[(d['date'] > "2016-08-15") & (d['block'] == "D4")]['usrid'].value_counts())





if __name__ == '__main__':
    main()


'''
import numpy as np
# examples using a.item()
type(np.float32(0).item()) # <type 'float'>
type(np.float64(0).item()) # <type 'float'>
type(np.uint32(0).item())  # <type 'long'>
# examples using np.asscalar(a)
type(np.asscalar(np.int16(0)))   # <type 'int'>
type(np.asscalar(np.cfloat(0)))  # <type 'complex'>
type(np.asscalar(np.datetime64(0)))  # <type 'datetime.datetime'>
type(np.asscalar(np.timedelta64(0))) # <type 'datetime.timedelta'>
