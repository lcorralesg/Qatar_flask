from Qatar import db

class Fechas(db.Model):
    __table_name__ = 'fechas'
    id_fecha = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seleccion_local = db.Column(db.Integer, db.ForeignKey('selecciones.id_seleccion'), nullable=False)
    seleccion_visitante = db.Column(db.Integer, db.ForeignKey('selecciones.id_seleccion'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    sede = db.Column(db.Integer, db.ForeignKey('sedes.id_sede'), nullable=False)
    goles_local = db.Column(db.Integer, nullable=False)
    goles_visitante = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(80), nullable=False)

    def __init__(self, seleccion_local, seleccion_visitante, fecha, hora, sede, goles_local, goles_visitante, estado):
        self.seleccion_local = seleccion_local
        self.seleccion_visitante = seleccion_visitante
        self.fecha = fecha
        self.hora = hora
        self.sede = sede
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante
        self.estado = estado
    
    def __repr__(self):
        return "<Fechas id_fecha='%s'>" % (self.id_fecha)