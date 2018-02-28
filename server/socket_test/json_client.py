import json

def json_encode(dict_data):
    json_data = json.dumps(dict_data)
    return json_data
    
def json_decode(json_data):
    dict_data = json.loads(json_data)
    return dict_data
    
