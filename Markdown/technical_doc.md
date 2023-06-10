# DOCUMENTATION 

Ce projet met à disposition un ensemble d'écrits d'actualité parus en grande majorité pendant la Fronde (1648-1653). Leur repérage a été rendu possible par le dépouillement des bibliographies de Célestin Moreau, Emile Socard, Ernest Labadie, Hubert Carrier et celle, en cours d'élaboration, de la [bibliothèque Mazarine](https://mazarinades.bibliotheque-mazarine.fr/). Le projet a d'abord consisté à récupérer numériquement ces documents, à en renseigner les métadonnées et à les lier entre eux et à des ressources ([base des imprimeurs](https://antonomaz.huma-num.fr/exist/apps/Antonomaz/imprimeurs.html?collection=imprimeurs), [notices](https://antonomaz.huma-num.fr/exist/apps/Antonomaz/notices.html?collection=notices) sur une notion ou un événement, etc.). Nous ajoutons également de nouvelles sources pouvant être qualifiées de "mazarinade" dans cette collection numérique. À moyen terme le but est d'une part d'encoder la structure des documents (éléments décoratifs, zones de texte, etc.) et d'autre part d'annoter linguistiquement leur formats texte (lemmatisation, identification des parties du discours).

## Livres numériques

Il s'agit d'exemplaires numériques moissonnés essentiellement sur *[Gallica](https://gallica.bnf.fr/)*, *[Mazarinum](https://mazarinum.bibliotheque-mazarine.fr/)* et *[GoogleBooks](https://books.google.fr/)*. 

Les images de Google Books ont fait l'objet d'un traitement particulier, dans le respect des mentions légales : en effet, il n'est pas rare, sur cette plateforme, que la dernière page du document numérisé soit dupliquée jusqu'à une dizaine de fois, ce qui alourdit le document et rend sa version océrisée très redondante. Ces pages répétées ont donc été supprimées pour que le fac simile numérique soit fidèle à l'objet imprimé.

## Textes obtenus automatiquement (OCR)

Chaque document peut être affiché et téléchargé en format texte. Ces textes sont issus d'un processus automatique (reconnaissance automatique de caractères/_optical characters recognition_ ou "OCR"), ce qui explique qu'ils contiennent des coquilles ou des erreurs manifestes. Cette automatisation de la transcritpion a toutefois été optimisée par l'utilsation d'un modèle de reconnaissance automatique entrainé sur des documents du XVIIe siècle (établi par Simon Gabay, avec l'outil Kraken). Nous ne réutilisons donc pas les océrisations de _Gallica_ ou de _Mazarinum_. La page de titre a été corrigée manuellement pour une partie des documents. Une recherche automatique (Ctrl +F) dans la page d'OCR permet de retrouver rapidement les occurrences qui auront été repérées par le moteur de recherche.

## Technologies utilisées

### Les images

Les images sont exposées grace au protocole [IIIF](https://iiif.io/) (International Image Interoperability Framework), via un visualiseur [Mirador](https://projectmirador.org/). Ce choix offre notamment une visualisation homogène de documents issus de bibliothèques numériques différentes, ainsi que tous les avantages de [IIIF](https://training.iiif.io/intro-to-iiif/) (comparaison de deux documents, recherche plein texte, etc.).

### Les textes 

L'édition des fichiers texte utilise le langage XML-TEI pour produire des données interopérables. L'encodage des métadonnées contenues dans l'en-tête de chaque fichier permet de décrire la matérialité du document, de donner des indications bibliographiques mais aussi de travailler finement l'établissements des métadonnées lui-même (voir infra). L'encodage du texte est actuellement minimal (paragraphes et lignes/vers, et permission d'imprimer et estampilles). Il est amené à évoluer grace à une HTRisation par eScriptorium.

Ces fichiers XML-TEI sont disponibles sur le [github du projet](https://github.com/Antonomaz/Corpus). La licence applicable pour la diffusion et la réutilisation du travail est une licence libre sans utilisation commerciale.

## Les métadonnées des textes

### Sources

Les métadonnées renseignées dans les fichiers XML-TEI sont d'origines diverses, elles s'appuient par défaut sur les bibliographies établies par E. Labadie, C. Moreau et E. Socard. D'autres sources nous ont permis de compléter et améliorer ces informations, en voici une liste non-exhaustive :
- **Bibliographie de la Bibliothèque Mazarine** : elles constituent de loin les métadonnées les plus complètes. Ces données s'appuient sur les écrits d'**Hubert Carrier**, dont le travail sur les datations nous a été particulièrement utile. Notons que les "Commentaires de la Bibliothèque Mazarine" peuvent ne pas correspondre à l'édition exposée sur Antonomaz; mais comme les notices de la BM précisent toujours les différences entre les différentes éditions, états ou émisions, il est en principe possible de savoir à quelle édition correspond l'exemplaire numérique exposé dans Antonomaz.
- **Catalogue de la Bibliothèque nationale de France** ;
- **Métadonnées fournies par la Bibliothèque municipale de Lyon** ;

Ces métadonnées sont ponctuellement complétées ou corrigées par nos soins lorsque ceci est possible.

### Établissement et hyperliaison des métadonnées

Un soin particulier a été apporté à la structuration et à l'établissement des métadonnées. Elles prennent en compte l'évolution des connaissances depuis la bibliographie de C. Moreau (vers 1850), qui a été amendée par H. Carrier et récemment la Base Bibliogrpahique de la Bibliothèque Mazarine. Les métadonnées intègrent ainsi les discussions de datation ou d'attribution entre les spécialistes à propos d'une production à 80 % anonyme. Elles sont hyperliées entre elles et avec les référentiels du web sémantique : [geonames](https://www.geonames.org/) pour les lieux, [isni](https://isni.org/) notamment, pour les personnes (auteurs et imprimeurs). Chaque imprimeur fait l'objet d'une fiche encodée en TEI, qui reprend les connaissances établies par le _Répertoire d'imprimeurs libraires, 1500-1810_ (BNF, 2004), dont le contenu scientifique a été converti numériquement dans les référentiels en usage, notamment [idref](https://www.idref.fr/). Une [base de données des imprimeurs](https://antonomaz.huma-num.fr/exist/apps/Antonomaz/imprimeurs.html?collection=imprimeurs) permet également de retrouver ces informations, indexées.
Des mots clés sont ajoutés peu à peu, en particulier les sujets, et les genres textuels (chansons, harangues, dialogues, etc.) afin de faciliter la consultation et l'interrogation du corpus.

## Sélection des items numériques et nommage

L'exemplaire numérique correspond à un exemplaire physique de bibliothèque. Pour autant nous avons choisi d'homogénéiser le nommage des documents en nous référant à la numérotation de Célestin Moreau. Le nom (.txt, .pdf, .xml) et l'URL du document  sont formés ainsi : [identifiants Moreau ou ses suppléments] + [bibliothèque numérique source du fac-simile numérique]. 
Ainsi, on peut retrouver les identifiants suivants : 
- Moreau3_MAZ : n° 3 de la Bibliographie Moreau, issus de _Mazarinum_ ;
- Moreau1suppl12_GALL : n° 12 du premier supplément de la Bibliographie Moreau, issu de _Gallica_ ;
- Labadie158_GBOOKS : n° 158 du supplément de Labadie, issu de _GoogleBooks_.

Il arrive que l'exemplaire numérique disponible en ligne ne corresponde pas exactement à celui décrit par Moreau (il peut s'agir d'une autre édition, ou d'un autre état de la même édition). Aussi le nommage repose-t-il sur une abstraction, qui serait "le" texte ("le" Moreau n°3, abstraction faite de toutes ses différentes manifestations matérielles).
Il peut en découler une inexactitude dans certains cas, puisque les différentes éditions peuvent comporter des changements plus ou moins importants. En pareil cas, il n'est pas rare que Moreau ait lui-même produit une nouvelle numérotation (dans ses "Suppléments"), auquel cas nous créons aussi un nouvel item quand le document est disponible en ligne. Quand le "supplément" Moreau consistait en un commentaire de sa part, sur un texte semblable, nous n'avons pas retenu l'item du Supplément Moreau.
Les réémissions (réédition avec changement d’endroits stratégiques comme la page de titre) sont considérées comme des entités à part.
Ce choix implique quelques approximations quant à la concordance de certains documents avec les notices de la Base Bibliographique des mazarinades de la Bibliothèque Mazarine (BM). Celle-ci repose en effet sur la description d'éditions (et de leurs variantes) et non d'entités "virtuelles" reposant sur un titre (comme nous le faisons en suivant Moreau). Comme signalé plus haut, l'utilisateur peut retrouver l'édition dont relève l'exemplaire numérique exposé dans Antonomaz en cherchant parmi les différentes notices et numéros BM liés aux divers états et rééditions d'un texte.

Ce choix de ne sélectionner qu'une édition permet d'éviter les redites dans les recherches par mot-clé dans la base textuelle (pour qui veut estimer le nombre d'écrits différents à utiliser le mot "Mazarin", par exemple). C'est ce point de vue, textuel et non documentaire, qui nous a poussés à exclure les états différents d'une même édition ou les rééditions avec le même titre, pour éviter les réitérations du même texte dans les recherches sur le site. 
