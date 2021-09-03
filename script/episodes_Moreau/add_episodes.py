import json
from lxml import etree
import re
import glob

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


def get_Moreau_id(fichier_Moreau):
    # On récupère tous les IDs des mazarinades concernées par les épisodes Moreau
    liste_Moreau_id = []
    for evt_id, values in fichier_Moreau.items():
        liste_Moreau_id += values["mazarinades"]
    return liste_Moreau_id



def check_id(liste_XML_id, liste_Moreau_id):
    # Cette fonction vise à conserver uniquement les IDs qui se retrouvent à la fois dans la liste des fichiers xml et des évènements Moreau.
    liste_matching_id = []
    # On ne conserve que le début de l'identifiant du fichier xml (pour enlever notamment _GALL, _GBOOKS et _MAZ)
    for xml_id in liste_XML_id:
        # Les suppléments ne sont pas concernés par les épisodes Moreau, on les passe;
        if re.match("Moreau[1,2,3]?suppl", xml_id):
            pass
        elif re.match("Moreau[0-9]+_(GALL|MAZ|GBOOKS)", xml_id) is not None:
            xml_id_source = re.match("Moreau[0-9]+_(GALL|MAZ|GBOOKS)", xml_id)[0]
            xml_id = re.match("Moreau[0-9]+", xml_id)[0]
            if xml_id in liste_Moreau_id:
                liste_matching_id.append(xml_id_source)
        else:
            pass
    liste_matching_id.sort()
    liste_matching_id = set(liste_matching_id)
    #print(liste_matching_id)
    #print(len(liste_matching_id))
    return liste_matching_id

def add_evt(matching_list, files, Moreau):
    # Cette fonction permet d'ajouter les évènements Moreau au sein des fichiers xml

    for file in files:
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(file, parser)
        xml_id = doc.xpath("//tei:TEI/@xml:id", namespaces=ns)[0]

        if xml_id in matching_list:
            # Nouveaux éléments à inclure :
            settingDesc = etree.Element("{http://www.tei-c.org/ns/1.0}settingDesc")
            setting = etree.Element("{http://www.tei-c.org/ns/1.0}setting")
            date = etree.Element("{http://www.tei-c.org/ns/1.0}date")
            p = etree.Element("{http://www.tei-c.org/ns/1.0}p")
            profileDesc = doc.xpath('//tei:profileDesc', namespaces=ns)[0]
            textClass = doc.xpath('//tei:profileDesc/tei:textClass', namespaces=ns)[0]

            # On s'assure de passer les fichiers qui ont déjà un settingDesc
            if len(doc.xpath('//tei:profileDesc/tei:settingDesc', namespaces=ns)) >= 1:
                pass
            else:
            
                # On supprime la source dans l'identifiant pour pouvoir matcher les identifiants contenus dans le JSON
                xml_id = re.match("Moreau[0-9]+", xml_id)[0]
                for evt_id, values in Moreau.items():
                    if xml_id in values["mazarinades"]:
                        p.text = values["title"]
                        setting.append(p)
                        date.text = values["date"]
                        setting.append(date)
                        date.attrib["when"] = values["date"]
                        setting.attrib["{http://www.w3.org/XML/1998/namespace}id"] = evt_id
                        setting.attrib["source"] = "Moreau"
                        settingDesc.append(setting)
                        profileDesc.insert(profileDesc.index(textClass)+1, settingDesc)
    
        etree.indent(doc)
        with open(file, "w+") as sortie_xml:
            output = etree.tostring(doc, pretty_print=True, encoding='utf-8', xml_declaration=True).decode(
                        'utf8')
            sortie_xml.write(str(output))


if __name__ == "__main__":
    # À MODIFIER : faire un vrai glob pour indiquer le chemin de fichier en entrée, voir pour la récursivité 
    files = glob.glob("../../Mazarinades/**/*.xml", recursive=True)

    liste_XML_id = []
    for file in files:
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(file, parser)
        xml_id = doc.xpath("//tei:TEI/@xml:id", namespaces=ns)[0]
        liste_XML_id.append(xml_id)
    liste_XML_id.sort()
    
    # On récupère les identifiants Moreau contenu dans le json
    Moreau = open('episodes_Moreau_v2.json', 'r')
    Moreau = json.load(Moreau)
    liste_Moreau_id = get_Moreau_id(Moreau)
    liste_Moreau_id.sort()
    
    # On compare les deux listes 
    matching_list = check_id(liste_XML_id, liste_Moreau_id)

    # Fonction d'ajout des évènements
    add_evt(matching_list, files, Moreau)


