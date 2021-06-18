import json

Moreau = open('episodes_Moreau.json', 'r')
Moreau = json.load(Moreau)

# L'idée est de changer la structure du fichier json pour avoir une entrée par évènement.
new_Moreau = {}
# Chaque évènement Moreau se voit donner un identifiant unique.
evt_Moreau = "evt_Moreau_"
evt_Moreau_nb = 1

# Les numéros Moreau sont modifiés pour correspondre aux normes d'identification du projet Antonomaz.
def correct_id(liste):
    new_list = []
    for id in liste:
        good_id = "Moreau" + id
        new_list.append(good_id)
    return new_list


# Les dates (parfois incomplètes) sont corrigés pour correspondre au format utilisé dans l'attribut @when.
def correct_date(date):
    if date == "N/A":
        new_date = ""
    elif date[:2] == "00":
        new_date = str(date[6:10]) + "-" + str(date[3:5])
    else:
        new_date = str(date[6:10]) + "-" + str(date[3:5]) + "-" + str(date[0:2])
    return new_date



for year, year_list in Moreau.items():
    for evt in year_list:
        # Chaque évènement correspond à présent à un dictionnaire contenant les informations qui nous intéresse.
        new_evt = {}
        new_evt["title"] = evt["Etiquette Moreau"]
        new_date = correct_date(evt["date"])
        new_evt["date"] = new_date
        new_evt["page"] = evt["page"]
        evt["liste"] = correct_id(evt["liste"])
        new_evt["mazarinades"] = evt["liste"]
        id = str(evt_Moreau) + str(evt_Moreau_nb)
        new_Moreau[id] = new_evt
        evt_Moreau_nb += 1


episodes_Moreau_v2 = open("episodes_Moreau_v2.json", "w+")
json.dump(new_Moreau, episodes_Moreau_v2)





