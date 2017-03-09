import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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



# regresa alumnos inscritos en materias intro bloque A
cursor.execute(" SELECT \
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
group by mdl_groups_members.userid ")

rows = cursor.fetchall() 

data = []
for line in rows:
    #print(line)
    data.append(line)


data2 = [id['usrid'] for id in data]
len(data2)


Connection.close()


'''
# query ok
# regresa cantidad de alumnos inscritos en materias curriculares + intro
cursor.execute(" select count(*) as total_alumnos_dia_dia \
from ( \
SELECT mdl_groups_members.userid as userd, \
from_unixtime(mdl_user_enrolments.timecreated), \
mdl_course.fullname,mdl_course.id,mdl_groups.name \
FROM mdl_groups_members \
INNER JOIN mdl_user ON mdl_user.id = mdl_groups_members.userid AND mdl_user.username not like '%demo%' \
INNER JOIN mdl_groups ON mdl_groups.id = mdl_groups_members.groupid \
INNER JOIN mdl_course ON mdl_course.id = mdl_groups.courseid \
INNER JOIN mdl_enrol ON mdl_enrol.courseid = mdl_groups.courseid \
INNER JOIN mdl_user_enrolments ON mdl_user_enrolments.enrolid = mdl_enrol.id AND mdl_user_enrolments.userid = mdl_groups_members.userid AND mdl_user.id = mdl_user_enrolments.userid \
INNER JOIN mdl_context ON mdl_context.contextlevel = 50 AND mdl_context.instanceid = mdl_groups.courseid \
INNER JOIN mdl_role_assignments ON mdl_role_assignments.contextid = mdl_context.id AND mdl_role_assignments.userid = mdl_groups_members.userid \
INNER JOIN mdl_role ON mdl_role.id = mdl_role_assignments.roleid AND mdl_role.id in(5,16) \
WHERE mdl_user_enrolments.status = 0 \
and mdl_enrol.courseid in (8906,8907,9025,9026,9027,9028,9029,9030,9031,9032,9033,9034,9035,9036,9037,9038,9039,9040,9041,9042,9043,9044,9045,9046,9047,9048,9049,9050,9051,9052,9053,9054,9055,9056,9057,9058,9059,9060,9061,9062,9063,9064,9065,9066,9067,9068,9069,9070,9071,9072,9073,9074,9075,9076,9077,9078,9079,9080,9081,9082,9083,9084,9085,9086,9087,9088,9089,9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,9100,9101,9102,9103,9104,9105,9106,9107,9108,9109,9110,9111,9112,9113,9114,9115,9116,9117,9118,9119,9120,9121,9122,9123,9124,9125,9126,9127,9128,9129,9130,9131,9132,9133,9134,9135,9136,9137,9138,9139,9140,9141,9142,9143,9144,9145,9146,9147,9148,9149,9150,9151,9152,9153,9154,9155,9156,9157,9158,9159,9160,9161,9162,9163,9164,9165,9166,9167,9168,9169,9170,9171,9172,9173,9174,9175,9176,9177,9178,9179,9180,9181,9182,9183,9184,9185,9186,9187,9188,9189,9190,9191,9192,9193,9194,9195,9196,9197,9198,9199,9200,9201,9202,9203,9204,9205,9206,9207,9208,9209,9210,9211,9212,9213,9214,9215,9216,9217,9218,9219,9220,9221,9222,9223,9224,9229,9230,9231,9232,9233,9234,9235,9236,9237,9238,9239,9240,9241,9242,9243,9244,9245,9246,9247,9248,9249,9250,9251,9252,9253,9254,9255,9256,9257,9258,9259,9260,9261,9262,9263,9264,9265,9266,9267,9268,9269,9270,9271,9272,9273,9274,9275,9276,9277,9278,9279,9280,9281,9282,9283,9284,9285,9286,9287,9288,9289,9290,9291,9292,9293,9294,9295,9296,9297,9298,9299,9300,9301,9302,9303,9304,9305,9306,9307,9308,9309,9310,9311,9312,9313,9314,9315,9316,9317,9318,9319,9320,9321,9322,9323,9324,9325,9326,9327,9328,9329,9330,9331,9332,9333,9334,9335,9336,9337,9338,9339,9340,9341,9342,9343,9344,9345,9346,9347,9348,9349,9350,9351,9352,9353,9354,9355,9356,9357,9358,9359,9360,9361,9362,9363,9364,9365,9366,9367,9368,9369,9370,9371,9372,9373,9374,9375,9376,9377,9378,9379,9380,9381,9382,9383,9384,9385,9386,9387,9388,9389,9390,9391,9392,9393,9394,9395,9396,9397,9398,9399,9400,9401,9402,9403,9404,9405,9406,9407,9408,9409,9410,9411,9412,9413,9414,9415,9416,9417,9418,9419,9420,9421,9422,9423,9424,9425,9426,9427,9428,9429,9430,9431,9432,9433,9434,9435,9436,9437,9438,9439,9440,9441,9442,9443,9444,9445,9446,9447,9448,9449,9450,9451,9452,9453,9454,9455,9456,9457,9458,9459,9460,9461,9462,9463,9464,8911,8912,8914,8915,8916,8918,8919,8920,8922,8923,8924,8925) \
and mdl_course.visible = 1 \
group by \
mdl_groups_members.userid ) as xx ")

# query ok
#materias introductorias del 2017-JAN-09 (bloque A)
cursor.execute("SELECT \
mdl_course.fullname, \
mdl_course.id, \
mdl_course.shortname, \
FROM_UNIXTIME(mdl_course.startdate) \
FROM mdl_course \
WHERE mdl_course.shortname like '%L1HB40%' \
and mdl_course.fullname not like '%copia%' \
and FROM_UNIXTIME(mdl_course.startdate) = '2017-01-09%' \
AND mdl_course.visible = 1")



