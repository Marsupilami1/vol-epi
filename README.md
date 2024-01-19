# Suivi du matériel d'escalade

## Description
Ce projet a pour but de fournir une interface simple pour le suivi du matériel de VOL [https://www.vertical-ouest-loisirs.fr/](https://www.vertical-ouest-loisirs.fr/).

Pour tester le projet localement:

``` sh
$ python -m venv vol
$ source vol/bin/activate
$ pip install -r requirements.txt
$ python main.py create-database
$ python main.py
```

## Base de données
Les schémas des relations sont décrits dans `models.py`.
### Table `EPI`
La table `EPI` contient l'ensemble du matériel du club, mis au rebut ou non.
Les attributs sont les suivants :

| Attribut               | Signification                            |
|:-----------------------|:-----------------------------------------|
| `epi_id`               | Identifiant entier unique                |
| `epi_genre_id`         | Corde, Harnais, etc, voir table `Genres` |
| `epi_type`             | Spécificité (corde à double, usage)      |
| `epi_marque`           | Fabricant                                |
| `epi_modele`           | Modèle et/ou numéro de série             |
| `epi_quantite`         | Nombre de pièces en cas de lot           |
| `epi_marquage`         | Signe distinctif                         |
| `epi_stockage_id`      | Lieu de stockage, voir table `Stockage`  |
| `epi_date_fabrication` | Date de fabrication                      |
| `epi_date_utilisation` | Date de première utilisation             |
| `epi_duree_vie`        | Durée de vie en années                   |


### Table `Genre`
Contient les différents genres d'EPI. les attributs sont:

| Attribut | Signification                          |
|:---------|:---------------------------------------|
| gen_id   | Identifiant entier unique              |
| gen_name | Nom du genre ("Corde", "Harnais", etc) |


### Table `Stockage`
Contient les différents endroits où peut être stocké le matériel:

| Attribut | Signification                                           |
|:---------|:--------------------------------------------------------|
| sto_id   | Identifiant entier unique                               |
| sto_name | Nom du genre ("Local Félix", "Caisse maintenance", etc) |

### Table `Controle`
Liste des contrôles effectués sur le matériel:

| Attribut   | Signification                 |
|:-----------|:------------------------------|
| con_id     | Identifiant entier unique     |
| con_epi_id | Identifiant de l'EPI concerné |
| con_date   | Date du contrôle              |

### Table `Rebut`
Liste du matériel mis au rebut:

| Attribut   | Signification                          |
|:-----------|:---------------------------------------|
| reb_epi_id | Identifiant de l'EPI concerné (unique) |
| reb_date   | Date de la mise au rebut               |

## Client

<!--  LocalWords:  BEAL EPI
 -->
