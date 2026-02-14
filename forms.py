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
from models import Kind, Storage


class AddEPI(Form):
    kind = QuerySelectField(
        "Genre", query_factory=lambda: Kind.query, get_label="kin_name"
    )
    ftype = StringField("Type", [validators.Length(max=20)])
    brand = StringField(
        "Marque", [validators.DataRequired(), validators.Length(max=20)]
    )
    product_name = StringField(
        "Modèle et/ou Numéro de série", [validators.Length(max=50)]
    )
    amount = IntegerField("Quantité/Nombre", [validators.NumberRange(min=0)])
    marking = StringField("Signe distinctif/Marquage", [validators.Length(max=100)])
    storage = QuerySelectField(
        "Stockage",
        [validators.DataRequired()],
        query_factory=lambda: Storage.query,
        get_label="sto_name",
    )
    manufacturing_date = DateField("Date de fabrication", [validators.optional()])
    first_use_date = DateField("Date de mise en service")
    life_time = IntegerField("Durée de vie (en années)", [validators.optional()])


class Move(Form):
    storage = QuerySelectField(
        "Déplacer vers",
        [validators.DataRequired()],
        query_factory=lambda: Storage.query,
        get_label="sto_name",
    )


class WasteForm(Form):
    submit = SubmitField("Mettre au rebut")
