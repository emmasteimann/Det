from flask import render_template, jsonify, request, session, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)


@app.route("/",methods=["POST","GET"])
def index():
    chatrooms = ChatRoom.query.all()
    if request.method == "GET":
        if 'username' in session:
            return render_template('index.html',username=session["username"],chatrooms=chatrooms)
        else:
            return render_template('login.html')
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        res = User.query.filter_by(email=email).first()
        if res:
            if res.password == password:
                session["username"] = res.username
                return render_template('index.html',username=session["username"],chatrooms=chatrooms)
            else:
                return render_template("error.html",error=f'The password for account with the email {email} is wrong! please try again')
        else:
            return render_template("error.html",error= f'There is no account with the user name {username}')

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        newUser = User(email=email,username=username,password=password)
        db.session.add(newUser)
        db.session.commit()
        session['username'] = username
        return render_template('index.html',username=username)

@app.route("/signout")
def signout():
    session.pop('username',None)
    return redirect("/")

@app.route("/newchat",methods=["POST"])
def newchat():
    chatname = request.form.get("chatname")
    password = request.form.get("password")
    is_public = True if request.form.get("is_public") else False
    print(is_public)
    newChat = ChatRoom(name=chatname,password=password,is_public=is_public)
    db.session.add(newChat)
    db.session.commit()
    return redirect("/")

@app.route("/chat/<int:id>")
def chat(id):
    chat = ChatRoom.query.get(id)
    return render_template("/chatroom.html",chat=chat,username=session['username'])

@socketio.on("join room")
def join(data):
    join_room(data["room"])
    chat = ChatRoom.query.get(data["room"])
    emit('newMessage',{"message":session["username"] + ' has entered the room.'}, room=data["room"])

@socketio.on("message sent")
def message(data):
    print(data['message'])
    join_room(data["room"])
    emit('newMessage', {"message":data["message"],"user":session["username"]},room=data["room"])



