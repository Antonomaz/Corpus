# Corpus - Antonomaz

<table id="myTable">
<tr><td></td><td>Total</td><td>1648</td><td>1649</td><td>1650</td><td>1651</td><td>1652</td><td>1653</td><td>1654</td><td>Après 1654</td><td>Sans Date</td></tr>
<tr><td>Référencées</td><td>5062 (100.0%)</td><td>70 (1.38%)</td><td>1817 (35.89%)</td><td>493 (9.74%)</td><td>598 (11.81%)</td><td>1381 (27.28%)</td><td>42 (0.83%)</td><td>25 (0.49%)</td><td>29 (0.57%)</td><td>602 (11.89%)</td></tr>
<tr><td>Antonomaz</td><td>3248 (64.16%)</td><td>34 (0.67%)</td><td>1442 (28.49%)</td><td>275 (5.43%)</td><td>311 (6.14%)</td><td>948 (18.73%)</td><td>8 (0.16%)</td><td>12 (0.24%)</td><td>4 (0.08%)</td><td>212 (4.19%)</td></tr>
</table>
Ce répertoire contient un corpus de mazarinades encodées en XML-TEI.

## Les données

Le corpus est consultable depuis le dossier [Mazarinades](https://github.com/Antonomaz/Corpus/tree/main/Mazarinades).


Les textes sont ajoutés au fur et à mesure de leur encodage.

### Organisation des fichiers

Les mazarinades sont classées selon l'identifiant qui leur a été attribué par Moreau ([à retrouver ici](http://antonomaz.huma-num.fr/tools/Biblio_Moreau.html)). Elles sont classées par centaines (de 1-101 à 4001-4101).

Ces dossiers sont complétées par les `Suppléments` identifiés par Moreau et les mazarinades identifiées par `Socard` et `Labadie`.

Le dossier `Bibliothèque_Mazarine` contient les documents qui n'ont pas été repérés par Moreau, Socard ou Labadie.

Si plusieurs exemplaires correspondant à un seul et même numéro Moreau ont été trouvés, ils sont placés dans le dossier `Doublons`, ils n'ont à priori pas été relus.

Enfin, les dossiers `to_do` et `temp_MAZ` correspondent à des dossiers de travail et contiennent des fichiers qui doivent être relus avant d'être ajoutés aux dossiers déjà évoqués.




## Validation

La bonne qualité et la cohérence de l'encodage des textes sont assurées par l'[ODD du projet](https://github.com/Antonomaz/ODD). Le schéma de validation ainsi que de la documentation y sont accessibles.

## Aperçu des données encodées

Il est possible d'avoir un aperçu des mazarinades et de leurs métadonnées en consultant [corpus.csv](https://github.com/Antonomaz/Corpus/tree/main/output/corpus.csv) produit automatiquement à partir de [ce script](https://github.com/Antonomaz/Corpus/tree/main/script/tei_to_csv.py).

## Licence

Les textes sont publiés sous la licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
