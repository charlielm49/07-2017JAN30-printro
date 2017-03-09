
# -*- coding: utf-8 -*-


BIGML_USERNAME="charlielm1015"
BIGML_API_KEY="90bb088a4d01d81953df8aecfb4ac3a5850423ed"

import pprint
from bigml.api import BigML
api = BigML(BIGML_USERNAME, BIGML_API_KEY)

source = api.create_source('.iris.')
api.ok(source) # to ensure that objects are finished before using them
dataset = api.create_dataset(source)
api.ok(dataset)
model = api.create_model(dataset)
api.ok(model)
prediction = api.create_prediction(model, \
{'sepal length': 5, 'sepal width': 2.5})


#to evaluate the model
evaluation = api.create_evaluation(model, dataset)
api.ok(evaluation)


#to get fields
source_get = api.get_source(source)
api.pprint(api.get_fields(source_get))

dataset_get = api.get_dataset(dataset)
api.pprint(api.get_fields(dataset_get))

evaluation_get = api.get_evaluation(evaluation)
api.pprint(evaluation_get['object']['result'])


# specific models
log = api.create_logistic_regression(dataset)
api.pprint(log['object'])
api.pprint(log['object']['logistic_regression'])
