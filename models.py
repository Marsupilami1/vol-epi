from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EPI(db.Model):
    __tablename__ = "EPI"
    epi_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    epi_genre_id = db.Column(db.Integer, db.ForeignKey("Genre.gen_id"), nullable=False)
    epi_genre = db.relationship("Genre", backref=db.backref("EPI", lazy=True))
    epi_type = db.Column(db.String(20))
    epi_marque = db.Column(db.String(20), nullable=False)
    epi_modele = db.Column(db.String(50))
    epi_quantite = db.Column(db.Integer)
    epi_marquage = db.Column(db.String(100))
    epi_stockage_id = db.Column(
        db.Integer, db.ForeignKey("Stockage.sto_id"), nullable=False
    )
    epi_stockage = db.relationship("Stockage", backref=db.backref("EPI", lazy=True))
    epi_date_fabrication = db.Column(db.DATE)
    epi_date_utilisation = db.Column(db.DATE)
    epi_duree_vie = db.Column(db.Integer)


class Genre(db.Model):
    __tablename__ = "Genre"
    gen_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    gen_name = db.Column(db.String(30))


class Stockage(db.Model):
    __tablename__ = "Stockage"
    sto_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    sto_name = db.Column(db.String(100))


class Controle(db.Model):
    __tablename__ = "Controle"
    con_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    con_epi_id = db.Column(db.Integer, db.ForeignKey("EPI.epi_id"), nullable=False)
    con_epi = db.relationship("EPI", backref=db.backref("Controle", lazy=True))
    con_date = db.Column(db.Date)


class Rebut(db.Model):
    __tablename__ = "Rebut"
    reb_epi_id = db.Column(
        db.Integer, db.ForeignKey("EPI.epi_id"), primary_key=True, nullable=False
    )
    reb_epi = db.relationship("EPI", backref=db.backref("Rebut", lazy=True))
    reb_date = db.Column(db.DATE)
