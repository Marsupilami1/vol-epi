from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cordes(db.Model):
    __tablename__ = "Cordes"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    fabricant = db.Column(db.String(30))
    modele = db.Column(db.String(30))
    serie = db.Column(db.String(30))
    longueur = db.Column(db.Integer)
    couleur = db.Column(db.String(30))
    utilisation = db.Column(db.String(20))
    description = db.Column(db.String(50))
    date_fin_vie = db.Column(db.Date)
    date_utilisation = db.Column(db.DATE)


class ControlesCordes(db.Model):
    __tablename__ = "ControlesCordes"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    corde_id = db.Column(db.Integer, db.ForeignKey("Cordes.id"), nullable=False)
    corde = db.relationship("Cordes", backref=db.backref("ControlesCordes", lazy=True))
    date = db.Column(db.DATE)
    remarques = db.Column(db.String(50))
    usure = db.Column(db.String(20))
    brulures = db.Column(db.String(20))
    coupures = db.Column(db.String(20))
    peluches = db.Column(db.String(20))
    ame = db.Column(db.String(20))
