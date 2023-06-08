import xmltodict
import os
import glob
import texte

test_dir: str = "../Mazarinades/1-100/*"
test_path: str = "../Mazarinades/1-100/Moreau91_GALL.xml"
test_file5:str = "../tests/Mazarinades_tests/2001-2100/Moreau2022_GBOOKS.xml"

# print(xml_to_dic(test_path)["teiHeader"]["fileDesc"]["titleStmt"]["respStmt"]["persName"][5])
#for path in glob.glob(pathname=test_dir):
#    #print(texte.Texte(path).corrector)
#    texte.Texte(path)
#    print("\n")
    # print((texte.Texte(test_path).get_header))
#texte.Texte(test_path)
f5 = texte.Texte(test_file5)
print(f5.header)
# ajout des when