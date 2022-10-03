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

    # Author and its id
    authors = doc.xpath("//tei:teiHeader//tei:sourceDesc/tei:bibl//tei:author", namespaces=ns)
    for author in authors :
        data = {}
        if author.xpath(".//tei:orgName/text()", namespaces=ns):
            orgname = author.xpath(".//tei:orgName/text()", namespaces=ns)[0]
            data["orgName"] = clean_text(orgname)
        else:
            data["orgName"] = ""

        if author.xpath(".//tei:persName/text()", namespaces=ns):
            persName = author.xpath(".//tei:persName/text()", namespaces=ns)[0]
            data["persName"] = clean_text(persName)
        else:
            data["persName"] = ""

        if author.xpath(".//tei:persName/tei:forename/text()", namespaces=ns):
            forename = author.xpath(".//tei:persName/tei:forename/text()", namespaces=ns)[0]
            data["forename"] = clean_text(forename)
        else:
            data["forename"] = ""

        if author.xpath(".//tei:persName/tei:surname/text()", namespaces=ns):
            surname = author.xpath(".//tei:persName/tei:surname/text()", namespaces=ns)[0]
            data["surname"] = clean_text(surname)
        else:
            data["surname"] = ""

        if author.xpath(".//tei:persName/tei:addName/text()", namespaces=ns):
            addname = author.xpath(".//tei:persName/tei:addName/text()", namespaces=ns)[0]
            data["addname"] = clean_text(addname)
        else:
            data["addname"] = ""

        if author.xpath("./@ref", namespaces=ns):
            data["author_id"] = author.xpath("./@ref", namespaces=ns)[0]
        else:
            data["author_id"] = ""

        if doc.xpath("//tei:TEI/@xml:id", namespaces=ns):
            data["id"] = doc.xpath("//tei:TEI/@xml:id", namespaces=ns)[0]
        else:
            data["id"] = ""

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
        output = list({v['author_id']:v for v in output}.values())

        
    
    with open('../output/author_unique.csv', 'w+', newline='') as csvfile:
        fieldnames = ['id', 'author_id', 'orgName', 'persName', 'forename', 'surname', 'addname']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for item in output:
            writer.writerow(item)



    