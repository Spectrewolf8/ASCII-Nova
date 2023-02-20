import json
with open('Test.json', 'w') as data_file:
    data_file.dump

with open('Test.json', 'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)

print(data)
