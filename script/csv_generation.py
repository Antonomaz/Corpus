import json
import glob
csv_dir:str="../output/database"
csv_file:str = "maz.csv"

def make_csv_from_json(filepath:str):
    json_dict:dict = json.load(fp=open(file=filepath))
    return