**Documentation synthèse des missions de stage de Mélanie Lecha et Camille Roblin (février-juillet 2021)**

# LIENS VERS LES RESSOURCES DU PROJET

## Plateformes publiques :
https://cahier.hypotheses.org/antonomaz

http://stih-sorbonne-universite.fr/dokuwiki/doku.php?id=antonomaz

## Tableurs internes au projet :
*	Avancée_travail_corpus : Documente l’avancée de la collecte des données PDF / XML
	* Feuille 1 « Corpus_complet » : liste de toutes les mazarinades recensées par les bibliographes et métadonnées (Vers/Prose, corpus, url PDF, url notice BM, conversion XML, transcription XML)
	* Feuille 2 « PDF_à_vérifier » : liste de documents non répertoriés par les bibliographes trouvés lors de la recherche de PDF et potentiellement intéressants
https://docs.google.com/spreadsheets/d/1GTbLJyyXfCAsFLFyTTVTc4ZMTyitsOO24xiPUn2Rp30/edit#gid=0
*	ListeMazarinades :  Océrisation des bibliographies et enrichissement des métadonnées, gestion lots 1 et 2 de la BM, quelques travaux sur corpus et métadonnées (12 feuilles)
https://docs.google.com/spreadsheets/d/1uIFuI-9IKC9EKV8jgcFkYhmJq6jhkxCiq3kzfzKD_eg/edit#gid=2129771631
*	CORPUS : Obsolète. Outil non mis à jour qui avait servi pour la première collecte de PDF. 
https://docs.google.com/spreadsheets/d/1PwAnVkHFILKbt059S5hmdEAdRnN7A_X8zNUd9iBY6n8/edit#gid=477833049

## Scripts et outils développés pour le projet :
https://github.com/Antonomaz/Corpus/tree/main/script : Dépôt de tous les scripts utiles à la préparation et à la gestion automatisée des données, ainsi que quelques outils pour extraire des informations du corpus XML-TEI.

https://github.com/rundimeco/antonomaz_tools : Dépôt des scripts réalisés par Gaël.

https://lejeunegael.fr/resources/Moreau/test.html : Moteur de recherche des Mazarinades.

## Dépots des données du projet :
*	https://sharedocs.huma-num.fr/#/5910/21081 : Accès aux PDF
*	https://github.com/Antonomaz/Corpus : Accès aux XML et visualisations statistiques des données


# RECHERCHE ASSISTEE DE PDF SUR GBOOKS/GALLICA

1.	Préparer la liste des titres à rechercher sur GBOOKS ou GALLICA sous la forme d’un fichier .txt avec id_titre(tabulation)titre(saut de ligne).

2.	Ouvrir le script "Search_pdf_on_..._from_a_list.ipynb".

3.	En bas de la page, dans la section " Exemple d’utilisation ", il y a deux fonctions launch_api() et download_results(). Remplacer le nom du fichier .txt par celui créé dans l’étape 1. En valeur de la variable regex, indiquer la ou les années de publication qui vous intéressent pour filtrer les résultats de l’API (si plusieurs années, séparer les dates par une barre verticale). 
	* Par défaut dans ce script, l’API Gallica est paramétrée pour ne donner que des résultats correspondants à des monographies du 17ème siècle. Pour changer ce paramètre, il faut modifier la variable chaine2 dans def launch_api() en s’appuyant sur la documentation de l’API Gallica disponible à cette adresse : https://api.bnf.fr/fr/api-gallica-de-recherche
	* L’API GBOOKS fonctionne avec un système de clé à créer dans " l’API console " de Google. Il faut coller cette clé en paramètre de la fonction launch_api_gbooks(). Pour plus d’informations : https://developers.google.com/books/docs/v1/using

4.	Cliquer sur Cell > Run All et attendre que le sablier dans l’onglet en haut ait disparu. Si aucun message d’erreur n’apparait dans le notebook, un dossier output a été créé au même niveau que le script. Ouvrir le fichier output_similar.txt qui se trouve à l’intérieur.
	* Dans ce fichier apparaît la liste de tous les titres proposés par l’API de GBOOKS ou de Gallica en réponse aux titres dans le fichier .txt que nous lui avons soumis à l’étape 1. Les réponses se présentent sous la forme : date de publication, titre du document, lien vers le pdf. 
	* Seuls les titres pour lesquels la date de publication coïncide avec celle indiquée dans la variable regex sont affichés.
	* En raison de la forte variation orthographique des documents, nous récupérons les 40premiers résultats du moteur de recherche GBOOKS/Gallica, ce qui signifie que beaucoup de titres sans rapport avec notre requête risquent d’apparaitre. Pour pallier ce problème, un comparateur de similarité lit chacun des titres et propose des correspondances avec les requêtes soumises à l’étape 1 s’il en trouve.
	* Cet indicateur de similarité se présente sous la forme D=score de similarité, (ID=id_du_document) : titre du document soumis à l’étape 1.
	* Si cette ligne n’apparait pas, c’est que le comparateur n’a pas trouvé de correspondance entre le résultat de l’API et les titres recherchés.

