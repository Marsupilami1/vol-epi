from flask import Flask, render_template, request, redirect, abort
from flask_socketio import SocketIO

from models import Cordes, ControlesCordes
from models import db
from forms import AjoutCordeForm, ControleCordeForm

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
    with app.app_context():
        db.create_all()
    print("[INFO] Database created.")
    exit(0)


# --------------------------------------------#
# Routes.
# --------------------------------------------#
@app.route("/")
def home():
    return render_template("pages/index.html")


@app.route("/ajout")
def ajout():
    return render_template("pages/ajout.html")


@app.route("/ajout/corde", methods=["GET", "POST"])
def ajout_corde():
    form = AjoutCordeForm(request.form)
    if request.method == "POST" and form.validate():
        corde = Cordes(
            fabricant=form.fabricant.data,
            modele=form.modele.data,
            serie=form.serie.data,
            longueur=form.longueur.data,
            couleur=form.couleur.data,
            utilisation=form.utilisation.data,
            description=form.description.data,
            date_utilisation=form.date_utilisation.data,
            date_fin_vie=form.date_fin_vie.data,
        )
        db.session.add(corde)
        db.session.commit()
        return redirect("/")
    return render_template("pages/ajout_corde.html", form=form)


@app.route("/controle/corde/<int:corde_id>", methods=["GET", "POST"])
def controle_corde_id(corde_id):
    form = ControleCordeForm(request.form)
    if request.method == "POST" and form.validate():
        controle = ControlesCordes(
            corde_id=corde_id,
            date=form.date.data,
            remarques=form.remarques.data,
            usure=form.usure.data,
            brulures=form.brulures.data,
            coupures=form.coupures.data,
            peluches=form.peluches.data,
            ame=form.ame.data
        )
        db.session.add(controle)
        db.session.commit()
        return redirect(f"/recherche/corde/{corde_id}")
    return render_template("pages/controle_corde.html", corde_id=corde_id, form=form)


@app.route("/recherche")
def recherche():
    return render_template("pages/recherche.html")


@app.route("/recherche/corde")
def recherche_corde():
    data = []
    for corde in Cordes.query.all():
        data.append(
            {
                "id": corde.id,
                "modele": corde.modele,
                "serie": corde.serie,
                "couleur": corde.couleur,
                "longueur": corde.longueur,
            }
        )
    return render_template("pages/recherche_corde.html", data=data)


@app.route("/recherche/corde/<int:corde_id>")
def recherche_corde_id(corde_id):
    corde = Cordes.query.get({"id": corde_id})
    if corde is None:
        abort(404)

    data = []
    for controle in ControlesCordes.query.filter(ControlesCordes.corde_id == corde_id).order_by(ControlesCordes.date):
        data.append({"date": controle.date.strftime("%d/%m/%Y")})
    return render_template(
        "pages/recherche_corde_id.html",
        corde_id=corde_id,
        fabricant=corde.fabricant,
        modele=corde.modele,
        serie=corde.serie,
        couleur=corde.couleur.lower(),
        longueur=corde.longueur,
        data=data,
    )


# -------------------------------------------#
# Launch.
# -------------------------------------------#
if __name__ == "__main__":
    socketio.run(app)
