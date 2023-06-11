import json
import glob
csv_dir:str="../output/database"
maz_json_dir:str = "../Mazarinades_jsons/Bibliotheque_Mazarine/*.json"
test_file:str ="../Mazarinades_jsons/Bibliotheque_Mazarine/BM48896_MAZ.json"
csv_file:str = csv_dir+ "/maz.csv"
from pathlib import Path
import csv
import re
fieldnames:list = ["ID", "titre", "date_imprimée", "Date plus précise", "lieu", "nb pages", "Notice"]
from json_stats_normalised import unknown_pub_date, unknown_pub_place

def prepare_row(filepath:str, fieldnames=fieldnames):
    data_dict:dict = json.load(fp=open(file=filepath))
    nbPages:int = data_dict["entête"]["nbPages"]
    title:str = re.sub(pattern=r"\s+",repl=" ", string=data_dict["entête"]["titre"])
    maz_id = (re.match(pattern=r"^.*(?=_)", string=(Path(filepath).parts)[-1])).group() #type: ignore
    #pub place
    pub_place = data_dict["entête"]["pubPlace"]
    if isinstance(pub_place, list):
        for p_p in data_dict["entête"]["pubPlace"]:
            if p_p["#text"] != unknown_pub_place:
                pub_place = p_p["#text"]
                break
        else:
            pub_place = unknown_pub_place
    else:
        pub_place = pub_place["#text"]
    print(pub_place)
    # pub date
    pub_date = data_dict["entête"]["pubDate"]
    #print(pub_date)
    if isinstance( data_dict["entête"]["pubDate"], list):
        for p_d in pub_date:
            if p_d["@when"] != unknown_pub_date:
                pub_date = p_d["@when"]
                break
        else:
            pub_date = unknown_pub_date
    else:
        pub_date = unknown_pub_date if unknown_pub_date in pub_date.values() else data_dict["entête"]["pubDate"]["@when"]
    print(pub_date)
    return {fieldnames[0]: maz_id, fieldnames[1]: title, fieldnames[2]: pub_date, fieldnames[3]:None, fieldnames[4]: pub_place, fieldnames[5]:nbPages, fieldnames[6]:None}

def make_csv_from_json(filepath:str, csv_file, mode:str="a", fieldnames:list = fieldnames):
    data_row:dict = prepare_row(filepath=filepath, fieldnames=fieldnames)
    print(data_row)
    # writing to csv
    if isinstance(csv_file, str):
       csv_file = open(csv_file, mode=mode)
    res = csv.DictWriter(f=csv_file, fieldnames=fieldnames)
    res.writerow(data_row)
    return data_row

def make_csv_from_json_dir(dir_path: str, csv_file, mode:str = "w", fieldnames:list=fieldnames):
    if isinstance(csv_file, str):
       csv_file = open(csv_file, mode=mode)
    res = csv.DictWriter(f=csv_file, fieldnames=fieldnames)
    res.writeheader()
    for filepath in glob.glob(dir_path):
        make_csv_from_json(filepath=filepath, fieldnames=fieldnames, csv_file=csv_file, mode="a")
    return

#make_csv_from_json(filepath=test_file, csv_file=csv_file)
make_csv_from_json_dir(dir_path=maz_json_dir, csv_file=csv_file, mode="w", fieldnames=fieldnames)
#prepare_row(filepath=test_file)