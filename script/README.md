# Scripts

Ce dossier contient des scripts permettant d'automatiquement corriger ou enrichir l'encodage des mazarinades.

## `tei_to_csv.py`

Ce script permet de produire un [fichier csv](https://github.com/Antonomaz/Corpus/blob/main/output/corpus.csv) reprenant les métadonnées principales des fichiers qui composent le corpus.

## `episodes_Moreau`

Ce dossier contient la liste des évènements de la Fronde définie par Moreau. Un script, [`add_episodes.py`](https://github.com/Antonomaz/Corpus/blob/main/script/episodes_Moreau/add_episodes.py), permet de les ajouter aux mazarinades correspondantes. 

La liste est consultable [ici](https://github.com/Antonomaz/Corpus/blob/main/script/episodes_Moreau/episodes_Moreau.json).

## `corr_num.py`

Ce script permet simplement de corriger la numérotation des éléments `pb` d'un fichier XML.