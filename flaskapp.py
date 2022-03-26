# -*- coding:utf-8 -*-

from flask import Flask, Response, jsonify, redirect, render_template, request, url_for, flash, abort, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from Admins import Manage, Prefix
from Persian import Persian
import config

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

app.config.update(
    #Change Before Config
    SECRET_KEY = config.SECRET_KEY
)

#Change Before Config
TOKEN = config.SEC_TOKEN

#login module
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'danger'

class User(UserMixin):
    """ Test user details:
    username : test
    password : test """
    
    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)

#Change Before Config
# User ids should be set in database too 
users = [User(id) for id in range(0, config.NUM_USER_CREATE)]

@app.route("/", methods=['GET'])
@limiter.limit("10 / minute")
def root():
    return render_template('index.html')

@app.route("/bot", methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        if request.form.get("check") == None and request.form.get("send_all") != None:
            text = request.form.get("send_all")
            Manage().send_text_message(text=text)
            flash("Successfully Sent", "success")

        elif request.form.get("send_all") == None and request.form.get("check") != None:
            user_id = Persian().convert(request.form.get("check"))
            do = Manage().block_unblock(user_id=user_id)

            if do == True:
               flash("User successfully blocked", "success") 
            
            elif do == False:
                flash("User successfully Unblocked", "success")
            
            elif do == "Error":
                flash("Format Error", "danger")
            
            else:
                flash("An error occured", "danger")

        else:
            pass

    all_users = Manage().get_list()
    res_users = []

    for i in all_users:
        res_users.append({"first_name" : i[0], "last_name" : i[1], "user_name" : i[2], "chat_id" : i[3], "user_id" : i[4], "time_joined" : i[5]})
    
    user_number = Manage().count_member()
    blocked_number = len(Manage().get_block())

    res_numbers = [{"all" : user_number, "blocked" : blocked_number}]

    return render_template('admin.html', data = {"users" : res_users, "numbers" : res_numbers, "current" : session['username'], "token" : TOKEN}), 200
    
@app.route(f'/bot/v1/{TOKEN}/members', methods=["GET"])
def get_members():
    
    rows = Manage().get_list()
    res = []

    for i in rows:
        res.append({"first_name" : i[0], "last_name" : i[1], "user_name" : i[2], "chat_id" : i[3], "user_id" : i[4], "time_joined" : i[5]})
    
    return render_template('show_members.html', data = {'users' : res}), 200

@app.route(f'/bot/v1/{TOKEN}/blocked_members', methods=["GET"])
def get_block_members():
    rows = Manage().get_block_info()
    res = []

    for i in rows:
        res.append({"first_name" : i[0], "last_name" : i[1], "user_name" : i[2], "chat_id" : i[3], "user_id" : i[4], "time_joined" : i[5]})
    
    return render_template('show_members.html', data = {'users' : res}), 200

@app.route('/bot/v1/check', methods=["GET"])
@limiter.limit("10 / minute")
def check():
    ret = {"message" : "System Works Great :))))"}

    return jsonify(ret), 200

@app.route(f'/bot/v1/{TOKEN}/prefixt2', methods=["GET"])
def prefixt2():
    pre = request.args.get('pre')
    dorost2 = [
        ("دستگاه تنفس 🫁", "ta"),
        ("دستگاه غدد 🌋", "es"),
        ("دستگاه قلب 🫀", "hea"),
        ("بیوشیمی دیسیپلین نظری 🧪", "cht2"),
        ("بیوشیمی دیسیپلین عملی 🧪", "chat2"),
        ("علوم تشریح عملی 💀", "att2"),
        ("فیزیولوژی عملی 🔎", "phya"),
        ("تغذیه 🍫", "tgh"),
        ("کامپیوتر 💻", "com"),
        ("زبان عمومی " + "2️⃣", "za2"),
        ("اندیشه اسلامی 📿", "an1"),
        ("انقلاب اسلامی 🕋", "en"),
        ("جامعه شناسی سلامت 👥", "jam"),
        ("خلاقیت و کارآفرینی 💼", "khl"),
        ("آداب پزشکی " + "2️⃣", "ada2"),
        ("... سایر", "other")
    ]

    if pre:
        rows = Prefix().prefixt2(query=pre)
        if rows != False:
            res = []
            for i in rows:
                res.append({"prefix" : i[0], "type" : i[1], "file_id" : i[2], "caption" : i[3]})

            return render_template('show_prefix.html', data = {'prefixes' : res, "category" : pre.upper()}), 200

        else:
            return render_template('404.html'), 404
    
    else:
        res = []

        for i in dorost2:
            res.append({"dars" : i[0], "link" : f"/bot/v1/{TOKEN}/prefixt2?pre={i[1]}"})

        return render_template('pre_list.html', data={'list' : res}), 200

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 / minute")
def login():
    if current_user.is_authenticated:
        return redirect('/bot')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Manage().get_admins_login(username=username, password=password) != "False":
            login_user(User(Manage().get_admins_login(username=username, password=password)))
            session['username'] = username
            return redirect('/bot')
        else:
            return abort(401)
    else:
        return render_template('login.html')

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect('/login')

@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.errorhandler(401)
def unauthorized(error):
    flash('An error occured', 'danger')
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()