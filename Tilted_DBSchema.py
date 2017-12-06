from dateline import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="tilted4",
    password="grades777",
    hostname="tilted4.mysql.pythonanywhere-services.com",
    databasename="tilted4$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "fghr393ghdg93ggh3933"
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(128))
  password_hash = db.Column(db.String(128))
  email = db.Column(db.String(128))
  birth_date = db.Column(db.String(128))
  first_name = db.Column(db.String(128))
  last_name = db.Column(db.String(128))
  comments = db.relationship('Comment')

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def get_id(self):
    return self.username

  def __repr__(self):
    return "<User(fname='%s', lname='%s', username='%s', email='%s', birth_date='%s')>" %(
      self.first_name, self.last_name, self.username, self.email, self.birth_date)


class Game(db.Model):
  __tablename__ = "game"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  summary = db.Column(db.String(4096))
  online_rating = db.Column(db.Integer, nullable=false)

  user_rating = db.relationship('Rate', backref='game')
  developed_by = db.relationship('Developed', backref='game')
  published_by = db.relationship('Published', backref='game')
  comments = db.relationship('Comment', backref='game')
  genre = db.relationship('Genre')
  price = db.Column(db.String(128))
  release = db.Colubm(db.String(128))
  available_on = db.relationship('Available', backref='game')

  def __repr__(self):
    return "<Game(title='%s', summary='%s', rating='%d')>" % (
      self.title, self.summary, self.rating)


class Company(db.Model):
  __tablename__ = "company"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), unique=True, nullable=False)
  location = db.Column(db.String(1028), nullable=False)
  established = db.Column(db.String(128), nullable=False)

  publishers = db.relationship("Publisher")
  developers = db.relationship("Developer")
  consoles = db.relationship("Console")

  def __repr__(self):
    return "<Company(name='%s', location='%s', established='%s')>" % (
      self.name, self.location, self.established)


class Developer(db.Model):
  __tablename__ = "developer"

  id = db.Column(db.Integer, primary_key=True)
  company = db.Column(db.Integer, db.ForeignKey('company.id'))


class Publisher(db.Model):
  __tablename__ = "publisher"

  id = db.Column(db.Integer, primary_key=True)
  company = db.Column(db.Integer, db.ForeignKey('company.id'))


class Developed(db.Model):
  __tablename__ = 'developed'

  id = db.Column(db.Integer, primary_key=True)
  developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'))
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'))


class Published(db.Model):
  __tablename__ = 'published'

  id = db.Column(db.Integer, primary_key=True)
  publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'))


class Comment(db.Model):
  __tablename__ = "comments"

  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(4096))
  posted = db.Column(db.DateTime, default=datetime.now)
  commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

  commenter = db.relationship('User', foreign_keys=commenter_id)


class Rate(db.Model):
  __tablename__ = "rate"

  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

  def __repr__(self):
    return "<Rate(user_rating='%d')>" % (
      self.rating)


class Genre(db.Model):
  __tablename__ = "genre"

  id = db.Column(db.Integer, primary_key=True)
  genre = db.Column(db.String(128), nullable=False)

  game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

  def __repr__(self):
    return "<Genre(genre='%s')>" % (self.genre)


class Console(db.Model):
  __tablename__ = "console"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), unique=True, nullable=False)
  description = db.Column(db.String(2048))
  release = db.Column(db.String(128), nullable=False)
  company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
  available_on = db.relationship("Available")


class Available(db.Model):
  __tablename__ = "available"

  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
  company_id = db.Column(db.Integer, db.ForeignKey('console.id'))
