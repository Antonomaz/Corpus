
import xmltodict
import xml.etree.ElementTree as ET
import glob
import dateutil.parser as duparser
from json_stats import unknown_pub_date, unknown_pub_name, unknown_pub_place
test_dir:str = "../tests/Mazarinades_tests/*/*.xml"
test_file1:str = "../tests/Mazarinades_tests/1701-1800/Moreau1751_GBOOKS.xml"
test_file2:str = "../tests/Mazarinades_tests/1701-1800/Moreau1704_GALL.xml"
test_file3:str = "../tests/Mazarinades_tests/2401-2500/Moreau2497_GBOOKS.xml"
test_file4:str = "../tests/Mazarinades_tests/1401-1500/Moreau1469_GALL.xml"
test_file5:str = "../tests/Mazarinades_tests/2001-2100/Moreau2042_GBOOKS.xml"

def normalise_publisher(publisher_field:dict):
    if isinstance(publisher_field, dict):
     persName_keys:list = ["surname", "forename", "orgName"]
     if "persName" not in publisher_field:
        #print(publisher_field)
        #persName_dict:dict = {}
        #for p_key in persName_keys:
        #        if p_key in publisher_field:
        #            persName_dict[p_key] = publisher_field[p_key]
        #            publisher_field.pop(p_key)
        #        publisher_field["persName"] = persName_dict
        #print(publisher_field)
        #print(publisher_field.keys())
        persName_dict:dict = {}
        for p_key in persName_keys:
            if p_key in publisher_field:
                print(publisher_field)
                persName_dict[p_key] = publisher_field[p_key]
                publisher_field.pop(p_key)
                publisher_field["persName"] = persName_dict
                print(publisher_field)
     elif "persName" in publisher_field:
        if isinstance(publisher_field["persName"], dict) and unknown_pub_name in publisher_field["persName"].values():
            #print("found:", publisher)
            publisher_field["persName"] = unknown_pub_name
    return publisher_field

def normalise_pub_date(pub_date_field:dict|str):
    #if isinstance(pub_date_field, str):
        
    # @when key add-in
    if isinstance(pub_date_field, dict):
        when_key:str = "@when"
        if when_key not in pub_date_field:
            if "@notAfter" in pub_date_field:
                pub_date = duparser.parse(timestr=pub_date_field    ["@notAfter"]).year
                pub_date_field[when_key] = pub_date
                #print(pub_date_field[when_key])
            elif "@notBefore" in pub_date_field:
                pub_date = duparser.parse(timestr=pub_date_field    ["@notBefore"]).year
                pub_date_field[when_key] = pub_date
                #print(pub_date_field[when_key])

            #print("modified pub date")
    return pub_date_field


def normalise_pub_place(pub_place_field:str|dict):
    where_key: str ="#text"
    if isinstance(pub_place_field, str):
        pub_place_field = {where_key: pub_place_field}
    return pub_place_field

def normalise_xml(input_filepath:str, output_filepath:str):
    xml_dict:dict = xmltodict.parse(open(input_filepath).read())
    dict_header:dict =xml_dict["TEI"]["teiHeader"]
    publisher = dict_header["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
    pub_date = dict_header["fileDesc"]["sourceDesc"]["bibl"]["date"]
    pub_place = dict_header["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"]
    #print(pub_date)
    # publisher
    if isinstance(publisher, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = [normalise_publisher(publisher_field=pub) for pub in publisher]
    else:
        if isinstance(publisher, dict):
            xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = normalise_publisher(publisher_field=publisher)
        
    # pub date
    #print(f"before: {pub_place}")
    if isinstance(pub_date, dict):
        #print(f"before: {pub_date}")
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = normalise_pub_date(pub_date_field=pub_date)
        #print(f"after: {pub_date}")
    else:
        # handling lists
        if isinstance(pub_date, list):
            pub_date = [normalise_pub_date(pub_date_field=pub_date_dict) for pub_date_dict in pub_date]
    # pub place
     # handling lists
    if isinstance(pub_place, list):
        pub_place = [normalise_pub_place(pub_place_field=pub_p) for pub_p in pub_place]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"] = normalise_pub_place(pub_place_field=pub_place)
    #print(f"after: {pub_place}")
    new_xml = xmltodict.unparse(input_dict=xml_dict, output=open(output_filepath, mode="w"))
    return new_xml

def normalise_xml_dir(dir_path:str):
    for filepath in glob.glob(pathname=dir_path):
        new_xml = normalise_xml(input_filepath=filepath, output_filepath=filepath)
    
    return

#normalise_xml(input_filepath=test_file1)
#normalise_xml(input_filepath=test_file2)
#normalise_xml(input_filepath=test_file3)
#normalise_xml(input_filepath=test_file4)
#normalise_xml(input_filepath=test_file5)
normalise_xml_dir(dir_path=test_dir)