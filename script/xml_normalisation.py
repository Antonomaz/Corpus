import xmltodict
import xml.etree.ElementTree as ET
import glob
import flatdict
import re
from pathlib import Path
import os
import dateutil.parser as duparser
from tqdm.auto import tqdm
from tei_to_json import tei_to_json_file
# unknown_pub_date, unknown_pub_name, unknown_pub_place
from json_stats_normalised import test_stats
# test_dir:str = "../tests/Mazarinades_tests/*/*.xml"
# test_dir:str = "../Mazarinades/*/*.xml"

back_up_dir: str = "../Mazarinades_bak/*/*.xml"
all_dir: str = "../Mazarinades/**/**.xml"
# maz_dir: str = "../Mazarinades/Bibliotheque_Mazarine/*.xml"
# maz_dir:str = "../tests/Mazarinades_tests/Bibliotheque_Mazarine/*.xml"

test_file1: str = "../tests/Mazarinades_tests/1701-1800/Moreau1751_GBOOKS.xml"
test_file2: str = "../tests/Mazarinades_tests/1701-1800/Moreau1704_GALL.xml"
test_file3: str = "../tests/Mazarinades_tests/2401-2500/Moreau2497_GBOOKS.xml"
test_file4: str = "../tests/Mazarinades_tests/1401-1500/Moreau1469_GALL.xml"
test_file5: str = "../tests/Mazarinades_tests/2001-2100/Moreau2022_GBOOKS.xml"
test_file6: str = "../tests/Mazarinades_tests/2001-2100/Moreau2082_GBOOKS.xml"
test_file7: str = "../tests/Mazarinades_tests/2001-2100/Moreau2012_GBOOKS.xml"
test_file8: str = "../tests/Mazarinades_tests/1301-1400/Moreau1372_GALL.xml"
test_file9: str = "../Mazarinades/3001-3100/Moreau3003_GBOOKS.xml"
test_file10: str = "../TODO/Moreau23_GBOOKS.xml"
test_file11: str = "../Mazarinades/1-100/Moreau56_GALL.xml"
unknown_pub_place: str = "Sans Lieu"
unknown_pub_name: str = "Sans Nom"
unknown_pub_date: str = "Sans Date"
# constants
XMLNS: str = "http://www.tei-c.org/ns/1.0"
ODD_LINK: str = "https://raw.githubusercontent.com/Antonomaz/ODD/main/Schema/ODD_Antonomaz.rng"
XML_HEADER: str = f"<?xml version='1.0' encoding='utf-8'?>\n<?xml-model href='{ODD_LINK}' type='application/xml' schematypens='http://relaxng.org/ns/structure/1.0'?>\n<?xml-model href='{ODD_LINK}' type='application/xml' schematypens='http://purl.oclc.org/dsdl/schematron'?>\n"


def normalise_publisher(publisher_field: dict):
    if isinstance(publisher_field, dict):
        persName_keys: list = ["surname", "forename", "orgName"]
        if "persName" not in publisher_field:
            persName_dict: dict = {}
            for p_key in persName_keys:
                if p_key in publisher_field:
                    # print(publisher_field)
                    persName_dict[p_key] = publisher_field[p_key]
                    publisher_field.pop(p_key)
                    publisher_field["persName"] = persName_dict
                    # print(publisher_field)
        elif "persName" in publisher_field:
            if isinstance(publisher_field["persName"], dict) and unknown_pub_name in publisher_field["persName"].values():
                publisher_field["persName"] = unknown_pub_name

    return publisher_field


def normalise_pub_date(pub_date_field: dict | str):
    date_key_str: str = "#text"
    when_key: str = "@when"
    if isinstance(pub_date_field, str):
        if pub_date_field == unknown_pub_date:
            pub_date_field = {date_key_str: pub_date_field, "@source": None}
        else:
            pub_date_field = {when_key: duparser.parse(
                timestr=pub_date_field).year}
        # print(pub_date_field)
    # @when key add-in
    if isinstance(pub_date_field, dict):
        if when_key not in pub_date_field:
            if "@notAfter" in pub_date_field:
                pub_date = duparser.parse(
                    timestr=pub_date_field["@notAfter"]).year
                pub_date_field[when_key] = pub_date
                # print(pub_date_field[when_key])
            elif "@notBefore" in pub_date_field:
                pub_date = duparser.parse(
                    timestr=pub_date_field["@notBefore"]).year
                pub_date_field[when_key] = pub_date
                # print(pub_date_field[when_key])
            elif unknown_pub_date in pub_date_field.values():
                pub_date_field[when_key] = unknown_pub_date
            # print("modified pub date")
    return pub_date_field


