from wtforms import Form, StringField, IntegerField, SelectField, DateField, validators, RadioField
from datetime import date

from models import Cordes


class AjoutCordeForm(Form):
    fabricant = StringField("Fabricant", [validators.Length(max=30)])
    modele = StringField("Modèle", [validators.Length(max=30)])
    serie = StringField("Numéro de Série", [validators.Length(max=30)])
    longueur = IntegerField("Longueur (mètres)", [validators.NumberRange(min=0)])
    couleur = StringField("Couleur", [validators.Length(max=30)])
    utilisation = SelectField(
        "Simple/Double",
        choices=[("simple", "Corde à simple"), ("double", "Corde à double")],
    )
    description = StringField("Description", [validators.Length(max=50)])
    date_utilisation = DateField("Première utilisation")
    date_fin_vie = DateField("Fin de vie")


wear_level = [
    ("ras", "RAS"),
    ("mineure", "Mineure"),
    ("majeure", "Majeure"),
    ("definitive", "Définitive"),
]


class ControleCordeForm(Form):
    date = DateField("Date du contrôle", [validators.DataRequired()], default=date.today())
    remarques = StringField("Remarques", [validators.Length(max=50)])
    usure = RadioField("Usure", [validators.DataRequired()], choices=wear_level, default="ras")
    brulures = RadioField("Brûlure", [validators.DataRequired()], choices=wear_level, default="ras")
    coupures = RadioField("Coupures", [validators.DataRequired()], choices=wear_level, default="ras")
    peluches = RadioField("Zones pelucheuses", [validators.DataRequired()], choices=wear_level, default="ras")
    ame = SelectField(
        "État de l'âme",
        choices=[
            ("ras", "RAS"),
            ("apparente", "Une partie de l'âme est apparente"),
            ("rupture", "Zones éventuelles de ruptures internes"),
            ("hernie", "Elle possède une hernie"),
        ],
    )
