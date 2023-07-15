from Qatar import db

class Selecciones(db.Model):
    __table_name__ = 'selecciones'
    id_seleccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_federacion = db.Column(db.String(80), nullable=False)
    pais = db.Column(db.String(80), nullable=False)
    
    jugadores = db.relationship('Jugadores')


    def __init__(self, nombre_federacion, pais):
        self.nombre_federacion = nombre_federacion
        self.pais = pais

    def __repr__(self):
        return "<Selecciones id_seleccion='%s'>" % (self.id_seleccion)