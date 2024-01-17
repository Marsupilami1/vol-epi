#!/usr/bin/env python3

import sqlite3
import os
from datetime import date

import models

database_path = os.path.abspath("./vol-maintenance.db")

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

corde = models.Corde(
    "zenith",
    "beal",
    "xab789",
    80,
    "rose",
    "simple",
    "Lot de deux cordes",
    date.today(),
    date.today(),
    date.today(),
    date.today(),
)

corde.register_on(cursor)
connection.commit()
connection.close()