def normalise_pub_place(pub_place_field: str | dict):
    where_key: str = "#text"
    was_str: bool = False
    if isinstance(pub_place_field, str):
        was_str = True
        # print(pub_place_field)
        # had to add in the @source to be able to use "#text" as a key
        pub_place_field = {where_key: pub_place_field, "@source": None}
        # print(pub_place_field)
    else:
        if isinstance(pub_place_field, dict):
            if unknown_pub_place in pub_place_field.values() and "@source" not in pub_place_field:
                pub_place_field["@source"] = None
                # print(pub_place_field)
    return pub_place_field, was_str


def name_publisher(publisher: dict):
    # print(f"publisher: {publisher}")
    publisher_flatdict = flatdict.FlatDict(value=publisher)
    # print(publisher_flatdict.values())
    if "Sans Nom" in publisher_flatdict.values():
        for flat_key in publisher_flatdict:
            if publisher_flatdict[flat_key] == "Sans Nom":
                publisher_flatdict[flat_key] = "Sans nom"
        publisher = publisher_flatdict.as_dict()
        # print(publisher)
    return publisher


def name_pub_date(pub_date: dict):
    # print(pub_date)
    pub_date_flatdict = flatdict.FlatDict(value=pub_date)
    # print(f"pub_date: {pub_date}")
    if "Sans Date" in pub_date_flatdict.values():
        for flat_key in pub_date:
            if pub_date_flatdict[flat_key] == "Sans Date":
                pub_date_flatdict[flat_key] = "Sans date"
    pub_date = pub_date_flatdict.as_dict()
    # print(pub_date)
    return pub_date


def name_pub_place(pub_place: dict):
    # print(f"pub_place: {pub_place}")
    pub_place_flatdict = flatdict.FlatDict(value=pub_place)
    if "Sans Lieu" in pub_place_flatdict.values():
        for flat_key in pub_place_flatdict:
            if pub_place_flatdict[flat_key] == "Sans Lieu":
                pub_place_flatdict[flat_key] = "Sans lieu"
        pub_place = pub_place_flatdict.as_dict()
    return pub_place


def name_genre(form: dict, value_to_change: str, replacement: str):
    form_flatdict = flatdict.FlatDict(form)
    for flat_key in form_flatdict:
        if form_flatdict[flat_key] == value_to_change:
            form_flatdict[flat_key] = replacement
            form = form_flatdict.as_dict()
            # print(f"form: {form}")
    return form


def rewrite_xml(input_filepath: str, output_filepath: str, xml_string: str, xml_declaration=""):
    input_file = open(file=input_filepath, mode="r", encoding="utf-8")
    output_file = open(file=output_filepath, mode="w")
    if xml_declaration == "":
        xml_declaration = XML_HEADER
    # print(f"XML DEC:{xml_declaration}")
    # print(f"body: {xml_string}")
    new_xml_str: str = xml_declaration+xml_string
    output_file.write(new_xml_str)
    output_file.close()
    input_file.close()
    return new_xml_str


