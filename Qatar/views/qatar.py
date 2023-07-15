import datetime
from math import trunc
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import Qatar
from Qatar.models.jugadores import Jugadores
from Qatar.models.selecciones import Selecciones
from Qatar.models.sedes import Sedes
from Qatar.models.fechas import Fechas
from Qatar.views.auth import login_required
from Qatar import db

Qatar = Blueprint('qatar', __name__)

# Redigir a index cuando se accede al sitio
@Qatar.route('/')
def redd():
    return redirect(url_for('qatar.index'))


#Cargar los jugadores con un inner join de la tabla selecciones
@Qatar.route('/index')
def index():
    jugadores = Jugadores.query.join(Jugadores.seleccion).all()
    for jugador in jugadores:
        fecha_nacimiento = jugador.fecha_nacimiento
        fecha_actual = datetime.date.today()
        edad = trunc((fecha_actual - fecha_nacimiento).days / 365.25)
        jugador.edad = edad
    return render_template('qatar/index.html', jugadores=jugadores)

#Cargar la tabla de posiciones
@Qatar.route('/posiciones')
def posiciones():
    return render_template('qatar/posiciones.html')

#Cargar la tabla de sedes
@Qatar.route('/sedes')
def sedes():
    sedes = Sedes.query.all()
    return render_template('qatar/sedes.html', sedes=sedes)

#Cargar la tabla de selecciones
@Qatar.route('/selecciones')
def selecciones():
    selecciones = Selecciones.query.all()
    return render_template('qatar/selecciones.html', selecciones=selecciones)

#Registrar una nueva selección
@Qatar.route('/agregar_seleccion', methods=['GET', 'POST'])
@login_required
def agregar_seleccion():
    selecciones = Selecciones.query.all()
    if request.method == 'POST':
        nombre_federacion = request.form.get('nombre_federacion')
        pais = request.form.get('pais')
        seleccion = Selecciones(nombre_federacion=nombre_federacion, pais=pais)
        db.session.add(seleccion)
        db.session.commit()
        flash('Selección agregada correctamente.', 'success')
        return redirect(url_for('qatar.agregar_seleccion'))

    return render_template('qatar/agregar_seleccion.html', selecciones=selecciones)


