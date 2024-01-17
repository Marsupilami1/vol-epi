from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cordes(db.Model):
    __tablename__ = "Cordes"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    modele = db.Column(db.String(30))
    fabricant = db.Column(db.String(30))
    longueur = db.Column(db.Integer)
    couleur = db.Column(db.String(30))
    utilisation = db.Column(db.String(20))
    description = db.Column(db.String(50))
    date_fabrication = db.Column(db.Date)
    date_fabrication = db.Column(db.Date)
    date_achat = db.Column(db.Date)
    date_fin_vie = db.Column(db.Date)
    date_utilisation = db.Column(db.DATE)

class ControlesCordes(db.Model):
    __tablename__ = "ControlesCordes"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    corde_id = db.Column(db.Integer, db.ForeignKey('Cordes.id'), nullable=False)
    corde = db.relationship('Cordes', backref=db.backref('ControlesCordes', lazy=True))
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
    """
