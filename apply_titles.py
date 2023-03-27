from bs4 import BeautifulSoup
import glob

liste_fichiers = glob.glob("Mazarinades/*/*.xml")
liste_fichiers = [x for x in liste_fichiers if "Doublons" not in x and "to_do" not in x]
import os

import json
import tqdm, re
with open("titres_corriges_Moreau.json") as f:
  dic = json.load(f)

for path_html in tqdm.tqdm(liste_fichiers):
  try:
    good_title = dic[re.split("/", path_html)[-1]]
  except:
    continue
  if "& " in good_title:
    good_title = re.sub("& ", "&amp; ", good_title)

  is_title = False
  done = False
  with open(path_html) as f:
    lignes = f.readlines()
  out = []
  for l in lignes:
    if done==True:
      out.append(l)
    elif "<title " in l:#TODO pas titleS!
      is_title=True
      if "</title>" in l:
        out.append(f"    <title type=\"main\" source=\"Moreau\">{good_title}</title>\n")
        done = True
    elif "</title>" in l:
      out.append(f"    <title type=\"main\" source=\"Moreau\">{good_title}</title>\n")
      done = True
    elif is_title==False:
      out.append(l)
  with open(path_html, "w") as w:
    w.write("".join(out))
  os.system(f"xmllint --noout {path_html}")
#Fichier Mazarinades/1-100/Moreau13
#Check NBR lignes

