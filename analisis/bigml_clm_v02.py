
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime
import pymysql.cursors
import glob
import os

BIGML_USERNAME="charlielm1015"
BIGML_API_KEY="90bb088a4d01d81953df8aecfb4ac3a5850423ed"

import pprint
from bigml.api import BigML
api = BigML(BIGML_USERNAME, BIGML_API_KEY)

# prueba: path = "."
# Ruta a dir .data
path1 = "/opt/aws-ml/.data/worker/"
# Id del proceso actual
# path2 = "8d06f930-4016-4911-8c12-2cc0f92a5b78"
# Ruta en AWS
path2 = "5318f322-6e90-4952-b62f-19f5e21c3720"
path = path1 + path2

command = "cd " + path
os.system(command)

source = api.create_source('full_f.csv')
api.ok(source) # to ensure that objects are finished before using them
dataset = api.create_dataset(source)
api.ok(dataset)
model = api.create_model(dataset)
api.ok(model)
prediction = api.create_prediction(model, \
{'8919-forum-discussion_view': 5, '8919-forum-post_created': 2.5})


