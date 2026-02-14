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

| Attribut                 | Signification                          |
|:-------------------------|:---------------------------------------|
| `epi_id`                 | Identifiant entier unique              |
| `epi_kind_id`            | Corde, Harnais, etc, voir table `Kind` |
| `epi_type`               | Spécificité (corde à double, usage)    |
| `epi_brand`              | Fabricant                              |
| `epi_product_name`       | Modèle et/ou numéro de série           |
| `epi_amount`             | Nombre de pièces en cas de lot         |
| `epi_marking`            | Signe distinctif/Marquage              |
| `epi_storage_id`         | Lieu de stockage, voir table `Storage` |
| `epi_manufacturing_date` | Date de fabrication                    |
| `epi_first_use_date`     | Date de première utilisation           |
| `epi_life_time`          | Durée de vie en années                 |


### Table `Kind`
Contient les différents genres d'EPI. les attributs sont:

| Attribut | Signification                          |
|:---------|:---------------------------------------|
| kin_id   | Identifiant entier unique              |
| kin_name | Nom du type ("Corde", "Harnais", etc) |


### Table `Storage`
Contient les différents endroits où peut être stocké le matériel:

| Attribut | Signification                                              |
|:---------|:-----------------------------------------------------------|
| sto_id   | Identifiant entier unique                                  |
| sto_name | Nom du stockage ("Local Félix", "Caisse maintenance", etc) |

### Table `Control`
Liste des contrôles effectués sur le matériel:

| Attribut   | Signification                 |
|:-----------|:------------------------------|
| con_id     | Identifiant entier unique     |
| con_epi_id | Identifiant de l'EPI concerné |
| con_date   | Date du contrôle              |

### Table `Waste`
Liste du matériel mis au rebut:

| Attribut   | Signification                          |
|:-----------|:---------------------------------------|
| was_epi_id | Identifiant de l'EPI concerné (unique) |
| was_date   | Date de la mise au rebut               |

## Client

<!--  LocalWords:  BEAL EPI
 -->
