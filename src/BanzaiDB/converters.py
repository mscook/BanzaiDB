import tablib
import json

def convert_from_JSON_to_CSV(json_data, header=False, fmt='csv'): 
    """
    """
    json_str = json.dumps(json_data)
    supported = ['csv']
    if fmt in supported:
        data = tablib.Dataset()
        data.json = '['+json_str+']'
        if header:
            tmp = data.csv.split('\n')
            return tmp[0]+"\n"+tmp[1]
        else:
            return data.csv.split('\n')[1]
    else:
        raise Exception("Only output in CSV is supported")

def convert_from_csv_to_JSON(csv_data, header):
    """
    """
    data = tablib.Dataset()
