from Qatar import db

class Jugadores(db.Model):
    __table_name__ = 'jugadores'
    id_jugador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apellidos = db.Column(db.String(80), nullable=False)
    nombres = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    altura = db.Column(db.Numeric(precision=6, scale=2), nullable=False)
    posicion = db.Column(db.String(80), nullable=False)
    id_seleccion = db.Column(db.Integer, db.ForeignKey('selecciones.id_seleccion'), nullable=False)
    goles = db.Column(db.Integer, nullable=False)
    asistencias = db.Column(db.Integer, nullable=False)

    seleccion = db.relationship('Selecciones')

    def __init__(self, apellidos, nombres, fecha_nacimiento, altura, posicion, id_seleccion, goles, asistencias):
        self.apellidos = apellidos
        self.nombres = nombres
        self.fecha_nacimiento = fecha_nacimiento
        self.altura = altura
        self.posicion = posicion
        self.id_seleccion = id_seleccion
        self.goles = goles
        self.asistencias = asistencias
    
    def __repr__(self):
        return "<Jugadores id_jugador='%s'>" % (self.id_jugador)