from lxml import etree
import csv
import glob
import re

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def clean_text(entry):
    "Function used to remove blank new lines"
    entry = entry.replace("\n", "")
    entry = re.sub('\s{2,}', ' ', entry)
    return entry


def get_data(doc):
    """
    Function used to retrieve specifics data in a dict.
    :param doc: a XML document
    :return: a dictionary
    """
    data = {}
    # ID
    if doc.xpath("//tei:TEI/@xml:id", namespaces=ns):
        data["id"] = doc.xpath("//tei:TEI/@xml:id", namespaces=ns)[0]
    else:
        data["id"] = ""

    # Author and its id
    author = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:author", namespaces=ns)[0]
    if author.xpath(".//tei:surname/text()", namespaces=ns) and author.xpath(".//tei:forename/text()", namespaces=ns):
        surname = author.xpath(".//tei:surname/text()", namespaces=ns)[0]
        forename = author.xpath(".//tei:forename/text()", namespaces=ns)[0]
        _author = surname + ", " + forename
        data["author"] = clean_text(_author)
    elif author.xpath(".//tei:surname/text()", namespaces=ns):
        _author = author.xpath(".//tei:surname/text()", namespaces=ns)[0]
        data["author"] = clean_text(_author)
    else:
        data["author"] = ""
    if author.xpath("./@ref", namespaces=ns):
        data["author_id"] = author.xpath("./@ref", namespaces=ns)[0]
    else:
        data["author_id"] = ""

    # Publisher and its id
    publisher = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:publisher", namespaces=ns)[0]
    if publisher.xpath(".//tei:surname/text()", namespaces=ns) and publisher.xpath(".//tei:forename/text()", namespaces=ns):
        surname = publisher.xpath(".//tei:surname/text()", namespaces=ns)[0]
        forename = publisher.xpath(".//tei:forename/text()", namespaces=ns)[0]
        _publisher = surname + ", " + forename
        data["publisher"] = clean_text(_publisher)
    elif publisher.xpath(".//tei:surname/text()", namespaces=ns):
        _publisher = publisher.xpath(".//tei:surname/text()", namespaces=ns)[0]
        data["publisher"]  = clean_text(_publisher)
    else:
        data["publisher"] = ""
    if publisher.xpath("./@ref", namespaces=ns):
        data["publisher_id"] = publisher.xpath("./@ref", namespaces=ns)[0].replace("\n", "")
    else:
        data["publisher_id"] = ""

    # Title
    if doc.xpath("//tei:teiHeader//tei:titleStmt/tei:title[@type='main']/text()", namespaces=ns):
        _title = doc.xpath("//tei:teiHeader//tei:titleStmt/tei:title[@type='main']/text()", namespaces=ns)[0]
        data["title"] = clean_text(_title)
    else:
        data["title"] = ""

    # Date
    if doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl//tei:date/@when", namespaces=ns):
        # We only keep the 4 first characters
        data["date"] = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl//tei:date/@when", namespaces=ns)[0][:4] 
    else:
        data["date"] = ""

    # PubPlace and its id
    if doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:pubPlace/text()", namespaces=ns):
        _pubPlace = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:pubPlace/text()", namespaces=ns)[0]
        data["pubPlace"] = clean_text(_pubPlace)
    else: 
        data["pubPlace"] = ""
    if doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:pubPlace/@ref", namespaces=ns):
        data["pubPlace_id"] = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:pubPlace/@ref", namespaces=ns)[0]
    else:
        data["pubPlace_id"] = ""
    
    # Pages
    if doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:extent/tei:measure[@unit='page']", namespaces=ns):
        data["pages"] = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl/tei:extent/tei:measure/@quantity", namespaces=ns)[0]
    else:
        data["pages"] = ""

    # Stamp
    if doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:msDesc//tei:stamp/text()", namespaces=ns):
        data["stamp"] = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:msDesc//tei:stamp/text()", namespaces=ns)[0]
    else:
        data["stamp"] = ""

    return data



if __name__ == "__main__":
    # À MODIFIER : faire un vrai glob pour indiquer le chemin de fichier en entrée, voir pour la récursivité 
    files = glob.glob("../Mazarinades/**/*.xml", recursive=True)
    output = []
    for file in files:
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(file, parser)
        data = get_data(doc)
        output.append(data)
    
    with open('../output/corpus.csv', 'w+', newline='') as csvfile:
        fieldnames = ['id', 'title', 'author', 'author_id', 'publisher', 'publisher_id', 'date', 'pubPlace', 'pubPlace_id', 'pages', 'stamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for item in output:
            writer.writerow(item)



    