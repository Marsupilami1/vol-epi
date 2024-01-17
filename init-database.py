import sqlite3

import os
from datetime import date

import models

database_path = os.path.abspath("./vol-maintenance.db")

if os.path.exists(database_path):
    print(
        f"Le fichier {database_path} existe déjà, voulez-vous le supprimer [o/N]: ",
        end="",
    )
    c = input()
    if c == "o" or c == "O":
        os.rename(database_path, database_path + ".old")
    else:
        exit(0)

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute(
    """
CREATE TABLE Cordes (
  c_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  c_modele VARCHAR(30),
  c_fabricant VARCHAR(30),
  c_serie VARCHAR(30),
  c_longueur INTEGER,
  c_couleur VARCHAR(30),
  c_type VARCHAR(30),
  c_description VARCHAR(50),
  c_dfabrication DATE,
  c_dachat DATE,
  c_dfvie DATE,
  c_dutilisation DATE
) """
)

cursor.execute(
    """
CREATE TABLE ControlesCordes (
  cc_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  c_id INTEGER REFERENCES Cordes,
  cc_date DATE,
  cc_remarques TEXT,
  cc_usure VARCHAR(20),
  cc_brulures VARCHAR(20),
  cc_coupures VARCHAR(20),
  cc_peluche VARCHAR(20),
  cc_ame VARCHAR(20)
) """
)

connection.commit()
connection.close()