5.	Le résultat de l’API semble être un PDF recherché pour le corpus de Mazarinades ? Pour confirmer l’identification du document, il faut ouvrir le PDF et vérifier que le nombre de pages, l’éditeur ou la date de publication coïncide avec la notice Moreau. Le moteur de recherche des mazarinades est utile pour cet usage (https://lejeunegael.fr/resources/Moreau/test.html)

6.	Après avoir confirmé l’identification du document et l’avoir enregistré (format de nommage : Moreau5_GALL.pdf), remplir les métadonnées dans le tableur " Avancée_travail_corpus " : texte en vers ou en prose (V ou P), lien url vers le PDF et permalien de la notice BM si elle existe. Si elle n’existe pas, compléter par la mention " sans notice ".
	* Pour trouver facilement si une notice existe sur le site de la BM, se rendre sur https://mazarinades.bibliotheque-mazarine.fr/ et écrire Moreau+id_moreau (ex : Moreau1584)

# CHAINE DE TRAITEMENT PDF VERS XML-TEI

## Océrisation

*	Faire passer les PDF voulus dans la pipeline développée par Jean-Baptiste Tanguy sous kraken. Lien vers le git de IMG2TXT : https://github.com/jbtanguy/IMG2TXT
*	/ ! \ Cette pipeline ne fonctionne que sous Linux. L’océrisation peut être assez longue, aussi il est conseillé de ne pas la faire en local mais sur les serveurs de la Sorbonne. 
*	Récupérer ensuite les fichiers txt générés (un texte = un dossier). 

## Concaténer les fichiers 

*	L’océrisation crée un fichier par page. Aussi est-il nécessaire, avant de générer le XML du document, d’effectuer une concaténation pour réunir l’ensemble des pages d’un document en un seul fichier. Lors de cette procédure, un encodage automatique du texte est aussi réalisé (balisage des lignes et changement de pages)
*	Il faut placer le script de concaténation " concatenate_and_encode_ocr_output.ipynb " à l’endroit où sont situés les dossiers des fichiers à concaténer et lancer le script (Cell > Run all). La regex en paramètre sert à éliminer les deux premières pages des océrisations qui sont des notices Gallica/GBooks.
*	Tous les fichiers concaténés sont rangés dans un dossier " sortie_concaten ". 

## Générer automatiquement les XML

*	Le script " transform_txt_file_to_tei.ipynb " est à placer dans le dossier " sortie_concaten " afin de pouvoir générer les XML avec le texte des documents à l’intérieur. 
*	Il reproduit toute la structure XML décidée par l’équipe Antonomaz avec des métadonnées préremplies
*	Une partie du script utilise les données des tableurs "Avancée_travail_corpus" et "ListeMazarinades", à savoir : l’id du document, le titre, la date et le lieu de publication du document + geonames, le nombre de pages,l’URL du fac-similé, l’URL de la notice mazarine.
*	Les deux tableurs doivent être exportés au format .tsv (séparateur : tabulation) et placés au même niveau que le script. Le nom des colonnes des tableurs ne doivent pas être modifiés car le script se base sur cela pour récupérer les métadonnées.

## Relecture des XML

*	Malgré les métadonnées préremplies et le balisage automatique du texte, une relecture est nécessaire. 
*	Ouvrir les fichiers XML à l’aide d’un projet (fichier xpr) peut être utile. Nous avons créé un projet intitulé " Antonomaz.xpr ", situé dans le dossier " Corpus " du git. Le projet permet de pouvoir modifier plusieurs fichiers en même temps et ainsi de gagner du temps.
*	Pour tous les choix et règles d’encodage, consulter le fichier " ODD_Antonomaz.html ".
*	/ ! \ Nos XML renvoyant en première ligne vers cet ODD, toute erreur d'encodage devrait être signalée dans une application telle que Oxygen XML editor.

### Métadonnées 
*	Compléter le geonames de la balise < pubPlace > si le champs n'a pas été pré-rempli: https://www.geonames.org/
*	Compléter les balises < author > et < publisher > en ajoutant leurs isnis (https://isni.oclc.org/).
*	/ ! \ Les geonames et les isnis doivent toujours être les mêmes. Si, par exemple, dans un fichier, l’éditeur Jean Dupont a l’isni " 1987639043215739 ", tous les fichiers ayant pour éditeur Jean Dupont doivent avoir l’isni précité. Sinon, cela gênera la récupération des informations pour les visualisations et autres traitements. 
*	Remplir la balise < note type= " BM_identifier " > avec l'identifiant du document donné par la Bibliothèque Mazarine, s’il y a une notice.
*	Vérifier la notice mazarine. S’il s’agit de la bonne au regard du document, changer @cert= " low " en @cert= " high ", à la fois pour < note type="BM_identifier" > et < ref type= "BM_notice" >. Si la notice ne correspond pas, rechercher la bonne sur mazarinum. Si elle n’existe pas, supprimer les informations.
*	Compléter la balise < format > en s'appuyant sur les métadonnées de la BNF de la BM par exemple.
*	Compléter l'ensemble du < msDesc > (informations liées au lieu de conservation du document original)
*	Indiquer True dans la balise < stamp > si un tampon se trouve sur la première page du document, False sinon.
*	Optionnel : copier les notes sur le document que l'on peut trouver sur la BM < p source="BM_notes" > ou sur le site de la BnF < p source="BnF_notes" >.
*	Optionnel : compléter les keywords.

### Texte
*	Supprimer le bruit évident généré par l'OCR.
*	Vérifier que la pagination est correcte : selon les numérisations, il peut y avoir des décalages. Si besoin, changer le numéro des pages à l’intérieur de la balise < pb >. 
*	Supprimer les pages vides, à l’exception de celle située entre la page de titre et la première page de texte.
*	S’il s’agit d’un texte en prose, encoder l’ensemble dans une seule balise < p >. Retirer  à l’aide d’un CTRL+H les balises < l >< /l >, uniquement utilisées pour les vers.

### Déposer les XML sur github
*	Pour chaque XML relu, cocher la case correspondante dans l’excel " Avancée_travail_corpus ". 
*	Déposer les XML sur le git.

# UTILISATION DE GITHUB

*	Ouvrir la console de l’OS – Linux, Windows ou iOS - en mode administrateur.
*	Un compte sur github est nécessaire pour pouvoir travailler sur le git. Il faudra ensuite accepter l’invitation de la part de l’un des administrateurs du git Antonomaz pour pouvoir travailler dessus. Si jamais vous acceptez un nouveau membre, lui donner les droits administrateurs pour qu’il puisse modifier le git.
*	Pour avoir le contenu du git sur sa machine, faire " git clone https://github.com/Antonomaz ".
*	Avant de déposer quoi que ce soit sur github, toujours faire un git pull branche voulue afin d’avoir les dernières mises à jour et de ne pas créer de conflits. 
*	Mettre les XML dans les dossiers correspondants dans le dossier " Mazarinades " de la branche corpus. Le corpus a été divisé en paquets de 100. Si vous avez un fichier qui entre dans aucun dossier déjà présent, créer un nouveau dossier. Github n’admet pas les dossiers vides. 
*	Une fois les XML placés dans les dossiers correspondants, faire : " git add -A " puis "git commit -m " message expliquant vos modifications " et enfin " git push ". Enfin, entrer son identifiant github puis son mot de passe. 
*	Il est conseillé de déposer les fichiers sur le git après chaque session d’encodage. 
*	Si vous repérez des erreurs au sein des fichiers mis en ligne, merci de les signaler dans " Issues ". Si vous réglez un problème, merci de clore " l’issue ".
*	Si vous souhaitez faire une suggestion d’encodage et marquer la progression, allez dans " Suivi de l’encodage ". 

# ARCHIVES : Documenter la recherche de PDF assistée  + manuelle
**I. Observations sur l'efficacité des API Gallica / Google Books**

*Avec script > Gallica*

* Toujours une sortie - sauf en cas d'erreur de connexion au serveur - même si elle ne correspond pas à la requête envoyée. -> le résultat le plus pertinent n'apparaît pas toujours en première place car gallica est assez sensible au bruit et ne considère pas nécessairement comme pertinent ce qui le serait pour un être humain. 
* Sensibilité aux variations orthographiques -> utilisation de titres tronqués pour tenter de la contourner, mais la solution n'est pas idéale -> il faudrait savoir comment l'API est paramétrée de base pour avoir des sorties plus pertinentes. Pour le moment, il est très difficile de savoir à combien de sorties il faut limiter le script.

*Avec script > Google Books*

* Quelques fois, le document numérisé n'a pas la page de titre numérisée, donc on est obligé de se fier aux métadonnées de GBOOKS pour l'identification du texte (bout de titre écrit dans l'url par exemple)
* Si google books ne trouve pas le document correspondant à la requête, il renvoie un xml vide (plus précis que gallica, mais pas les mêmes logiques non plus). 
* Limitation au niveau du nombre de requêtes par minute et par jour.
* Ne pas resserrer la recherche par titre, rechercher dans "tout" avec comme seule limite la date de publi pour resserrer les résultats => meilleurs résultats car il y a une océrisation sommaire réalisée sur les scans, c'est donc parfois par ce biais qu'on tombe sur un texte dont le titre était orthographié différemment ou qui était à l'intérieur d'un recueil
* Meilleurs résultats avec des titres tronqués (ni trop courts, ni trop longs)
* Parfois GBOOK n'a pas le titre en entier ou a le mauvais titre => intérêt de faire des recherches par petites collocations
* Les articles entre parenthèses dans nos listes ont pu gêner le moteur de rechercher google. Supprimer l'article de début à l'avenir. Exemple : titre chez nous : "Courrier (le) de la Guyenne, apportant le véritable état des affaires." titre gbooks : "Le Courrier de la Guienne, Apportant le veritable Estat des Affaires" Requête uniquement trouvable en mettant "le courrier de la guyenne"
* Pour améliorer le script, possibilité de travailler avec des titres prétronqués après la première virgule ?

*Recherche manuelle > Gallica*

* La recherche manuelle "Titre + intervalle de dates" donne des documents du corpus qui n'apparaissaient pas dans les résultats de l'API. Contourner la variation orthographique en prenant dans les titres des termes qui n'y sont pas sensibles (ou bien moins que d'autres). -> il semble quand même que le moteur de recherche les comprenne assez bien (mieux que l'api?). 
* Certains liens dans la liste des résultats renvoient en fait directement vers d'autres bibliothèques numériques (comme mazarinum) sur lesquelles on peut télécharger (ou pas) le document voulu. -> Pourrait expliquer en partie que certains résultats n'apparaissent pas lors de l'interrogation de l'api. 
*Recherche manuelle > Gbooks-
* Avantage de la recherche manuelle : quand la requête gbook ne retourne rien, possibilité d'essayer avec une autre partie du titre, ou en orthographiant différemment le titre (exemple roi => roy). Ces modifs permettent très souvent de tomber sur le document recherché.
* certains titres gbooks ont tous les "u" rempalcés par des "v" => quand un document est introuable, essayer d'utiliser des mots clés peut sensible à cette variation (une date présente dans le titre par ex)

**II. Observations sur le script de comparaison de titres**

* Adaptation du script pour fichiers en tsv (plus pratique à l'export)
* Il est sensible à la casse + variations ponctuation => prétraitement du texte en minuscule et, peut être, suppression des caractères spéciaux ?


**III. Modification des titres**

* Piste pour améliorer les sorties des deux api : faire des corrections car les erreurs proviennent de variations orthographiques.

modif_titres = {  
    "ami": "amy",
    "ch[aâ]teau": " chasteau",  
     "députés": "deputez",
    "[eé]chevin": "eschevin",
    "[eé]crite": "escrite",
    "[eé]p[iî]tre": "epistre",
    " Et ": " & ",
    "Etampes": "Estampes",
    "[eé]tat": "estat",
    "extrait": "extraict",
    "fait": "faict",
    "français": "françois",
    "h[oô]tel": "hostel"
    "jeudi": "jeudy",
    "jour": "iour",
    "Jules": "Iule",
    "lundi": "lundy",
    "mai": "may",
    "mardi": "mardy",
    "maréchal": "mareschal",
    "mercredi": "mercredy",
     "notre": "nostre",
    "particularités": "particularitez",
    "pr[ée]vôt": "prevost",
    "reine " : "reyne",
    "remontrance": "remonstrance",
    "remportés" : "remportez",
    "roi " : "roy",
    "samedi": "samedy",
    "sujet": "subiect",
    "Toulouse": "Tholouze",
    "troupes": "trouppes",
    "vendredi": "vendredy",
    }

