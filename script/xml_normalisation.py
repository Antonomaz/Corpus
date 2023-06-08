import xmltodict
import xml.etree.ElementTree as ET
import glob
import flatdict
import dateutil.parser as duparser
from tei_to_json import tei_to_json_file
from json_stats_normalised import unknown_pub_date, unknown_pub_name, unknown_pub_place, test_stats
test_dir:str = "../tests/Mazarinades_tests/*/*.xml"
test_file1:str = "../tests/Mazarinades_tests/1701-1800/Moreau1751_GBOOKS.xml"
test_file2:str = "../tests/Mazarinades_tests/1701-1800/Moreau1704_GALL.xml"
test_file3:str = "../tests/Mazarinades_tests/2401-2500/Moreau2497_GBOOKS.xml"
test_file4:str = "../tests/Mazarinades_tests/1401-1500/Moreau1469_GALL.xml"
test_file5:str = "../tests/Mazarinades_tests/2001-2100/Moreau2022_GBOOKS.xml"
test_file6:str = "../tests/Mazarinades_tests/2001-2100/Moreau2082_GBOOKS.xml"
test_file7:str = "../tests/Mazarinades_tests/2001-2100/Moreau2012_GBOOKS.xml"

def normalise_publisher(publisher_field:dict):
    if isinstance(publisher_field, dict):
     persName_keys:list = ["surname", "forename", "orgName"]
     if "persName" not in publisher_field:
        persName_dict:dict = {}
        for p_key in persName_keys:
            if p_key in publisher_field:
                #print(publisher_field)
                persName_dict[p_key] = publisher_field[p_key]
                publisher_field.pop(p_key)
                publisher_field["persName"] = persName_dict
                #print(publisher_field)
     elif "persName" in publisher_field:
        if isinstance(publisher_field["persName"], dict) and unknown_pub_name in publisher_field["persName"].values():
            publisher_field["persName"] = unknown_pub_name
        
    return publisher_field

def normalise_pub_date(pub_date_field:dict|str):
    date_key_str: str ="#text"
    when_key:str = "@when"
    if isinstance(pub_date_field, str):
        if pub_date_field == unknown_pub_date:
            pub_date_field = {date_key_str: pub_date_field, "@source": None}
        else:
            pub_date_field = {when_key: duparser.parse(timestr=pub_date_field).year}
        print(pub_date_field)
    # @when key add-in
    if isinstance(pub_date_field, dict):
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
    was_str:bool = False
    if isinstance(pub_place_field, str):
        was_str= True
        #print(pub_place_field)
        pub_place_field = {where_key: pub_place_field, "@source": None} #had to add in the @source to be able to use "#text" as a key
        #print(pub_place_field)
    return pub_place_field, was_str

def normalise_xml(input_filepath:str, output_filepath:str):
    #print(input_filepath)
    xml_dict:dict = xmltodict.parse(open(input_filepath).read())
    dict_header:dict =xml_dict["TEI"]["teiHeader"]
    publisher = dict_header["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
    pub_date = dict_header["fileDesc"]["sourceDesc"]["bibl"]["date"]
    pub_place = dict_header["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"]
    #print(pub_place)
    print(pub_date)
    # publisher
    if isinstance(publisher, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = [normalise_publisher(publisher_field=pub) for pub in publisher]
    else:
        if isinstance(publisher, dict):
            xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = normalise_publisher(publisher_field=publisher)
        
    # pub date
    #print(f"before: {pub_place}")
    # handling lists
    if isinstance(pub_date, list):
        pub_date = [normalise_pub_date(pub_date_field=pub_date_dict) for pub_date_dict in pub_date]
    else:
        #print(f"before: {pub_date}")
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = normalise_pub_date(pub_date_field=pub_date)
        #print(f"after: {pub_date}")
    # pub place
     # handling lists
    if isinstance(pub_place, list):
        pub_place = [normalise_pub_place(pub_place_field=pub_p)[0] for pub_p in pub_place]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"], was_str = normalise_pub_place(pub_place_field=pub_place)
        #print("was str:", xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"])
        #if was_str:
        #    print("was str:", xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"])
    #print(f"after: {pub_place}")
    new_xml = xmltodict.unparse(input_dict=xml_dict, output=open(output_filepath, mode="w"), pretty=True, short_empty_elements=True)
    #new_xml = xmltodict.unparse(input_dict=xml_dict)
    #new_new_xml = xmltodict.parse(new_xml, xml_attribs=True)
    #print(new_new_xml["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"])
    return new_xml

def normalise_names(input_filepath:str, output_filepath:str):
    xml_dict:dict = xmltodict.parse(open(input_filepath).read())
    dict_header:dict =xml_dict["TEI"]["teiHeader"]
    publisher:dict = dict_header["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
    pub_date:dict = dict_header["fileDesc"]["sourceDesc"]["bibl"]["date"]
    pub_place:dict = dict_header["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"]
    #publisher
    print(f"publisher: {publisher}")
    publisher_flatdict = flatdict.FlatDict(value=publisher)
    #print(publisher_flatdict.values())
    if "Sans Nom" in publisher_flatdict.values():
        for flat_key in publisher:
            if publisher_flatdict[flat_key]== "Sans Nom":
                publisher_flatdict[flat_key] = "Sans nom"
    xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = publisher_flatdict.as_dict()
    print(publisher)
    #pub date
    #print(pub_date)
    pub_date_flatdict = flatdict.FlatDict(value=pub_date)
    if "Sans Date" in pub_date_flatdict.values():
        print(f"pub_date: {pub_date}")
        for flat_key in pub_date:
            if pub_date_flatdict[flat_key] == "Sans Date":
                pub_date_flatdict[flat_key] = "Sans date"
    xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = pub_date_flatdict.as_dict()
    print(pub_date)
    #print(pub_date)
    #pub place
    pub_place_flatdict = flatdict.FlatDict(value=pub_place)
    print(f"pub_place: {pub_place}")
    if "Sans Lieu" in pub_place_flatdict.values():
        for flat_key in pub_place_flatdict:
            if pub_place_flatdict[flat_key] == "Sans Lieu":
                pub_place_flatdict[flat_key] = "Sans lieu"
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"] = pub_place_flatdict.as_dict()
    print(pub_place)
    new_xml = xmltodict.unparse(input_dict=xml_dict, output=open(output_filepath, mode="w"), pretty=True, short_empty_elements=True)
    return new_xml

def normalise_xml_dir(dir_path:str):
    for filepath in glob.glob(pathname=dir_path):
        new_xml = normalise_xml(input_filepath=filepath, output_filepath=filepath)
    return

#normalise_xml(input_filepath=test_file1)
#normalise_xml(input_filepath=test_file2)
#normalise_xml(input_filepath=test_file3)
#normalise_xml(input_filepath=test_file4)
#normalise_xml(input_filepath=test_file5, output_filepath="temp.xml")
#normalise_xml(input_filepath=test_file6, output_filepath="temp_xml/temp.xml")
#normalise_xml(input_filepath=test_file7, output_filepath="temp_xml/temp.xml")
#tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
#normalise_xml_dir(dir_path=test_dir)
normalise_names(input_filepath=test_file6, output_filepath="temp_xml/temp.xml")
tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
#test_stats()