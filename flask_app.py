from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import desc
from sqlalchemy.sql import func

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
    ratings = db.relationship('Rate')


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

class Game(db.Model):
  __tablename__ = "game"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  summary = db.Column(db.String(4096))
  online_rating = db.Column(db.Float, nullable=True)
  developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable = False)
  publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable = False,)
  #comment_id = db.Column(db.Integer, nullable = True) #how to handle this
  genre = db.Column(db.String(256), nullable = False)
  price = db.Column(db.Float, nullable = False)
  publisher = db.relationship("Publisher")
  developer = db.relationship("Developer")

  def __repr__(self):
    return "<Game(title='%s', summary='%s')>" % (
      self.title, self.summary)


# DO THESE NEXT TABLES NEED LINES FOR THE ONE TO ONE RELATIONSHIP??
class Developer(db.Model):
  __tablename__ = "developer"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)

class Publisher(db.Model):
  __tablename__ = "publisher"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096), nullable=False)
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

class Rate(db.Model):
  __tablename__ = "rate"

  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer, nullable=False)
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

  #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  #game = db.relationship("Game", back_populates="rate")

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
  rater = db.relationship('User', foreign_keys=user_id)


  def __repr__(self):
    return "<Rate(user_rating='%d')>" % (
      self.rating)

#Game.rate = db.relationship("Rate", order_by=Rate.id, back_populates="game")


class Console(db.Model):
  __tablename__ = "console"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), unique=True, nullable=False)
  description = db.Column(db.String(2048))
  release_date = db.Column(db.String(128))
  manufacturer = db.Column(db.String(128))


class Available(db.Model):
  __tablename__ = "available"

  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
  console_id = db.Column(db.Integer, db.ForeignKey('console.id'), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():

    gameTable = Game.query.all()

    genrelist = set(x.genre for x in gameTable)
    myAvg = "0.00"



    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all(),
         games=Game.query.all(), avgprice=myAvg, genres=genrelist, userss=User.query.all())

    if not request.form.get('delme') == None:
       User.query.filter(User.id.in_(request.form["delme"])).delete(synchronize_session='fetch')
       for x in request.form.getlist("delme"):
           User.query.filter(User.id == x).delete()

    if not request.form.get('upme') == None:
        ourgame = Game.query.filter(Game.id == request.form["upid"]).first()
        ourgame.title = request.form["upme"]


#gameTable = Game.query.order_by(desc(Game.price)).all()

    """if not current_user.is_authenticated:
        return redirect(url_for('index'))"""

    if 'gamename' in request.form and request.form["gamename"] != "nothing" and 'sgenre' in request.form and request.form["sgenre"] != "nothing":
        if 'sortprice' in request.form:
            if request.form["sortprice"] == "high":
                searchResults=Game.query.filter(Game.title.contains(request.form["gamename"]), Game.genre==request.form["sgenre"]).order_by(Game.price)
            elif request.form["sortprice"] == "low":
                searchResults=Game.query.filter(Game.title.contains(request.form["gamename"]), Game.genre==request.form["sgenre"]).order_by(desc(Game.price))
        else:
            searchResults=Game.query.filter(Game.title.contains(request.form["gamename"]), Game.genre==request.form["sgenre"])
        myAvg=Game.query.with_entities(func.avg(Game.price).label('average')).filter(Game.title.contains(request.form["gamename"]), Game.genre==request.form["sgenre"]).first()
        return render_template("main_page.html", comments=Comment.query.all(), users=User.query.all(),
         games=Game.query.all(), genres=genrelist, avgprice=myAvg.average, results=searchResults, pgenre=request.form["sgenre"], pgamename=request.form["gamename"])


    if 'sgenre' in request.form and request.form["sgenre"] != "nothing":
        if 'sortprice' in request.form:
            if request.form["sortprice"] == "high":
                searchResults=Game.query.filter_by(genre=request.form["sgenre"]).order_by(Game.price)
            elif request.form["sortprice"] == "low":
                searchResults=Game.query.filter_by(genre=request.form["sgenre"]).order_by(desc(Game.price))
        else:
            searchResults=Game.query.filter_by(genre=request.form["sgenre"])
        myAvg=Game.query.with_entities(func.avg(Game.price).label('average')).filter_by(genre=request.form["sgenre"]).first()
        return render_template("main_page.html", comments=Comment.query.all(),
         games=Game.query.all(), genres=genrelist, avgprice=myAvg.average, users=User.query.all(), results=searchResults, pgenre=request.form["sgenre"], pgamename="nothing")

    elif 'gamename' in request.form:
        if 'sortprice' in request.form:
            if request.form["sortprice"] == "high":
                searchResults=Game.query.filter(Game.title.contains(request.form["gamename"])).order_by(Game.price)
                #gameAvg=Game.query(func.avg(Game.price).label('average')).filter(Game.title.contains(request.form["gamename"])).order_by(Game.price)
            elif request.form["sortprice"] == "low":
                searchResults=Game.query.filter(Game.title.contains(request.form["gamename"])).order_by(desc(Game.price))

        else:
            searchResults=Game.query.filter(Game.title.contains(request.form["gamename"]))
        myAvg=Game.query.with_entities(func.avg(Game.price).label('average')).filter(Game.title.contains(request.form["gamename"])).first()
        return render_template("main_page.html", comments=Comment.query.all(),
         games=Game.query.all(), genres=genrelist, avgprice=myAvg.average, users=User.query.all(), results=searchResults, pgenre="nothing", pgamename=request.form["gamename"])




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

@app.route("/compare/", methods=["GET", "POST"])
def compare():
    if request.method == "GET":
        return render_template("compare.html", error=False)


    return redirect(url_for('index'))


@app.route("/game/", methods=["GET", "POST"])
def game():

    if request.method == "POST":
        onegame=Game.query.filter_by(id=request.form["gid"]).first()


        gameid = onegame.id
        consoles = Console.query.all()
        available = Available.query.all()

        myConsoles = []
        for x in available:
            if x.game_id == gameid:
                myConsoles.append(x.console_id)

        myConsoleNames = []
        for x in myConsoles:
            myConsoleNames.append(Console.query.filter_by(id=x).first().name)

        onedev=db.session.query(Developer).join(Game, Developer.id==onegame.developer_id).first()
        #onedev=Developer.query.filter_by(id=onegame.developer_id).first()
        onepub=db.session.query(Publisher).join(Game, Publisher.id==onegame.publisher_id).first()
        #onepub=Publisher.query.filter_by(id=onegame.publisher_id).first()
        return render_template("game.html", error=False, game=onegame, dev=onedev, pub=onepub, cons=myConsoleNames)


    return redirect(url_for('index'))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))