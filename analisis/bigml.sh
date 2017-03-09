
curl -o iris.csv https://static.bigml.com/csv/iris.csv
export BIGML_USERNAME=LuisHerrera
export BIGML_API_KEY=363851e59f721cf461ec8e42a3ef04aa0a2bb179
export BIGML_AUTH="username=$BIGML_USERNAME;api_key=$BIGML_API_KEY"
curl "https://bigml.io/source?$BIGML_AUTH" -F file=iris.csv

export BIGML_AUTH="username=$BIGML_USERNAME;api_key=$BIGML_API_KEY"

curl "https://bigml.io/source?$BIGML_AUTH" -F file=@iris.csv
curl "https://bigml.io/source?$BIGML_AUTH" -F file=@iris.csv | jq '.'
curl "https://bigml.io/dataset?$BIGML_AUTH" -X POST -H 'content-type: application/json' -d '{"source": "source/58a776917e0a8d39db002561"}' | jq '.'
curl "https://bigml.io/model?$BIGML_AUTH" -X POST -H 'content-type: application/json' -d '{"dataset": "dataset/58a7794a663ac2320e000f8b"}' | jq '.'
curl "https://bigml.io/prediction?$BIGML_AUTH" -X POST -H 'content-type: application/json' -d '"model": "model/58a77a62663ac23204001a4e", "input_data": {"000000": 5, "000001": 3}}' | jq '.'

# clm:

export BIGML_USERNAME=charlielm1015
export BIGML_API_KEY=90bb088a4d01d81953df8aecfb4ac3a5850423ed
export BIGML_AUTH="username=$BIGML_USERNAME;api_key=$BIGML_API_KEY"

from bigml.api import BigML
api = BigML()

source = api.create_source('.iris.')
