from Qatar import db

class Sedes(db.Model):
    __table_name__ = 'sedes'
    id_sede = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_sede = db.Column(db.String(80), nullable=False)
    pais = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.String(80), nullable=False)
    area = db.Column(db.String(80), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)


    def __init__(self, nombre_sede, pais, direccion, estado, area, capacidad):
        self.nombre_sede = nombre_sede
        self.pais = pais
        self.direccion = direccion
        self.estado = estado
        self.area = area
        self.capacidad = capacidad
    
    def __repr__(self):
        return "<Sedes id_sede='%s'>" % (self.id_sede)