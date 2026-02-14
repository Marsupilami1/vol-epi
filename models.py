from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EPI(db.Model):
    __tablename__ = "EPI"
    epi_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    epi_kind_id = db.Column(db.Integer, db.ForeignKey("Kind.kin_id"), nullable=False)
    epi_kind = db.relationship("Kind", backref=db.backref("EPI", lazy=True))
    epi_type = db.Column(db.String(20))
    epi_brand = db.Column(db.String(20), nullable=False)
    epi_product_name = db.Column(db.String(50))
    epi_amount = db.Column(db.Integer)
    epi_marking = db.Column(db.String(100))
    epi_storage_id = db.Column(
        db.Integer, db.ForeignKey("Storage.sto_id"), nullable=False
    )
    epi_storage = db.relationship("Storage", backref=db.backref("EPI", lazy=True))
    epi_manufacturing_date = db.Column(db.DATE)
    epi_first_use_date = db.Column(db.DATE)
    epi_life_time = db.Column(db.Integer)


class Kind(db.Model):
    __tablename__ = "Kind"
    kin_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    kin_name = db.Column(db.String(30))


class Storage(db.Model):
    __tablename__ = "Storage"
    sto_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    sto_name = db.Column(db.String(100))


class Control(db.Model):
    __tablename__ = "Control"
    con_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    con_epi_id = db.Column(db.Integer, db.ForeignKey("EPI.epi_id"), nullable=False)
    con_epi = db.relationship("EPI", backref=db.backref("Control", lazy=True))
    con_date = db.Column(db.Date)


class Waste(db.Model):
    __tablename__ = "Waste"
    was_epi_id = db.Column(
        db.Integer, db.ForeignKey("EPI.epi_id"), primary_key=True, nullable=False
    )
    was_epi = db.relationship("EPI", backref=db.backref("Waste", lazy=True))
    was_date = db.Column(db.DATE)
