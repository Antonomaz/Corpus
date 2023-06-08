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
test_file8:str = "../tests/Mazarinades_tests/1301-1400/Moreau1372_GALL.xml"
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
        #print(pub_date_field)
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
    #print(pub_date)
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


def name_publisher(publisher:dict):
    #print(f"publisher: {publisher}")
    publisher_flatdict = flatdict.FlatDict(value=publisher)
    #print(publisher_flatdict.values())
    if "Sans Nom" in publisher_flatdict.values():
        for flat_key in publisher_flatdict:
            if publisher_flatdict[flat_key]== "Sans Nom":
                publisher_flatdict[flat_key] = "Sans nom"
        publisher = publisher_flatdict.as_dict()
    #print(publisher)
    return publisher

def name_pub_date(pub_date:dict):
    pub_date_flatdict = flatdict.FlatDict(value=pub_date)
    #print(f"pub_date: {pub_date}")
    if "Sans Date" in pub_date_flatdict.values():
        for flat_key in pub_date:
            if pub_date_flatdict[flat_key] == "Sans Date":
                pub_date_flatdict[flat_key] = "Sans date"
    pub_date = pub_date_flatdict.as_dict()
    #print(pub_date)
    return pub_date

def name_pub_place(pub_place:dict):
    pub_place_flatdict = flatdict.FlatDict(value=pub_place)
    #print(f"pub_place: {pub_place}")
    if "Sans Lieu" in pub_place_flatdict.values():
        for flat_key in pub_place_flatdict:
            if pub_place_flatdict[flat_key] == "Sans Lieu":
                pub_place_flatdict[flat_key] = "Sans lieu"
        pub_place = pub_place_flatdict.as_dict()
    return pub_place

def name_genre(form:dict, value_to_change:str, replacement:str):
    form_flatdict = flatdict.FlatDict(form)
    for flat_key in form_flatdict:
        if form_flatdict[flat_key] == value_to_change:
            form_flatdict[flat_key] = replacement
            form = form_flatdict.as_dict()
            print(f"form: {form}")
    return form

def normalise_names(input_filepath:str, output_filepath:str, value_to_change:str="", replacement:str=""):
    xml_dict:dict = xmltodict.parse(open(input_filepath).read())
    dict_header:dict =xml_dict["TEI"]["teiHeader"]
    publisher:dict|list = dict_header["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
    pub_date:dict|list = dict_header["fileDesc"]["sourceDesc"]["bibl"]["date"]
    pub_place:dict|list = dict_header["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"]
    form:dict|list = dict_header["profileDesc"]["textClass"]["keywords"]["term"]
    #print(form)
    #form
    if value_to_change != "":
        if isinstance(form, list):
            xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"] = [name_genre(form=f, value_to_change=value_to_change, replacement=replacement) for f in form]
        else:            
            xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"] = name_genre(form=form, value_to_change=value_to_change, replacement=replacement)
        #print(xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"])
        #print(xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"], input_filepath)
    #publisher
    if isinstance(publisher, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = [name_publisher(publisher=pub) for pub in publisher]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = name_publisher(publisher=publisher)
    #print(xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"]) 
    #pub date
    #print(pub_date)
    if isinstance(pub_date, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = [name_pub_date(pub_date=date) for date in pub_date]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = name_pub_date(pub_date=pub_date)
    #print(xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"])
        
    #print(pub_date)
    #pub place
    if isinstance(pub_place, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"] = [name_pub_place(pub_place=place) for place in pub_place]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"] = name_pub_place(pub_place=pub_place)
    
    #print(xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"])
    new_xml = xmltodict.unparse(input_dict=xml_dict, output=open(output_filepath, mode="w"), pretty=True, short_empty_elements=True)
    return new_xml

#change genre classification
#<term type="genre">pièce de théâtre</term>
#./1301-1400/Moreau1372_GALL.xml


def normalise_xml_dir(dir_path:str, value_to_change:str = "", replacement:str=""):
    for filepath in glob.glob(pathname=dir_path):
        new_xml = normalise_xml(input_filepath=filepath, output_filepath=filepath)
        new_xml = normalise_names(input_filepath=filepath, output_filepath=filepath, value_to_change=value_to_change, replacement=replacement)
    return

#normalise_xml(input_filepath=test_file1)
#normalise_xml(input_filepath=test_file2)
#normalise_xml(input_filepath=test_file3)
#normalise_xml(input_filepath=test_file4)
#normalise_xml(input_filepath=test_file5, output_filepath="temp.xml")
#normalise_xml(input_filepath=test_file6, output_filepath="temp_xml/temp.xml")
#normalise_xml(input_filepath=test_file7, output_filepath="temp_xml/temp.xml")
#tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
normalise_xml_dir(dir_path=test_dir, value_to_change="pièce de théâtre", replacement="texte de forme théâtrale")
#normalise_names(input_filepath=test_file8, output_filepath="temp_xml/temp.xml", value_to_change="pièce de théâtre", replacement="texte de forme théâtrale")
#tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
#test_stats()