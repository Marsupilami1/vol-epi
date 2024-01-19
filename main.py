from flask import Flask, render_template, request, redirect, abort
from flask_socketio import SocketIO
from datetime import date
import os

from models import EPI, Genre, Stockage, Controle, Rebut
from models import db
import forms

import sys

# --------------------------------------------#
# Init App.
# --------------------------------------------#
app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
socketio = SocketIO(app)

# --------------------------------------------#
# Create the database if asked to do so.
# --------------------------------------------#
if len(sys.argv) >= 2 and sys.argv[1] == "create-database":
    if os.path.exists("./database.db"):
        print("The database exists, please remove it before you create a new one.")
        exit(1)
    with app.app_context():
        db.create_all()
        print("[INFO] Database created.")

        # Fill `Genre` table
        db.session.add(Genre(gen_name="Harnais"))
        db.session.add(Genre(gen_name="Corde"))
        db.session.add(Genre(gen_name="Casque"))
        db.session.add(Genre(gen_name="Anneau"))
        db.session.add(Genre(gen_name="Assureur"))
        db.session.add(Genre(gen_name="Degaine"))
        db.session.add(Genre(gen_name="Mousqueton"))
        db.session.add(Genre(gen_name="Bloqueur"))
        db.session.add(Genre(gen_name="Coinceur"))

        # Fill `Stockage` table
        db.session.add(Stockage(sto_name="Local Félix"))
        db.session.add(Stockage(sto_name="Caisse cours jeunes/débutants"))
        db.session.add(Stockage(sto_name="Caisse maintenance"))
        db.session.add(Stockage(sto_name="Caisse Sortie"))
        db.session.add(Stockage(sto_name="Sac cours enfants/jeunes"))
        db.session.add(Stockage(sto_name="Sac Handisport"))

        db.session.commit()
        print("[INFO] Database populated.")
    exit(0)


# --------------------------------------------#
# Routes.
# --------------------------------------------#
@app.route("/")
def home():
    return render_template("pages/index.html")


@app.route("/ajout", methods=["GET", "POST"])
def ajout():
    form = forms.AjoutMateriel(request.form)
    if request.method == "POST" and form.validate():
        epi = EPI(
            epi_genre=form.genre.data,
            epi_type=form.ftype.data,
            epi_marque=form.marque.data,
            epi_modele=form.modele.data,
            epi_quantite=form.quantite.data,
            epi_marquage=form.marquage.data,
            epi_stockage=form.stockage.data,
            epi_date_fabrication=form.date_fabrication.data,
            epi_date_utilisation=form.date_utilisation.data,
            epi_duree_vie=form.duree_vie.data,
        )
        db.session.add(epi)
        # Ajout automatique d'un contrôle
        db.session.flush()  # récupération de ei.epi_id
        db.session.refresh(epi)
        controle = Controle(
            con_epi_id=epi.epi_id,
            con_date=form.date_utilisation.data,
        )
        db.session.add(controle)
        db.session.commit()
        return redirect(f"/epi/{epi.epi_id}")
    return render_template("pages/ajout.html", form=form)


@app.route("/recherche/genre")
def recherche_genre():
    data = []
    for genre in Genre.query.all():
        epis = []
        for epi in EPI.query.filter(EPI.epi_genre == genre):
            fin_de_vie = None
            urgence = "all good"
            if epi.epi_duree_vie != None:
                fin_de_vie = epi.epi_date_utilisation.year + epi.epi_duree_vie
                if fin_de_vie - date.today().year <= 2:
                    urgence = "worrying"
                if fin_de_vie - date.today().year <= 1:
                    urgence = "critical"
            epis.append(
                {
                    "id": epi.epi_id,
                    "type": epi.epi_type.capitalize(),
                    "marque": epi.epi_marque,
                    "modele": epi.epi_modele,
                    "count": epi.epi_quantite,
                    "marquage": epi.epi_marquage.capitalize(),
                    "stockage": epi.epi_stockage.sto_name,
                    "fin_de_vie": fin_de_vie,
                    "urgence": urgence,
                }
            )
        data.append(
            {
                "genre": genre.gen_name,
                "epis": epis,
            }
        )
    return render_template("pages/recherche_genre.html", data_by_genre=data)

@app.route("/recherche/stockage")
def recherche_stockage():
    data = []
    for stockage in Stockage.query.all():
        epis = []
        for epi in EPI.query.filter(EPI.epi_stockage == stockage):
            fin_de_vie = None
            urgence = "all good"
            if epi.epi_duree_vie != None:
                fin_de_vie = epi.epi_date_utilisation.year + epi.epi_duree_vie
                if fin_de_vie - date.today().year <= 2:
                    urgence = "worrying"
                if fin_de_vie - date.today().year <= 1:
                    urgence = "critical"
            epis.append({
                    "genre": epi.epi_genre.gen_name,
                    "id": epi.epi_id,
                    "type": epi.epi_type.capitalize(),
                    "marque": epi.epi_marque,
                    "modele": epi.epi_modele,
                    "count": epi.epi_quantite,
                    "marquage": epi.epi_marquage.capitalize(),
                    "fin_de_vie": fin_de_vie,
                    "urgence": urgence,
                })
        data.append({
                "stockage": stockage.sto_name,
                "epis": epis,
            })
    return render_template("pages/recherche_stockage.html", data_by_stockage=data)

@app.route("/epi/<int:epi_id>", methods=["GET", "POST"])
def epi(epi_id):
    """
    Interface de gestion d'un lot d'EPI.
    - Toutes les informations relative à/au lot d'EPI.
    - Stockage: visiter et déplacer
    - Contrôles: liste, ajouter et mettre au rebut
    """
    form = forms.Deplacement(request.form)
    if request.method == "POST":
        if "rebut" in request.form.keys():
            rebut = Rebut(
                reb_epi_id=epi_id,
                reb_date=date.today(),
            )
            db.session.add(rebut)
            db.session.commit()
        elif "controle" in request.form.keys():
            controle = Controle(
                con_epi_id=epi_id,
                con_date=date.today(),
            )
            db.session.add(controle)
            db.session.commit()
        elif form.validate():
            epi = EPI.query.get({"epi_id": epi_id})
            epi.epi_stockage = form.stockage.data
            db.session.commit()

        return redirect(f"/epi/{epi_id}")

    epi = EPI.query.get({"epi_id": epi_id})
    if epi is None:
        abort(404)

    # REBUT
    dernier_rebut = Rebut.query.get({"reb_epi_id": epi_id})

    # CONTROLES
    controles = []
    for controle in Controle.query.where(Controle.con_epi_id == epi_id):
        controles.append({"date": controle.con_date.strftime("%m/%Y")})

    return render_template(
        "pages/epi.html",
        epi_id=epi_id,
        marque=epi.epi_marque,
        modele=epi.epi_modele,
        marquage="(" + epi.epi_marquage + ")" if epi.epi_marquage != "" else "",
        stockage=epi.epi_stockage.sto_name,
        has_rebut_date=dernier_rebut is not None,
        rebut_date=dernier_rebut,
        controles=controles,
        form=form,
    )

# -------------------------------------------#
# Launch.
# -------------------------------------------#
if __name__ == "__main__":
    socketio.run(app)
