import json

data_double_quote = '{"name":"revotu","age":"24"}'
data_single_quote = "{'name':'revotu','age':'24'}"

print json.loads(data_double_quote)

print json.loads(data_single_quote)