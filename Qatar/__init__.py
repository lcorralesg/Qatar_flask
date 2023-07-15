from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from Qatar.views.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from Qatar.views.qatar import Qatar as qatar_blueprint
app.register_blueprint(qatar_blueprint)

db.create_all()