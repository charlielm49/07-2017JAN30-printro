07-2016JAN30-printro
--------------------

python scripts:


01_obtainData.py: 
--------------
- python connect to MOODLE database (with pymysql)
- query to database



02_churn_detalle_v02.py (creo que esto es copia de proyecto 04)
-----------------------

- obtiene fecha mínima: 
    1) a = df(['var1', 'var2', 'var a contar']).groupby(['var1', 'var2']).min()
    2) a = a.unstack()
    3) a.columns = a.columns.droplevel(0)


03_columnas.py
--------------
- read from csv file
- cleans event field
- creates new field crsid + event
- obtains total events per user
event2 = event[['usrid', 'crsevntname', 'component']].\
groupby(['usrid', 'crsevntname']).count()
- converts pandas dataframe multiindex to columns
event2.reset_index(inplace = True)
'''
all are columns:
   usrid              crsevntname  component
0   2928          0-core-msg_view          2
1   3021  0-core-usr_profile_view          4
'''
- converts rows to columns
tmp = event2.pivot_table('component', 'usrid', 'crsevntname')

---

SQL queries

01-detailed_activities.txt - queries para obtener detalle histórico de todas las actividades de todos los alumnos


--- 
PROCESO GLOBAL:
1) query (SQL): obtiene usrs registrados en introductorios (crse-enrol)



2) query (SQL): obtiene eventos de los usuarios obtenidos en 1) (logevent)

3) script (PANDAS): convierte columna de eventos en tabla de eventos por usuario en un solo renglón (vector de atributos)
AFINAR: que no regrese eventos de introductorias
AFINAR (ya): que no incluya reingresos


4) query (SQL): obtiene informacion de usrs de tabla estudiantes (usr)



5) script (PANDAS): pega la informacion de usrs a sus eventos


6) (?): sube la tabla a contenedor


7) script (BIGML): corre analisis , obtiene modelo, programa automatizacion del proceso (semanal)


quién va a coordinar todo el proceso?

---

lluvia de ideas de info a utilizar para analisis

tiempos
 registro, 
 accesos,  
 actividades academicas
frecuencias
 a partir de tiempos:
  tareas entregadas
  examenes
  foros
  eventos
cantidades
 a partir de eventos:
  num logins
  num ...
demograficos
 a
 b
eventos
 presente/ausente (1/0)


---

pend: sacar mas variables de la tabla de usuarios: como hacerle? hacer otro query a la misma tabla? o modificar el query actual?

 

______________________________________________
