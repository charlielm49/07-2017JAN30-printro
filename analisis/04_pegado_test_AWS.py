#!/usr/bin/python
# -*- coding: utf-8 -*

import glob
import os

def main():
  path1 = "/opt/aws-ml/.data/worker/"
  # Id del proceso actual
  # path2 = "8d06f930-4016-4911-8c12-2cc0f92a5b78"
  # Ruta en AWS
  path2 = "5318f322-6e90-4952-b62f-19f5e21c3720"
  path = path1 + path2

  command = "cd " + path
  print(command)
  os.system(command)

  all_files = glob.glob(os.path.join(path, "*.csv"))

  command = "rm " + " ".join(map(str, all_files))
  print(command)
  os.system(command)


if __name__ == '__main__':
    main()
