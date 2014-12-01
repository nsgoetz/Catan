from flask import Flask, session, redirect, url_for, escape, \
      request, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask.ext.bcrypt import Bcrypt

def create_app(configfile=None):
  app = Flask(__name__)
  Bootstrap(app)
  app.config.from_object('config')
  #AppConfig(app, configfile)

  return app

app = create_app()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from app import views, models