def normalise_names(input_filepath: str, output_filepath: str, value_to_change: str = "", replacement: str = "", xml_declaration: str = ""):
    # parse og xml
    og_tree = ET.parse(source=input_filepath)
    og_root = og_tree.getroot()
    og_body = og_root[1][0]
    xml_dict: dict = xmltodict.parse((f := open(input_filepath)).read())
    f.close()
    dict_header: dict = xml_dict["TEI"]["teiHeader"]
    publisher: dict | list = dict_header["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
    pub_date: dict | list = dict_header["fileDesc"]["sourceDesc"]["bibl"]["date"]
    pub_place: dict | list = dict_header["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"]
    form: dict | list = dict_header["profileDesc"]["textClass"]["keywords"]["term"]
    input_file = open(file=input_filepath, mode="r", encoding="utf-8")
    # print(form)
    # form
    if value_to_change != "":
        if isinstance(form, list):
            xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"] = [
                name_genre(form=f, value_to_change=value_to_change, replacement=replacement) for f in form]
        else:
            xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"] = name_genre(
                form=form, value_to_change=value_to_change, replacement=replacement)
        # print(xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"])
        # print(xml_dict["TEI"]["teiHeader"]["profileDesc"]["textClass"]["keywords"]["term"], input_filepath)
    # publisher
    if isinstance(publisher, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = [
            name_publisher(publisher=pub) for pub in publisher]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = name_publisher(
            publisher=publisher)
    # print(xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"])
    # pub date
    # print(pub_date)
    if isinstance(pub_date, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = [
            name_pub_date(pub_date=date) for date in pub_date]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = name_pub_date(
            pub_date=pub_date)
    # print(xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"])

    # print(pub_date)
    # pub place
    if isinstance(pub_place, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"] = [
            name_pub_place(pub_place=place) for place in pub_place]
    else:
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"] = name_pub_place(
            pub_place=pub_place)

    # print(xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"])
    new_xml = xmltodict.unparse(input_dict=xml_dict, output=open(
        output_filepath, mode="w"), pretty=True, short_empty_elements=True)
    new_tree = ET.parse(output_filepath)
    # new_root = new_tree.getroot()
    new_tree.getroot()[1][0] = og_body
    # for descendant in new_tree.getroot()[1][0][0]:
    #    print(descendant.tag, descendant.attrib)
    # write to output file
    ET.indent(tree=new_tree)
    new_xml_string: str = ET.tostring(
        element=new_tree.getroot(), encoding="utf-8", method="xml").decode()
    rewrite_xml(input_filepath=input_filepath, output_filepath=output_filepath,
                xml_string=new_xml_string, xml_declaration=xml_declaration)
    input_file.close()
    return new_xml

# change genre classification
# <term type="genre">pièce de théâtre</term>
# ./1301-1400/Moreau1372_GALL.xml


def normalise_xml(input_filepath: str, output_filepath: str, change_name: bool = False, value_to_change: str = "", replacement: str = "", xml_declaration: str | None = XML_HEADER):
    input_file = open(file=input_filepath, mode="r", encoding="utf-8")
    if xml_declaration is None:
        # retrieve xml_declaration
        xml_declaration = ""
        for line in input_file:
            if re.match(pattern=r"^(<TEI).*", string=line):
                break
            xml_declaration += line
    # register XMLNS
    ET.register_namespace(prefix="", uri=XMLNS)
    # parse the original xml
    og_tree = ET.parse(source=input_filepath)
    og_root = og_tree.getroot()
    og_body = og_root[1][0]
    xml_dict: dict = xmltodict.parse(xml_input=(
        f := open(file=input_filepath, mode="rb")), force_cdata=True)
    f.close()
    dict_header: dict = xml_dict["TEI"]["teiHeader"]

    publisher = dict_header["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
    pub_date = dict_header["fileDesc"]["sourceDesc"]["bibl"]["date"]
    pub_place = dict_header["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"]

    # print(pub_place)
    # print(pub_date)

    # publisher
    if isinstance(publisher, list):
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = [
            normalise_publisher(publisher_field=pub) for pub in publisher]
    else:
        if isinstance(publisher, dict):
            xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["publisher"] = normalise_publisher(
                publisher_field=publisher)

    # pub date
    # print(f"before: {pub_place}")
    # handling lists
    if isinstance(pub_date, list):
        pub_date = [normalise_pub_date(pub_date_field=pub_date_dict)
                    for pub_date_dict in pub_date]
    else:
        # print(f"before: {pub_date}")
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["date"] = normalise_pub_date(
            pub_date_field=pub_date)
        # print(f"after: {pub_date}")

    # pub place
        # handling lists
    if isinstance(pub_place, list):
        pub_place = [normalise_pub_place(pub_place_field=pub_p)[
            0] for pub_p in pub_place]
    else:
        # print("before:", xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"])
        xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"], was_str = normalise_pub_place(
            pub_place_field=pub_place)
        # print("after:", xml_dict["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"])
        if was_str:
            print("was str:", xml_dict["TEI"]["teiHeader"]
                  ["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"])
    # print(f"after: {pub_place}")
    xmltodict.unparse(input_dict=xml_dict, pretty=True, output=(
        ff := open(file=output_filepath, mode="w")), short_empty_elements=True)
    ff.close()
    new_tree = ET.parse(output_filepath)
    # new_root = new_tree.getroot()
    new_tree.getroot()[1][0] = og_body
    # for descendant in new_tree.getroot()[1][0][0]:
    #    print(descendant.tag, descendant.attrib)
    # write to output file
    output_file = open(file=output_filepath, mode="w")
    ET.indent(tree=new_tree)
    new_xml_string: str = ET.tostring(
        element=new_tree.getroot(), encoding="utf-8", method="xml").decode()
    rewrite_xml(input_filepath=input_filepath, output_filepath=output_filepath,
                xml_string=new_xml_string, xml_declaration=xml_declaration)
    if change_name:
        normalise_names(input_filepath=input_filepath, output_filepath=output_filepath,
                        value_to_change=value_to_change, replacement=replacement, xml_declaration=xml_declaration)
    output_file.close()
    return new_tree


def normalise_xml_dir(dir_path: str, value_to_change: str = "", replacement: str = "", change_name: bool = False, xml_declaration: str | None = XML_HEADER):
    for filepath in tqdm(glob.glob(pathname=dir_path)):
        print(filepath)
        new_xml = normalise_xml(input_filepath=filepath, output_filepath=filepath, value_to_change=value_to_change,
                                replacement=replacement, change_name=change_name, xml_declaration=xml_declaration)
        # new_xml = normalise_names(input_filepath=filepath, output_filepath=filepath, value_to_change=value_to_change, replacement=replacement)
    return


def change_attribute_name(input_filepath: str, output_filepath: str, tag: str, old_attribute: str, new_attribute: str, namespace: str = ""):
    ET.register_namespace(prefix="", uri=XMLNS)
    xml_tree = ET.parse(source=input_filepath)
    tags_to_change: list = xml_tree.findall(
        f".//ns:{tag}[@{old_attribute}]", namespaces={"ns": XMLNS})
    # print(tags_to_change)
    for tag_c in tags_to_change:
        tag_c.set(new_attribute, tag_c.get(old_attribute))
        tag_c.attrib.pop(old_attribute)
    ET.indent(tree=xml_tree)
    new_xml_string: str = ET.tostring(
        element=xml_tree.getroot(), encoding="utf-8", method="xml").decode()
    return rewrite_xml(input_filepath=input_filepath, output_filepath=output_filepath, xml_string=new_xml_string)


def change_attribute_name_dir(dir_path: str, tag: str, old_attribute: str, new_attribute: str, namespace: str = ""):
    for filepath in glob.glob(pathname=dir_path):
        if "MAZ" in filepath:
            print(filepath)
            change_attribute_name(input_filepath=filepath, output_filepath=filepath, tag=tag,
                                  old_attribute=old_attribute, new_attribute=new_attribute, namespace=XMLNS)
    return


def reformat_first_page():
    return


def update_xml_body(input_filepath: str, output_dir: str, text_dir_path: str, engine: str | None = None, xml_declaration: str | None = XML_HEADER):
    input_file = open(file=input_filepath, mode="r", encoding="utf-8")
    if xml_declaration is None:
        # retrieve xml_declaration
        xml_declaration = ""
        for line in input_file:
            if re.match(pattern=r"^(<TEI).*", string=line):
                break
            xml_declaration += line
    if engine is None:
        engine = os.path.basename(text_dir_path)
        print(engine)
    # register XMLNS
    ET.register_namespace(prefix="", uri=XMLNS)
    # parse the original xml
    og_tree = ET.parse(source=input_filepath)
    og_root = og_tree.getroot()
    og_header = og_root[0]
    og_body = og_root[1][0]
    # set xml:id
    # og_root.set("xml:id", Path(input_filepath).stem)
    # update engine in projectDesc
    og_projectDesc_p_list: list = og_root.findall(
        f".//ns:projectDesc/ns:p", namespaces={"ns": XMLNS})
    if "amélie" in (ET.tostring(og_root, encoding='utf-8', method='xml').lower().decode('utf-8')):
        for project_p in og_projectDesc_p_list:
            if "kraken" in project_p.text.lower():
                project_p.text = f"L'édition présentée ici est issue d'une transcription manuelle réalisée par Amélie Hip."
        print(project_p.text)
        print("Manual transcription.")
    else:
        for project_p in og_projectDesc_p_list:
            if "kraken" in project_p.text.lower():
                project_p.text = f"L'édition présentée ici est issue d'un processus d'OCRisation réalisé avec {engine}."
                print(project_p.text)
        # update the body of the document
        # keep the first page
        dummy_root = ET.Element("dummy_root")
        dummy_root.text = ""
        dummy_tree = ET.ElementTree(element=(dummy_root))
        # first_page_str:str = ""
        capture: bool = False
        for element in og_body.iter():
            # print(capture)
            # print(element.tag)
            if element.tag == f"{{{XMLNS}}}pb":
                if element.attrib.get("n") == "1":
                    capture = True
                else:
                    capture = False
                    break
            if capture:
                dummy_subelement = ET.SubElement(
                    dummy_root, element.tag, element.attrib)
                dummy_subelement.text = element.text
                dummy_subelement.tail = element.tail
        og_pb1: str = ET.tostring(
            element=dummy_root, encoding="unicode", xml_declaration=False)
        # make new body
        new_text_path: str = os.path.join(
            text_dir_path, f"{Path(input_filepath).stem}.txt")
        with open(new_text_path, "r") as text_file:
            # print("before")
            # print(og_pb1)
            og_pb1 = re.sub(pattern=r"<.*dummy_root.*?>",
                            repl="", string=og_pb1)
            # print("after")
            # print(og_pb1)
            new_text: str = text_file.read()
            pb2_match = re.match(r"(.*)(<pb n=\"2\" />)(.*)",
                                 new_text, flags=re.DOTALL)
            if pb2_match is not None:
                # print(re.match(r"<pb n=\"1\" />(.*)<pb n=\"2\" />", new_text, re.DOTALL))
                new_text = re.sub(
                    pattern=r"<pb n=\"1\" />(.*)<pb n=\"2\" />", repl=f"{og_pb1}<pb n=\"2\" />", string=new_text, flags=re. DOTALL)
                # print(new_text)
            else:
                new_text = re.sub(pattern=r"<pb n=\"1\" />(.*)",
                                  repl=og_pb1, string=new_text, flags=re.DOTALL)
            # replace new body in <text>
            text_tag = og_root.find(f".//ns:text", namespaces={"ns": XMLNS})
            if text_tag is not None:
                text_tag.clear()
                text_tag.append(ET.fromstring(
                    f"<body><p>{new_text}</p></body>"))
            # print(ET.tostring(og_root, encoding="utf-8", method="xml").decode("utf-8"))
            # save new xml file
    with open(os.path.join(output_dir, os.path.basename(input_filepath)), "w") as output_file:
        ET.indent(og_tree)
        output_file.write(
            f"{xml_declaration}{ET.tostring(og_root, encoding='utf-8', method='xml').decode('utf-8')}")
    return

    # keep track of figures to re-insert them in the corrected text in the appropriate location later
    # figure_elements: list[dict] = []
    # for element in reversed(list(og_body.iter())):
    #    if element.tag == f"{{{XMLNS}}}figure":
    #        figure_loc_dict:dict = {"figure_el": element, "context":None, "pb": None}
    #        figure_elements.append(figure_loc_dict)
    #        continue
    #    elif len(figure_elements) != 0:
    #        #print(f"tag: {element.tag}")
    #        #print(f"tail:{element.tail}")
    #        if element.tag == f"{{{XMLNS}}}pb":
    #            if figure_elements[-1]["pb"] is None:
    #                figure_elements[-1]["pb"] = element.attrib.get("n")
    #        else:
    #            if figure_elements[-1]["context"] is None:
    #                figure_elements[-1]["context"] = element.tail
    # print(figure_elements)
    return


if __name__ == "__main__":
    # normalise_xml(input_filepath=test_file1)
    # normalise_xml(input_filepath=test_file2)
    # normalise_xml(input_filepath=test_file3)
    # normalise_xml(input_filepath=test_file4)
    # normalise_xml(input_filepath=test_file5, output_filepath="temp.xml")
    # normalise_xml(input_filepath=test_file6, output_filepath="temp_xml/temp.xml")
    # normalise_xml(input_filepath=test_file7, output_filepath="temp_xml/temp.xml")
    # tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
    # normalise_names(input_filepath=test_file8, output_filepath="temp_xml/temp.xml", value_to_change="pièce de théâtre", replacement="texte de forme théâtrale")
    # tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
    # test_stats()
    # change_attribute_name(input_filepath=test_BM_file, output_filepath="temp_xml/BM.xml", tag="pb", old_attribute="n", new_attribute="vue", namespace=namespace)
    change_attribute_name_dir(dir_path=all_dir, tag="pb",
                              old_attribute="n", new_attribute="vue", namespace=XMLNS)

    # normalise_xml_dir(dir_path=test_dir, value_to_change="pièce de théâtre", replacement="texte de forme théâtrale", change_name=True)
    # normalise_xml_dir(dir_path="../Mazarinades/Antonomaz/*.xml", value_to_change="pièce de théâtre", replacement="texte de forme théâtrale", change_name=True)

    # update tests
    # test_dir: str = "../tests"
    # text_dir_path: str = "../../Ressources/#PDF_to_TEI/2-textes_concat/kraken4.3.13.dev25"
    # update_xml_body(input_filepath=test_file11, output_dir=test_dir, text_dir_path=text_dir_path, xml_declaration=XML_HEADER)
    # maz_dir_1_100: str = "../Mazarinades/1-100/"
    # for filepath in glob.glob("../Mazarinades/1-100/*"):
    #    update_xml_body(input_filepath=filepath, output_dir=maz_dir_1_100, text_dir_path=text_dir_path, xml_declaration=XML_HEADER)
