class Materiel:
    pass


class Corde(Materiel):
    def __init__(
        self,
        modele,
        fabricant,
        serie,
        longueur,
        couleur,
        type,
        description,
        dfabrication,
        dachat,
        dfvie,
        dutilisation,
    ):
        self._id = None
        self._modele = modele
        self._fabricant = fabricant
        self._serie = serie
        self._longueur = longueur
        self._couleur = couleur
        self._type = type
        self._description = description
        self._dfabrication = dfabrication
        self._dachat = dachat
        self._dfvie = dfvie
        self._dutilisation = dutilisation

    def register_on(self, cursor):
        values = (
            self._modele,
            self._fabricant,
            self._serie,
            self._longueur,
            self._couleur,
            self._type,
            self._description,
            self._dfabrication.isoformat(),
            self._dachat.isoformat(),
            self._dfvie.isoformat(),
            self._dutilisation.isoformat(),
        )

        cursor.execute(
            """
          INSERT INTO Cordes (
            c_modele,
            c_fabricant,
            c_serie,
            c_longueur,
            c_couleur,
            c_type,
            c_description,
            c_dfabrication,
            c_dachat,
            c_dfvie,
            c_dutilisation)
          VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            values,
        )


class Controle:
    pass


class ControleCordes(Controle):
    pass
