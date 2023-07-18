# STATISTIQUES

Vu le nombre important d'entités dans le corpus des mazarinades, il semble utile de proposer quelques exploitations statistiques.
Nous le faisons à partir de deux jeux de données combinés : les métadonnées issues de la tradition bibliographique (les plus complètes), et celles issues du corpus Antonomaz, moins complètes (2/3 de cet ensemble), mais plus précises sur certains points (présence ou non d'un nom d'auteur et d'un nom d'imprimeur libraire).

[Bibliographies](https://antonomaz.huma-num.fr/tools/Biblio_Moreau.html) [Projet Antonomaz](https://github.com/Antonomaz)

## Calculs à partir des bibliographies anciennes (environ 5060 mazarinades recensées)

En exploitant les données issues des bibliographies du XIXe siècle, à savoir celles de C. Moreau, E. Labadie et E. Socard, il est possible de proposer quelques premières statistiques.

*N.B. : les données exploitées sont consultables à [cette adresse](https://antonomaz.huma-num.fr/tools/Biblio_Moreau.html). Elles comportent 5 055 entrées et ont été préalablement nettoyées, des erreurs peuvent cependant encore s'y trouver (notamment des doublons en raison des suppléments publiés par C. Moreau).*


###  Dates de publication

- 88 % des documents (4460 imprimés) indiquent une date de publication.
- 12 % environ (602 imprimés) n'en indiquent pas.
        - 63 % environ des mazarinades (3198 imprimés) ont été publiées pendant les deux années les plus productives : 1649 et 1652.


<table class='table table-striped'>
<tr><th scope='col'></th><th scope='col'>1648</th><th scope='col'>1649</th><th scope='col'>1650</th><th scope='col'>1651</th><th scope='col'>1652</th><th scope='col'>1653</th><th scope='col'>1654</th><th scope='col'>Après 1654</th><th scope='col'>Sans Date</th></tr>
<tr><th scope='col'>5062 mazarinades (100.0%)</th><th scope='col'>70 (1.38%)</th><th scope='col'>1817 (35.89%)</th><th scope='col'>493 (9.74%)</th><th scope='col'>598 (11.81%)</th><th scope='col'>1381 (27.28%)</th><th scope='col'>42 (0.83%)</th><th scope='col'>25 (0.49%)</th><th scope='col'>29 (0.57%)</th><th scope='col'>602 (11.89%)</th></tr>
</table>

*Ces données ont été calculées après avoir retiré les entrées sans date de publication.*

### Lieux de publication (villes)

- 65,2 % des documents (3 294 imprimés) indiquent la ville de publication.
- 34,8 %  (1 761 imprimés) ne l'indiquent pas.
        - 91 % des mazariandes sont imprimées à Paris.


<table class="table table-striped">
<thead>
  <tr>
    <th scope="col">Lieux de publication</th>
    <th scope="col">Bordeaux</th>
    <th scope="col">Paris</th>
    <th scope="col">Pontoise</th>
    <th scope="col">Rouen</th>
    <th scope="col">Saint-Germain-en-Laye</th>
    <th scope="col">Total</th>
  </tr>
</thead>
<tbody>
  <tr>
    <th scope="row">Nombre de mazarinades</th>
    <td>97</td>
    <td>3 010</td>
    <td>34</td>
    <td>33</td>
    <td>32</td>
    <td>3 196</td>
  </tr>
  <tr>
    <th scope="row">Pourcentage</th>
    <td>3 %</td>
    <td>91.3 %</td>
    <td>1 %</td>
    <td>1 %</td>
    <td>1 %</td>
    <td>97.3 %</td>
  </tr>
</tbody>
</table>

*Seuls les lieux de publication indiqués au moins dix fois ont été retenus. Ces données ont été calculées après avoir retiré les entrées sans lieu de publication.*

### Nombre de pages

Les données suivantes ont été calculées à partir des 4 664 entrées des bibliographies Moreau (et suppléments) qui indiquent un nombre de pages.
**Il apparait que presque la moitié des mazarinades comportent 7-8 pages (2 cahiers), et 11 % comportent 4 pages (1 cahier).**

<table class="table table-striped">
<thead>
  <tr>
    <th scope="col">Nombre de pages</th>
    <th scope="col">4</th>
    <th scope="col">6</th>
    <th scope="col">7</th>
    <th scope="col">8</th>
    <th scope="col">11</th>
    <th scope="col">12</th>
    <th scope="col">14</th>
    <th scope="col">15</th>
    <th scope="col">16</th>
    <th scope="col">Total</th>
  </tr>
</thead>
<tbody>
  <tr>
    <th scope="row">Nombre de mazarinades</th>
    <td>517</td>
    <td>273</td>
    <td>914</td>
    <td>1 371</td>
    <td>132</td>
    <td>195</td>
    <td>93</td>
    <td>167</td>
    <td>178</td>
    <td>3840</td>
  </tr>
  <tr>
    <th scope="row">Pourcentage</th>
    <td>11 %</td>
    <td>6 %</td>
    <td>20 %</td>
    <td>29 %</td>
    <td>3 %</td>
    <td>4 %</td>
    <td>2 %</td>
    <td>3.5 %</td>
    <td>4 %</td>
    <td>82.5 %</td>
  </tr>
</tbody>
</table>

<br/>
<hr/>

## Calcul à partir de l'échantillon Antonomaz (3065 mazarinades, 2/3 des mazarinades connues)

Les statistiques ici proposées ne concernent pas la totalité du corpus, comme c'est le cas dans la partie précédente, mais uniquement les mazarinades qui composent le corpus du projet Antonomaz, c'est-à-dire celles trouvées dans les bibliothèques numériques accessibles, soit un peu plus de 3 000 documents.

### Taux d'anonymat

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

Sur Antonomaz, environ 57  % d’écrits (1747 imprimés) sont sans nom d'auteurs, 2  % affichent un pseudonyme au sens large : initiales et pseudonymes (70 imprimés).

Dès que nous avons pu identifier l'auteur (même si ce n'est pas explicite sur le document), l'imprimé n'est pas compté comme anonyme.

<table style="width:100%;" border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th></th>
      <th>Nombre d'auteurs</th>
      <th>Pourcentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Auteur nommé</th>
      <td>1248</td>
      <td>40.717781</td>
    </tr>
    <tr>
      <th>Auteur anonyme</th>
      <td>1747</td>
      <td>56.998369</td>
    </tr>
    <tr>
      <th>Pseudonyme</th>
      <td>70</td>
      <td>2.283850</td>
    </tr>
  </tbody>
</table>

__Statistiques proposées par H. Carrier (échantillon de 1000 écrits, 1/5 du corpus global)__

A titre de comparaison, on peut observer les statistiques qu'H. Carrier avait proposées, établies sur un ensemble "d'un millier de mazarinades prises au hasard", où "les différents genres et années de publication se trouvent équitablement répartis" par H. Carrier (_La Presse de la Fronde (1648-1653): Les mazarinades. Les hommes du livre_, Genève, Droz, 1991, t. 2, p. 150.).

__Il estime l’anonymat à 83% des pièces, à quoi il ajoute 7% de cryptonymes.__

__Seules 10% de cet échantillon de mazarinades affichent donc un nom d'auteur, et 90 % effacent leur origine énonciative.__

Il exclut les pièces officielles types actes royaux, mais aussi "lettres authentiques, manifestes et déclarations des principaux personnages de l’État", problablement parce qu'il estime qu'elles sont évidemment attribuées et que la question de l'auteur n'a pas d'intérêt (_ibid._, p. 77). 

Son chiffre rend donc compte de l'anonymat affiché (il compte comme anonymes même les pièces dont l'auteur nous est connu par le contexte, et pouvait l'être, parfois évidemment, par les contemporains). Le chiffre ne reflète donc pas le savoir actuel sur les auteurs de mazarinades, mais est un très bon indicateur de l'effet d'anonymat massif produit par ces imprimés.

### Taux d'anonymat typographique (noms d'imprimeur-libraire indiqués ou non)

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

55 % de mazarinades inscrivent une adresse typographique complète (environ la même proportion que celle indiquée par Carrier _infra_). Pour les 45 % imprimés restants, on peut penser que c'est par prudence que ni le nom ni l'adresse des imprimeurs-libraires ne sont affichés ; cela représentait un risque commercial puisque l'acheteur ne pouvait pas identifier le lieu où se procurer le libelle.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>info status</th>
      <th>count</th>
      <th>percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>unnamed_publisher</td>
      <td>1390</td>
      <td>45.350734</td>
    </tr>
    <tr>
      <td>pseudonym</td>
      <td>4</td>
      <td>0.130506</td>
    </tr>
    <tr>
      <td>named_publisher+known_pub_date+known_pub_place</td>
      <td>1671</td>
      <td>54.518760</td>
    </tr>
  </tbody>
</table>

__Statistiques proposées par H. Carrier (échantillon de 1000 écrits, 1/5 du corpus global)__

Sur son échantillon de 1000 mazarinades calibrées en fonction des genres et des années, H. Carrier calcule que 16 % des mazarinades ne donnent aucune information éditoriale, 31 % affichent le lieu et la date de publication. Enfin, il note que  53 % de ces imprimés ont une adresse typographique complète (lieu, date, nom d'imprimeur), sensiblement la même proportion que pour Antonomaz.

__Globlament donc on peut affirmer qu'une mazarinade sur deux affiche son origine typographique.__

Il note également que ces chiffres varient au cours de la Fronde : si 64% des mazarinades de l'échantillon étudié présentent une adresse typographique complète en 1649, ils ne sont plus que 38% en 1652.

### Imprimatur

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>file_count</th>
      <th>imprimatur-ed_file_count</th>
      <th>imprimatur-ed_file_percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>3065</td>
      <td>755</td>
      <td>24.632953</td>
    </tr>
  </tbody>
</table>

### Imprimatur per year

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>year</th>
      <th>count</th>
      <th>percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Sans date</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>1649</td>
      <td>476</td>
      <td>15.530179</td>
    </tr>
    <tr>
      <td>1652</td>
      <td>164</td>
      <td>5.350734</td>
    </tr>
    <tr>
      <td>1651</td>
      <td>54</td>
      <td>1.761827</td>
    </tr>
    <tr>
      <td>1650</td>
      <td>37</td>
      <td>1.207178</td>
    </tr>
    <tr>
      <td>1655</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>1648</td>
      <td>18</td>
      <td>0.587276</td>
    </tr>
    <tr>
      <td>1653</td>
      <td>4</td>
      <td>0.130506</td>
    </tr>
  </tbody>
</table>

### Nombre de pages

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>nb_page</th>
      <th>count</th>
      <th>percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>8</td>
      <td>918</td>
      <td>29.951060</td>
    </tr>
    <tr>
      <td>7</td>
      <td>584</td>
      <td>19.053834</td>
    </tr>
    <tr>
      <td>6</td>
      <td>169</td>
      <td>5.513866</td>
    </tr>
    <tr>
      <td>16</td>
      <td>141</td>
      <td>4.600326</td>
    </tr>
    <tr>
      <td>4</td>
      <td>268</td>
      <td>8.743883</td>
    </tr>
    <tr>
      <td>32</td>
      <td>44</td>
      <td>1.435563</td>
    </tr>
    <tr>
      <td>11</td>
      <td>95</td>
      <td>3.099511</td>
    </tr>
    <tr>
      <td>10</td>
      <td>29</td>
      <td>0.946166</td>
    </tr>
    <tr>
      <td>12</td>
      <td>127</td>
      <td>4.143556</td>
    </tr>
    <tr>
      <td>2</td>
      <td>7</td>
      <td>0.228385</td>
    </tr>
    <tr>
      <td>15</td>
      <td>123</td>
      <td>4.013051</td>
    </tr>
    <tr>
      <td>14</td>
      <td>67</td>
      <td>2.185971</td>
    </tr>
    <tr>
      <td>20</td>
      <td>44</td>
      <td>1.435563</td>
    </tr>
    <tr>
      <td>23</td>
      <td>30</td>
      <td>0.978793</td>
    </tr>
    <tr>
      <td>25</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>84</td>
      <td>5</td>
      <td>0.163132</td>
    </tr>
    <tr>
      <td>30</td>
      <td>17</td>
      <td>0.554649</td>
    </tr>
    <tr>
      <td>18</td>
      <td>18</td>
      <td>0.587276</td>
    </tr>
    <tr>
      <td>133</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>31</td>
      <td>25</td>
      <td>0.815661</td>
    </tr>
    <tr>
      <td>64</td>
      <td>3</td>
      <td>0.097879</td>
    </tr>
    <tr>
      <td>75</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>27</td>
      <td>9</td>
      <td>0.293638</td>
    </tr>
    <tr>
      <td>22</td>
      <td>21</td>
      <td>0.685155</td>
    </tr>
    <tr>
      <td>40</td>
      <td>12</td>
      <td>0.391517</td>
    </tr>
    <tr>
      <td>44</td>
      <td>6</td>
      <td>0.195759</td>
    </tr>
    <tr>
      <td>80</td>
      <td>4</td>
      <td>0.130506</td>
    </tr>
    <tr>
      <td>19</td>
      <td>28</td>
      <td>0.913540</td>
    </tr>
    <tr>
      <td>24</td>
      <td>50</td>
      <td>1.631321</td>
    </tr>
    <tr>
      <td>274</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>38</td>
      <td>8</td>
      <td>0.261011</td>
    </tr>
    <tr>
      <td>28</td>
      <td>14</td>
      <td>0.456770</td>
    </tr>
    <tr>
      <td>3</td>
      <td>43</td>
      <td>1.402936</td>
    </tr>
    <tr>
      <td>39</td>
      <td>8</td>
      <td>0.261011</td>
    </tr>
    <tr>
      <td>270</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>108</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>116</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>36</td>
      <td>13</td>
      <td>0.424144</td>
    </tr>
    <tr>
      <td>87</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>43</td>
      <td>3</td>
      <td>0.097879</td>
    </tr>
    <tr>
      <td>48</td>
      <td>4</td>
      <td>0.130506</td>
    </tr>
    <tr>
      <td>35</td>
      <td>6</td>
      <td>0.195759</td>
    </tr>
    <tr>
      <td>1</td>
      <td>23</td>
      <td>0.750408</td>
    </tr>
    <tr>
      <td>13</td>
      <td>8</td>
      <td>0.261011</td>
    </tr>
    <tr>
      <td>29</td>
      <td>3</td>
      <td>0.097879</td>
    </tr>
    <tr>
      <td>26</td>
      <td>12</td>
      <td>0.391517</td>
    </tr>
    <tr>
      <td>37</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>46</td>
      <td>5</td>
      <td>0.163132</td>
    </tr>
    <tr>
      <td>119</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>34</td>
      <td>4</td>
      <td>0.130506</td>
    </tr>
    <tr>
      <td>240</td>
      <td>2</td>
      <td>0.065253</td>
    </tr>
    <tr>
      <td>192</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>63</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>59</td>
      <td>2</td>
      <td>0.065253</td>
    </tr>
    <tr>
      <td>94</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>72</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>45</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>42</td>
      <td>3</td>
      <td>0.097879</td>
    </tr>
    <tr>
      <td>248</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>9</td>
      <td>3</td>
      <td>0.097879</td>
    </tr>
    <tr>
      <td>17</td>
      <td>3</td>
      <td>0.097879</td>
    </tr>
    <tr>
      <td>166</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>74</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>47</td>
      <td>3</td>
      <td>0.097879</td>
    </tr>
    <tr>
      <td>152</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>118</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>95</td>
      <td>2</td>
      <td>0.065253</td>
    </tr>
    <tr>
      <td>56</td>
      <td>2</td>
      <td>0.065253</td>
    </tr>
    <tr>
      <td>5</td>
      <td>5</td>
      <td>0.163132</td>
    </tr>
    <tr>
      <td>456</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>235</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>54</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>50</td>
      <td>2</td>
      <td>0.065253</td>
    </tr>
    <tr>
      <td>218</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>68</td>
      <td>2</td>
      <td>0.065253</td>
    </tr>
    <tr>
      <td>150</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>311</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>52</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>263</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>114</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>41</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>79</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>718</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>199</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>107</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>57</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>331</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>428</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>325</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
  </tbody>
</table>

### Date de publication

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>year</th>
      <th>count</th>
      <th>percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Sans Date</td>
      <td>38</td>
      <td>1.239804</td>
    </tr>
    <tr>
      <td>1649</td>
      <td>1414</td>
      <td>46.133768</td>
    </tr>
    <tr>
      <td>1652</td>
      <td>938</td>
      <td>30.603589</td>
    </tr>
    <tr>
      <td>1651</td>
      <td>332</td>
      <td>10.831974</td>
    </tr>
    <tr>
      <td>1650</td>
      <td>276</td>
      <td>9.004894</td>
    </tr>
    <tr>
      <td>1654</td>
      <td>12</td>
      <td>0.391517</td>
    </tr>
    <tr>
      <td>1662</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>1655</td>
      <td>2</td>
      <td>0.065253</td>
    </tr>
    <tr>
      <td>1648</td>
      <td>41</td>
      <td>1.337684</td>
    </tr>
    <tr>
      <td>1634</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>1653</td>
      <td>8</td>
      <td>0.261011</td>
    </tr>
    <tr>
      <td>1663</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
    <tr>
      <td>1656</td>
      <td>1</td>
      <td>0.032626</td>
    </tr>
  </tbody>
</table>

### Lieu de publication

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>place</th>
      <th>count</th>
      <th>percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Sans Lieu</td>
      <td>713</td>
      <td>23.262643</td>
    </tr>
    <tr>
      <td>Saint-Germain-en-Laye</td>
      <td>16</td>
      <td>0.522023</td>
    </tr>
    <tr>
      <td>Paris</td>
      <td>2201</td>
      <td>71.810767</td>
    </tr>
    <tr>
      <td>Pontoise</td>
      <td>20</td>
      <td>0.652529</td>
    </tr>
    <tr>
      <td>Orléans</td>
      <td>27</td>
      <td>0.880914</td>
    </tr>
    <tr>
      <td>Bordeaux</td>
      <td>35</td>
      <td>1.141925</td>
    </tr>
    <tr>
      <td>Rouen</td>
      <td>24</td>
      <td>0.783034</td>
    </tr>
  </tbody>
</table>

### Nom d'imprimeur

__Statistiques sur l'échantillon Antonomaz (2/3 du corpus global)__

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>publisher status</th>
      <th>count</th>
      <th>percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>named_publisher</td>
      <td>1693</td>
      <td>55.236542</td>
    </tr>
    <tr>
      <td>unnamed_publisher</td>
      <td>1368</td>
      <td>44.632953</td>
    </tr>
    <tr>
      <td>pseudonym</td>
      <td>4</td>
      <td>0.130506</td>
    </tr>
  </tbody>
</table>

