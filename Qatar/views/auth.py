from distutils.log import error
import functools
from flask import(
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from Qatar.models.user import Users

from Qatar import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

#Register a new user
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        users = Users(username=username, password=generate_password_hash(password))
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        user_name = users.query.filter_by(username=username).first()
        if user_name == None:
            db.session.add(users)
            db.session.commit()
        else:
            error = f'User {username} already exists.'

        if error is None:
            flash('User created successfully.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('auth/register.html')

#Login a user
#if the user is logged in, redirect to the maintenance page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None:
        return redirect(url_for('qatar.agregar_jugador'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()
        error = None
        if not user:
            error = 'Username is incorrect.'
        elif not check_password_hash(user.password, password):
            error = 'Password is incorrect.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            flash('You were logged in.', 'success')
            return redirect(url_for('qatar.agregar_jugador'))
        else:
            flash(error)
    return render_template('auth/login.html')

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.get_or_404(user_id)

@auth.route('/logout')
def logout():
    session.clear()
    flash('You were logged out.', 'success')
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view