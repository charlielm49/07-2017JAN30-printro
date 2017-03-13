# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import glob
import os

# prueba: path = "."
# Ruta a dir .data
path1 = "/opt/aws-ml/.data/worker/"
# Id del proceso actual
path2 = "8d06f930-4016-4911-8c12-2cc0f92a5b78"
path = path1 + path2

command = "cd " + path
os.system(command)
# Leemos archivos y ponemos en lista
all_files = glob.glob(os.path.join(path, "*.csv"))
# Convertimos a dataframe
df_files = (pd.read_csv(file) for file in all_files)
# Concatenamos archivos con Pandas
concat_file = pd.concat(df_files, ignore_index = True)
# Exportamos a archivo
concat_file.to_csv("full_f.csv", index = False)
# Borramos archivos chiquitos
command = "rm " + " ".join(map(str, all_files))
os.system(command)
