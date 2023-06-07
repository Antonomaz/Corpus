
import xmltodict
import xml.etree.ElementTree as ET
import dateutil.parser as duparser
from json_stats import unknown_pub_date, unknown_pub_name, unknown_pub_place
test_dir:str = "/tests/Mazarinades_tests/*/*.xml"
test_file1:str = "../tests/Mazarinades_tests/1701-1800/Moreau1751_GBOOKS.xml"
test_file2:str = "../tests/Mazarinades_tests/1701-1800/Moreau1704_GALL.xml"
test_file3:str = "../tests/Mazarinades_tests/2401-2500/Moreau2497_GBOOKS.xml"
test_file4:str = "../tests/Mazarinades_tests/1401-1500/Moreau1469_GALL.xml"


def normalise_pub_date(pub_date_field:dict|str):
    if isinstance(pub_date_field, str):
    # @when key add-in
    elif isinstance(pub_date_field, dict):
        when_key:str = "@when"
        if when_key not in pub_date_field:
            if "@notAfter" in pub_date_field:
                pub_date = duparser.parse(timestr=pub_date_field    ["@notAfter"]).year
            elif "@notBefore" in pub_date_field:
                pub_date = duparser.parse(timestr=pub_date_field    ["@notBefore"]).year
            pub_date_field[when_key] = pub_date
    return pub_date_field

def normalise_xml(filepath:str):
    xml_dict:dict = xmltodict.parse(open(filepath).read())
    dict_header:dict =xml_dict["TEI"]["teiHeader"]
    publisher = dict_header["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
    pub_date = dict_header["fileDesc"]["sourceDesc"]["bibl"]["date"]
    #print(pub_date)
    # publisher
    if isinstance(publisher, dict):
        if "persName" in publisher:
            if isinstance(publisher["persName"], dict) and unknown_pub_name in publisher["persName"].values():
                #print("found:", publisher)
                publisher["persName"] = unknown_pub_name
                #print(publisher)
    # pub date
    if isinstance(pub_date, dict):
        print(f"before: {pub_date}")
        pub_date = normalise_pub_date(pub_date_dict=pub_date)
        print(f"after: {pub_date}")
    else:
        # handling lists
        if isinstance(pub_date, list):
        pub_date = [normalise_pub_date(pub_date_dict=pub_date_dict)]

    return

normalise_xml(filepath=test_file1)
normalise_xml(filepath=test_file2)
normalise_xml(filepath=test_file3)
normalise_xml(filepath=test_file4)