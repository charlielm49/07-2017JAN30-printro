# -*- coding: utf-8 -*-

# automatic import with pylab
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 1200)
#import manually
import pandas as pd
import seaborn as sns
import pprint

import boto3    

client = boto3.client('machinelearning')

response = client.create_data_source_from_s3(
    DataSourceId='string',
    DataSourceName='string',
    DataSpec={
        'DataLocationS3': 'string',
        'DataRearrangement': 'string',
        'DataSchema': 'string',
        'DataSchemaLocationS3': 'string'
    },
    ComputeStatistics=True|False
)

response = client.create_data_source_from_s3(
    DataSourceId='ds-bankingdata2',    
    DataSourceName='Banking Data 2',    
    DataSpec={'DataLocationS3': 's3://machinelearningutel/banking-batch.csv',        'DataSchema': '{"version" : "1.0",            "rowId" : null,            "rowWeight" : null,            "targetAttributeName" : null,             "dataFormat" : "CSV",             "dataFileContainsHeader" : true,             "attributes" :[ {    "attributeName" : "age",    "attributeType" : "NUMERIC"      }, {    "attributeName" : "job",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "marital",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "education",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "default",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "housing",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "loan",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "contact",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "month",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "day_of_week",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "duration",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "campaign",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "pdays",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "previous",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "poutcome",    "attributeType" : "CATEGORICAL"  }, {    "attributeName" : "emp_var_rate",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "cons_price_idx",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "cons_conf_idx",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "euribor3m",    "attributeType" : "NUMERIC"  }, {    "attributeName" : "nr_employed",    "attributeType" : "NUMERIC"  } ],  "excludedAttributeNames" : [ ]}'    }, 
    ComputeStatistics=True)