#Eliminar una selección
@Qatar.route('/delete/seleccion/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_seleccion(id):
    seleccion = Selecciones.query.get_or_404(id)
    db.session.delete(seleccion)
    db.session.commit()
    flash('Selección eliminada correctamente.', 'success')
    return redirect(url_for('qatar.agregar_seleccion'))



@Qatar.route('/editar_seleccion/edit/<int:id_seleccion>', methods=['GET', 'POST'])
@login_required
def editar_seleccion(id_seleccion):
    selecciones = Selecciones.query.all()
    seleccion = Selecciones.query.filter_by(id_seleccion=id_seleccion).first()
    return render_template('qatar/editar_seleccion.html', seleccion=seleccion, selecciones=selecciones)


@Qatar.route('/editar_seleccion/update/<int:id_seleccion>', methods=['GET', 'POST'])
@login_required
def actualizar_seleccion(id_seleccion):
    seleccion = Selecciones.query.filter_by(id_seleccion=id_seleccion).first()
    if request.method == 'POST':
        nombre_federacion = request.form.get('nombre_federacion')
        pais = request.form.get('pais')
        seleccion.nombre_federacion = nombre_federacion
        seleccion.pais = pais
        db.session.commit()
        flash('Selección actualizada correctamente.', 'success')
        return redirect(url_for('qatar.agregar_seleccion'))
    return render_template('qatar/agregar_seleccion.html', seleccion=seleccion)


#Registrar un nuevo jugador en la base de datos teniendo permisos de administrador
@Qatar.route('/agregar_jugador', methods=['GET', 'POST'])
@login_required
def agregar_jugador():
    selecciones = Selecciones.query.all()
    jugadores = Jugadores.query.all()
     #Transformar la fecha de nacimiento a edad
    for jugador in jugadores:
        fecha_nacimiento = jugador.fecha_nacimiento
        fecha_actual = datetime.date.today()
        edad = trunc((fecha_actual - fecha_nacimiento).days / 365.25)
        jugador.edad = edad

    if request.method == 'POST':
        apellidos = request.form.get('apellidos')
        nombres = request.form.get('nombres')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        altura = request.form.get('altura')
        posicion = request.form.get('posicion')
        edad = request.form.get('edad')
        id_seleccion = request.form.get('id_seleccion')
        goles = request.form.get('goles')
        asistencias = request.form.get('asistencias')
        jugador = Jugadores(apellidos=apellidos, nombres=nombres, fecha_nacimiento=fecha_nacimiento, altura=altura, posicion=posicion, id_seleccion=id_seleccion, goles=goles, asistencias=asistencias)
        db.session.add(jugador)
        db.session.commit()
        flash('Jugador agregado correctamente.', 'success')
        return redirect(url_for('qatar.agregar_jugador'))
    return render_template('qatar/agregar_jugador.html', selecciones=selecciones, jugadores=jugadores)


#Editar un jugador existente en la tabla jugadores
@Qatar.route('/editar_jugador/edit/<int:id_jugador>', methods=['GET', 'POST'])
def editar_jugador(id_jugador):
    jugador_seleccion = Jugadores.query.filter_by(id_jugador=id_jugador).join(Jugadores.seleccion).first()
    jugadores = Jugadores.query.all()
    for jugador in jugadores:
        fecha_nacimiento = jugador.fecha_nacimiento
        fecha_actual = datetime.date.today()
        edad = trunc((fecha_actual - fecha_nacimiento).days / 365.25)
        jugador.edad = edad
    selecciones = Selecciones.query.all()
    return render_template('qatar/editar_jugador.html', jugador_seleccion=jugador_seleccion, jugadores=jugadores, selecciones=selecciones)
    
    
@Qatar.route('/editar_jugador/update/<int:id_jugador>', methods=['GET', 'POST'])
def update_jugador(id_jugador):
    jugador = Jugadores.query.filter_by(id_jugador=id_jugador).first()
    jugador.apellidos = request.form.get('apellidos')
    jugador.nombres = request.form.get('nombres')
    jugador.fecha_nacimiento = request.form.get('fecha_nacimiento')
    jugador.altura = request.form.get('altura')
    jugador.posicion = request.form.get('posicion')
    jugador.id_seleccion = request.form.get('id_seleccion')
    jugador.goles = request.form.get('goles')
    jugador.asistencias = request.form.get('asistencias')
    db.session.commit()
    flash('Jugador actualizado correctamente.', 'success')
    return redirect(url_for('qatar.agregar_jugador'))



#Eliminar un jugador existente en la tabla jugadores
@Qatar.route('/delete/<int:id_jugador>')
def delete_jugador(id_jugador):
    jugador = Jugadores.query.filter_by(id_jugador=id_jugador).first()
    db.session.delete(jugador)
    db.session.commit()
    flash('Jugador eliminado correctamente.', 'success')
    return redirect(url_for('qatar.agregar_jugador'))


#Registrar una sede
@Qatar.route('/agregar_sede', methods=['GET', 'POST'])
@login_required
def agregar_sede():
    sedes = Sedes.query.all()
    if request.method == 'POST':
        nombre_sede = request.form.get('nombre_sede')
        pais = request.form.get('pais')
        direccion = request.form.get('direccion')
        estado = request.form.get('estado')
        area = request.form.get('area')
        capacidad = request.form.get('capacidad')
        sede = Sedes(nombre_sede=nombre_sede, pais=pais, direccion=direccion, estado=estado, area=area, capacidad=capacidad)
        db.session.add(sede)
        db.session.commit()
        flash('Sede agregada correctamente.', 'success')
        return redirect(url_for('qatar.agregar_sede'))
    return render_template('qatar/agregar_sede.html', sedes=sedes)



#Eliminar una sede existente en la tabla sedes
@Qatar.route('/delete/sede/<int:id_sede>')
def delete_sede(id_sede):
    sede = Sedes.query.filter_by(id_sede=id_sede).first()
    db.session.delete(sede)
    db.session.commit()
    flash('Sede eliminada correctamente.', 'success')
    return redirect(url_for('qatar.agregar_sede'))


#Editar una sede existente en la tabla sedes
@Qatar.route('/editar_sede/edit/<int:id_sede>', methods=['GET', 'POST'])
def editar_sede(id_sede):
    sede = Sedes.query.filter_by(id_sede=id_sede).first()
    sedes = Sedes.query.all()
    return render_template('qatar/editar_sede.html', sede=sede, sedes=sedes)


@Qatar.route('/editar_sede/update/<int:id_sede>', methods=['GET', 'POST'])
def update_sede(id_sede):
    sede = Sedes.query.filter_by(id_sede=id_sede).first()
    sede.nombre_sede = request.form.get('nombre_sede')
    sede.pais = request.form.get('pais')
    sede.direccion = request.form.get('direccion')
    sede.estado = request.form.get('estado')
    sede.area = request.form.get('area')
    sede.capacidad = request.form.get('capacidad')
    db.session.commit()
    flash('Sede actualizada correctamente.', 'success')
    return redirect(url_for('qatar.agregar_sede'))

#Registrar una fecha
@Qatar.route('/agregar_fecha', methods=['GET', 'POST'])
@login_required
def agregar_fecha():
    fechas = Fechas.query.all()
    if request.method == 'POST':
        nombre_fecha = request.form.get('nombre_fecha')
        fecha = request.form.get('fecha')
        fecha_fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        fecha_fecha = fecha_fecha.date()
        fecha = Fechas(nombre_fecha=nombre_fecha, fecha=fecha_fecha)
        db.session.add(fecha)
        db.session.commit()
        flash('Fecha agregada correctamente.', 'success')
        return redirect(url_for('qatar.agregar_fecha'))
    return render_template('qatar/agregar_fecha.html', fechas=fechas)