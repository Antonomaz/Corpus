from lxml import etree
import re
import glob
import pandas as pd

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


def add_episode(file, liste_moreau):
    print(file)
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(file, parser)
    # On récupère l'ID du fichier XML et on ne conserve que la numéro Moreau
    xml_id = doc.xpath("//tei:TEI/@xml:id", namespaces=ns)[0]
    # Prise en compte des suppléments
    if re.match("Moreau[1,2,3]?suppl", xml_id):
        xml_id = re.match("Moreau[1,2,3]?suppl[0-9]+", xml_id)[0]
    elif re.match("(Moreau|Socard|Labadie)[0-9]+", xml_id):
        xml_id = re.match("(Moreau|Socard|Labadie)[0-9]+", xml_id)[0]
    else:
        pass

    df_maz=pd.read_csv(liste_moreau, sep=',', header=0)
    r=re.compile(xml_id+"$")
    for i in range(len(df_maz)):
        id_maz_tab = str(df_maz.loc[i, "ID"])
        #id_maz_tab = re.split("/", id_maz_tab)[-1]
        m = r.match(id_maz_tab)
        if m:
            abstract = doc.xpath("//tei:abstract", namespaces=ns)[0]
            p = etree.SubElement(abstract, "p")
            p.attrib["source"] = "Moreau"
            p.text = str(df_maz.loc[i, "Notice"])
    etree.indent(doc)
    with open(file, "w+") as sortie_xml:
        output = etree.tostring(doc, pretty_print=True, encoding='utf-8', xml_declaration=True).decode(
                        'utf8')
        sortie_xml.write(str(output))


def check(file):
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(file, parser)
    if doc.xpath("//tei:abstract/tei:p[@source='Moreau']", namespaces=ns):
        return "NO"
    else:
        return "YES"


if __name__ == "__main__":
    # À MODIFIER : faire un vrai glob pour indiquer le chemin de fichier en entrée, voir pour la récursivité 
    files = glob.glob("../Mazarinades/**/*.xml", recursive=True)
    Moreau = "ListeMazarinades - Documents_all.csv"

    for file in files:
        status = check(file)
        if status == "YES":
            add_episode(file, Moreau)