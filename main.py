from flask import Flask, render_template, request, redirect, abort
from flask_socketio import SocketIO
from datetime import date
import os

from models import EPI, Kind, Storage, Control, Waste
from models import db
import forms

import sys

# Init App
app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
socketio = SocketIO(app)

# Create the database if needed
if len(sys.argv) >= 2 and sys.argv[1] == "create-database":
    if os.path.exists("./database.db"):
        print("The database exists, do you wan't to reinitialize it? [y/N]")
        yes_no = input()
        if yes_no == "y" or yes_no == "Y":
            print("[INFO] Database removed", file=sys.stderr)
            os.remove("./database.db")
        else:
            exit(0)
    with app.app_context():
        db.create_all()
        print("[INFO] Database created", file=sys.stderr)

        # Fill [Kind] table
        db.session.add(Kind(kin_name="Harnais"))
        db.session.add(Kind(kin_name="Corde"))
        db.session.add(Kind(kin_name="Casque"))
        db.session.add(Kind(kin_name="Anneau"))
        db.session.add(Kind(kin_name="Assureur"))
        db.session.add(Kind(kin_name="Degaine"))
        db.session.add(Kind(kin_name="Mousqueton"))
        db.session.add(Kind(kin_name="Bloqueur"))
        db.session.add(Kind(kin_name="Coinceur"))

        # Fill [Storage] table
        db.session.add(Storage(sto_name="Local Félix"))
        db.session.add(Storage(sto_name="Caisse cours jeunes/débutants"))
        db.session.add(Storage(sto_name="Caisse maintenance"))
        db.session.add(Storage(sto_name="Caisse Sortie"))
        db.session.add(Storage(sto_name="Sac cours enfants/jeunes"))
        db.session.add(Storage(sto_name="Sac Handisport"))

        db.session.commit()
        print("[INFO] Database populated", file=sys.stderr)
    exit(0)


# Routes
@app.route("/")
def home():
    return render_template("pages/index.html")


@app.route("/ajout", methods=["GET", "POST"])
def ajout():
    form = forms.AddEPI(request.form)
    if request.method == "POST" and form.validate():
        epi = EPI(
            epi_kind=form.kind.data,
            epi_type=form.ftype.data,
            epi_brand=form.brand.data,
            epi_product_name=form.product_name.data,
            epi_amount=form.amount.data,
            epi_marking=form.marking.data,
            epi_storage=form.storage.data,
            epi_manufacturing_date=form.manufacturing_date.data,
            epi_first_use_date=form.first_use_date.data,
            epi_life_time=form.life_time.data,
        )
        db.session.add(epi)
        # Ajout automatique d'un contrôle
        db.session.flush()  # récupération de ei.epi_id
        db.session.refresh(epi)
        controle = Control(
            con_epi_id=epi.epi_id,
            con_date=form.first_use_date.data,
        )
        db.session.add(controle)
        db.session.commit()
        return redirect(f"/epi/{epi.epi_id}")
    return render_template("pages/ajout.html", form=form)


@app.route("/search/kind")
def search_kind():
    data = []
    for kind in Kind.query.all():
        epis = []
        for epi in EPI.query.filter(EPI.epi_kind == kind):
            discarded = Waste.query.get({"was_epi_id": epi.epi_id}) is not None

            end_of_life = None
            urgency = "all good"
            if epi.epi_life_time is not None:
                end_of_life = epi.epi_first_use_date.year + epi.epi_life_time
                if end_of_life - date.today().year <= 2:
                    urgency = "worrying"
                if end_of_life - date.today().year <= 1:
                    urgency = "critical"
            epis.append(
                {
                    "id": epi.epi_id,
                    "type": epi.epi_type.capitalize(),
                    "brand": epi.epi_brand,
                    "product_name": epi.epi_product_name,
                    "count": epi.epi_amount,
                    "marking": epi.epi_marking.capitalize(),
                    "storage": epi.epi_storage.sto_name,
                    "discarded": discarded,
                    "end_of_life": end_of_life,
                    "urgency": urgency,
                }
            )
        data.append(
            {
                "kind": kind.kin_name,
                "epis": epis,
            }
        )
    return render_template("pages/search_kind.html", data_by_kind=data)


@app.route("/search/storage")
def search_storage():
    data = []
    for storage in Storage.query.all():
        epis = []
        for epi in EPI.query.filter(EPI.epi_storage == storage):
            end_of_life = None
            urgency = "all good"
            if epi.epi_life_time != None:
                end_of_life = epi.epi_first_use_date.year + epi.epi_life_time
                if end_of_life - date.today().year <= 2:
                    urgency = "worrying"
                if end_of_life - date.today().year <= 1:
                    urgency = "critical"
            epis.append(
                {
                    "kind": epi.epi_kind.kin_name,
                    "id": epi.epi_id,
                    "type": epi.epi_type.capitalize(),
                    "brand": epi.epi_brand,
                    "product_name": epi.epi_product_name,
                    "count": epi.epi_amount,
                    "marking": epi.epi_marking.capitalize(),
                    "end_of_life": end_of_life,
                    "urgency": urgency,
                }
            )
        data.append(
            {
                "storage": storage.sto_name,
                "epis": epis,
            }
        )
    return render_template("pages/search_storage.html", data_by_storage=data)


@app.route("/epi/<int:epi_id>", methods=["GET", "POST"])
def epi(epi_id):
    """
    Interface de gestion d'un lot d'EPI.
    - Toutes les informations relative à/au lot d'EPI.
    - Stockage: visiter et déplacer
    - Contrôles: liste, ajouter et mettre au rebut
    """
    form = forms.Move(request.form)
    if request.method == "POST":
        if "discard" in request.form.keys():
            waste = Waste(
                was_epi_id=epi_id,
                was_date=date.today(),
            )
            db.session.add(waste)
            db.session.commit()
        elif "control" in request.form.keys():
            control = Control(
                con_epi_id=epi_id,
                con_date=date.today(),
            )
            db.session.add(control)
            db.session.commit()
        elif form.validate():
            epi = EPI.query.get({"epi_id": epi_id})
            epi.epi_storage = form.storage.data
            db.session.commit()

        return redirect(f"/epi/{epi_id}")

    epi = EPI.query.get({"epi_id": epi_id})
    if epi is None:
        abort(404)

    # WASTE
    waste_info = Waste.query.get({"was_epi_id": epi_id})

    # CONTROLS
    controls = []
    for control in Control.query.where(Control.con_epi_id == epi_id):
        controls.append({"date": control.con_date.strftime("%m/%Y")})

    return render_template(
        "pages/epi.html",
        epi_id=epi_id,
        brand=epi.epi_brand,
        product_name=epi.epi_product_name,
        marking="(" + epi.epi_marking + ")" if epi.epi_marking != "" else "",
        storage=epi.epi_storage.sto_name,
        discarded=waste_info is not None,
        controles=controls,
        form=form,
    )


# -------------------------------------------#
# Launch.
# -------------------------------------------#
if __name__ == "__main__":
    socketio.run(app)
