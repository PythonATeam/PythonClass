from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

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
    username = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    birth_date = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    comments = db.relationship('Comment')


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

    def __repr__(self):
        return "<User(fname='%s', lname='%s', username='%s', email='%s', birth_date='%s')>" % (
                self.first_name, self.last_name, self.username, self.email, self.birth_date)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096), nullable=False)
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    #game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register_page.html", error=False)

    user = load_user(request.form["username"])

    if not user is None:
        return render_template("register_page.html", error=True)

    if request.form["password"] != request.form["pwconfirm"]:
        return render_template("register_page.html", passfail=True)


    newuser = User(username=request.form["username"], password_hash=generate_password_hash(request.form["password"]),
    email=request.form["email"], birth_date=request.form["bday"], first_name=request.form["fname"], last_name=request.form["lname"])

    db.session.add(newuser)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))