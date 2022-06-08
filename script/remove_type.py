from argparse import Namespace
from os import remove
from lxml import etree
import re
import glob

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def remove_type(doc):
    if doc.xpath("//tei:TEI/@type", namespaces=ns):
        TEI_ = doc.xpath("//tei:TEI", namespaces=ns)[0]
        type = doc.xpath("//tei:TEI/@type", namespaces=ns)[0]
        print(type)
        if type == "recueil":
            pass
        else:
            del TEI_.attrib["type"]
        return type

    
def genre(doc, type):
    result = []
    if type == "mazarinades_burlesques" or type == "mazarinades_burlesque":
        if doc.xpath("//tei:term[@type='subgenre']", namespaces=ns):
            textes = doc.xpath("//tei:term[@type='subgenre']", namespaces=ns)
            for texte in textes :
                if texte.text == "burlesque":
                    result.append("no")
                else :
                    result.append("yes")
        else :
            result.append("yes")

    if type == "mazarinades_narration" :
        if doc.xpath("//tei:term[@type='genre']", namespaces=ns):
            textes = doc.xpath("//tei:term[@type='genre']", namespaces=ns)
            for texte in textes :
                if texte.text == "narration" or texte.text == "Narration":
                    result.append("no")
                else :
                    result.append("yes")
        else :
            result.append("yes")

    if type == "mazarinades_lettres" :
        if doc.xpath("//tei:term[@type='genre']", namespaces=ns):
            print("ok") 
            textes = doc.xpath("//tei:term[@type='genre']", namespaces=ns)
            for texte in textes :
                if texte.text == "lettres" or texte.text == "Lettres" or texte.text == "Lettre" or texte.text == "lettre":
                    result.append("no")
                else :
                    result.append("yes")

        else :
            result.append("yess")

    print(result)
    return doc, result, type

def add_genre(result, doc, type):
    keywords = doc.xpath("//tei:keywords", namespaces=ns)[0]
    if "no" in result:
        pass
    else:
        if type == "mazarinades_burlesques" or type == "mazarinades_burlesque":
            term = etree.SubElement(keywords, "term")
            term.attrib["type"] = "subgenre"
            term.text = "burlesque" 
        elif type == "mazarinades_lettres":
            term = etree.SubElement(keywords, "term")
            term.attrib["type"] = "genre"
            term.text = "lettre"
        elif type == "mazarinades_narration":
            term = etree.SubElement(keywords, "term")
            term.attrib["type"] = "genre"
            term.text = "narration"
    return doc


if __name__ == "__main__":
    files = glob.glob("../to_do/*.xml", recursive=True)

    for file in files:
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(file, parser)
        type = remove_type(doc)
        doc, result, type = genre(doc, type)
        doc = add_genre(result, doc, type)
        etree.indent(doc)
        with open(file, "w+") as sortie_xml:
            output = etree.tostring(doc, pretty_print=True, encoding='utf-8', xml_declaration=True).decode(
                        'utf8')
            sortie_xml.write(str(output))
        

        
