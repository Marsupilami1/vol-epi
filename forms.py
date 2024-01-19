from wtforms import (
    Form,
    StringField,
    IntegerField,
    SelectField,
    DateField,
    RadioField,
    SubmitField,
    validators,
)
from wtforms_sqlalchemy.fields import QuerySelectField
from datetime import date
from models import Genre, Stockage


class AjoutMateriel(Form):
    genre = QuerySelectField(
        "Genre", query_factory=lambda: Genre.query, get_label="gen_name"
    )
    ftype = StringField("Type", [validators.Length(max=20)])
    marque = StringField(
        "Marque", [validators.DataRequired(), validators.Length(max=20)]
    )
    modele = StringField("Modèle", [validators.Length(max=50)])
    quantite = IntegerField("Quantité/Nombre", [validators.NumberRange(min=0)])
    marquage = StringField("Signe distinctif/Marquage", [validators.Length(max=100)])
    stockage = QuerySelectField(
        "Stockage",
        [validators.DataRequired()],
        query_factory=lambda: Stockage.query,
        get_label="sto_name",
    )
    date_fabrication = DateField("Date de fabrication")
    date_utilisation = DateField("Date de mise en service")
    duree_vie = IntegerField("Durée de vie (en années)", [validators.optional()])


class RebutForm(Form):
    submit = SubmitField("Mettre au rebut")
