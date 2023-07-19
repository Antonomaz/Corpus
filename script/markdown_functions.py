import pandas as pd
import glob
from math import ceil
from markdownipy import markdownipy
from pathlib import Path

data_dir:str = "../output/stats/*.csv"
bibliographies_link:str="https://antonomaz.huma-num.fr/tools/Biblio_Moreau.html"
antonomaz_corpus_link:str="https://github.com/Antonomaz"
bibliography_stats:str = "../Markdown/script_fuel/bibliography_stats.md"

def update_markdown_stats(data_dir:str, markdown_filepath:str="", title:str="STATISTIQUES", bibliographies_link:str=bibliographies_link, antonomaz_corpus_link:str=antonomaz_corpus_link, bibliography_stats:str = bibliography_stats):
    #load the stats data (key name: base file name without extension)
    stat_dict:dict = {Path(csv_file).parts[-1][:-4]: pd.read_csv(filepath_or_buffer=csv_file) for csv_file in glob.glob(data_dir)}
    #write markdown file
    md = markdownipy.markdownipy()
    md < title|md.h1
    md < "Vu le nombre important d'entités dans le corpus des mazarinades, il semble utile de proposer quelques exploitations statistiques.\nNous le faisons à partir de deux jeux de données combinés : les métadonnées issues de la tradition bibliographique (les plus complètes), et celles issues du corpus Antonomaz, moins complètes (2/3 de cet ensemble), mais plus précises sur certains points (présence ou non d'un nom d'auteur et d'un nom d'imprimeur libraire)."
    md < f"{bibliographies_link|md.link('Bibliographies')} {antonomaz_corpus_link|md.link('Projet Antonomaz')}"
    md < open(bibliography_stats).read()
    md < "Calcul à partir de l'échantillon Antonomaz (3065 mazarinades, 2/3 des mazarinades connues)"|md.h2
    md < "Les statistiques ici proposées ne concernent pas la totalité du corpus, comme c'est le cas dans la partie précédente, mais uniquement les mazarinades qui composent le corpus du projet Antonomaz, c'est-à-dire celles trouvées dans les bibliothèques numériques accessibles, soit un peu plus de 3 000 documents."
    md < "Taux d'anonymat"|md.h3
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    md < f"Sur Antonomaz, environ {ceil(stat_dict['author_stats'].at[1, 'percentage'])}  % d’écrits ({stat_dict['author_stats'].at[1, 'count']} imprimés) sont sans nom d'auteurs, {int(stat_dict['author_stats'].at[2, 'percentage'])}  % affichent un pseudonyme au sens large : initiales et pseudonymes ({stat_dict['author_stats'].at[2, 'count']} imprimés)."
    md < "Dès que nous avons pu identifier l'auteur (même si ce n'est pas explicite sur le document), l'imprimé n'est pas compté comme anonyme."
    # changing column and row labels
    author_stats_df = stat_dict["author_stats"]
    author_stats_df.columns = ["authorship_status", "Nombre de mazarinades", "Pourcentage"]
    author_stats_df.set_index("authorship_status", inplace=True)
    author_stats_df.index = ["Auteur nommé", "Auteur anonyme", "Pseudonyme"]
    print(author_stats_df)
    md < author_stats_df.to_html(header=True, index=True, justify="center", index_names=True)
    md < "Statistiques proposées par H. Carrier (échantillon de 1000 écrits, 1/5 du corpus global)"|md.bold
    md < f"A titre de comparaison, on peut observer les statistiques qu'H. Carrier avait proposées, établies sur un ensemble \"d'un millier de mazarinades prises au hasard\", où \"les différents genres et années de publication se trouvent équitablement répartis\" par H. Carrier (_La Presse de la Fronde (1648-1653): Les mazarinades. Les hommes du livre_, Genève, Droz, 1991, t. 2, p. 150.)."
    md < "Il estime l’anonymat à 83% des pièces, à quoi il ajoute 7% de cryptonymes."|md.bold
    md < "Seules 10% de cet échantillon de mazarinades affichent donc un nom d'auteur, et 90 % effacent leur origine énonciative."|md.bold
    md < "Il exclut les pièces officielles types actes royaux, mais aussi \"lettres authentiques, manifestes et déclarations des principaux personnages de l’État\", problablement parce qu'il estime qu'elles sont évidemment attribuées et que la question de l'auteur n'a pas d'intérêt (_ibid._, p. 77). "
    md < "Son chiffre rend donc compte de l'anonymat affiché (il compte comme anonymes même les pièces dont l'auteur nous est connu par le contexte, et pouvait l'être, parfois évidemment, par les contemporains). Le chiffre ne reflète donc pas le savoir actuel sur les auteurs de mazarinades, mais est un très bon indicateur de l'effet d'anonymat massif produit par ces imprimés."
    md < "Taux d'anonymat typographique (noms d'imprimeur-libraire indiqués ou non)"|md.h3
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    md < f"{ceil(stat_dict['all_info_publisher_stats'].at[2, 'percentage']) } % de mazarinades inscrivent une adresse typographique complète (environ la même proportion que celle indiquée par Carrier _infra_). Pour les {int(stat_dict['all_info_publisher_stats'].at[0, 'percentage']) } % imprimés restants, on peut penser que c'est par prudence que ni le nom ni l'adresse des imprimeurs-libraires ne sont affichés ; cela représentait un risque commercial puisque l'acheteur ne pouvait pas identifier le lieu où se procurer le libelle."
    # renaming column labels
    all_info_publisher_stats_df = stat_dict["all_info_publisher_stats"]
    all_info_publisher_stats_df.columns = ["info_status", "Nombre de mazarinades", "Pourcentage"]
    all_info_publisher_stats_df.set_index("info_status", inplace=True)
    all_info_publisher_stats_df.index = ["Imprimeur anonyme", "Pseudonyme", "Adresse typographique complète"]
    print(all_info_publisher_stats_df)
    md < all_info_publisher_stats_df.to_html(header=True, index=True).replace('<th>', '<th scope="col">')
    md < "Statistiques proposées par H. Carrier (échantillon de 1000 écrits, 1/5 du corpus global)"|md.bold
    md < "Sur son échantillon de 1000 mazarinades calibrées en fonction des genres et des années, H. Carrier calcule que 16 % des mazarinades ne donnent aucune information éditoriale, 31 % affichent le lieu et la date de publication. Enfin, il note que  53 % de ces imprimés ont une adresse typographique complète (lieu, date, nom d'imprimeur), sensiblement la même proportion que pour Antonomaz."
    md < "Globlament donc on peut affirmer qu'une mazarinade sur deux affiche son origine typographique."|md.bold
    md < "Il note également que ces chiffres varient au cours de la Fronde : si 64% des mazarinades de l'échantillon étudié présentent une adresse typographique complète en 1649, ils ne sont plus que 38% en 1652."
    md < "Imprimatur"|md.h3
    # renaming column labels
    imprimatur_stat_df = stat_dict["imprimatur_stat"]
    imprimatur_stat_df.columns = ["Nombre total de mazarinades", "Nombre avec imprimatur", "Pourcentage avec imprimatur"]
    print(imprimatur_stat_df)
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    md < imprimatur_stat_df.to_html(header=True, index=False)
    md < "Imprimatur par an"|md.h3
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    # renaming column labels
    imprimatur_per_year_stats_df = stat_dict["imprimatur_per_year_stats"]
    imprimatur_per_year_stats_df.columns = ["Année", "Nombre avec imprimatur", "Pourcentage avec imprimatur"]
    imprimatur_per_year_stats_df.sort_values(by=["Année"], inplace=True)
    print(imprimatur_per_year_stats_df)
    md < imprimatur_per_year_stats_df.to_html(header=True, index=False)
    md < "Nombre de pages"|md.h3
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    # renaming column labels
    nb_page_stat_df = stat_dict["nb_page_stat"]
    nb_page_stat_df.columns = ["Nombre de pages", "Nombre de mazarinades", "Pourcentage"]
    nb_page_stat_df.sort_values(by=["Nombre de pages"], inplace=True)
    print(nb_page_stat_df)
    md < stat_dict["nb_page_stat"].to_html(header=True, index=False)
    md < "Date de publication"|md.h3
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    # renaming column labels
    pub_date_stat_df = stat_dict["pub_date_stat"]
    pub_date_stat_df.columns = ["Année", "Nombre de mazarinades", "Pourcentage"]
    pub_date_stat_df.sort_values(by=["Année"], inplace=True)
    print(pub_date_stat_df)
    md < pub_date_stat_df.to_html(header=True, index=False)
    md < "Lieu de publication"|md.h3
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    # renaming column labels
    pub_place_stat_df = stat_dict["pub_place_stat"]
    pub_place_stat_df.columns = ["Lieu", "Nombre de mazarinades", "Pourcentage"]
    pub_place_stat_df.sort_values(by=["Pourcentage"], inplace=True, ascending=False)
    print(pub_place_stat_df)
    md < pub_place_stat_df.to_html(header=True, index=False)
    md < "Nom d'imprimeur"|md.h3
    md < "Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)"|md.bold
    # changing column and row labels
    publisher_stats_df = stat_dict["publisher_stats"]
    publisher_stats_df.columns = ["publisher_status", "Nombre de mazarinades", "Pourcentage"]
    publisher_stats_df.set_index("publisher_status", inplace=True)
    publisher_stats_df.index = ["Imprimeur nommé", "Imprimeur anonyme", "Pseudonyme"]
    print(publisher_stats_df)
    md < publisher_stats_df.to_html(header=True, index=True)

    
    #print(stat_dict["all_info_publisher_stats"].at[2, "percentage"])
    #print(stat_dict)
    md > markdown_filepath
    return stat_dict

update_markdown_stats(data_dir=data_dir, markdown_filepath="../Markdown/statistiques.md")