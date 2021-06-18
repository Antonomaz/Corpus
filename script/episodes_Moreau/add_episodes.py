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
        elif re.match("Moreau[0-9]+", xml_id) is not None:
            xml_id = re.match("Moreau[0-9]+", xml_id)[0]
            if xml_id in liste_Moreau_id:
                liste_matching_id.append(xml_id)
        else:
            pass
    liste_matching_id.sort()
    print(liste_matching_id)
    print(len(liste_matching_id))
    # ATTENTION : QUAND DEUX ORIGINES POUR UN MÊME IDENTIFIANT, MODIFIER LA STRUCTURE DU SCRIPT POUR CONSERVER LE NOM ORIGINEL DE FICHIER
    return liste_matching_id




if __name__ == "__main__":
    # À MODIFIER : faire un vrai glob pour indiquer le chemin de fichier en entrée, voir pour la récursivité 
    files = glob.glob("../../Mazarinades/**/*.xml", recursive=True)
    # Liste contenant l'ensemble des IDs des fichiers XMl encodés
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