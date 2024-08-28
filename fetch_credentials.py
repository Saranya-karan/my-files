import json

credentials_dict = {}

try:
    with open('credentials/credentials.json', 'r') as f:
        credentials_dict = json.load(f)
        # print(credentials_dict)
except:
    raise Exception('Unable to find credentials.json file')