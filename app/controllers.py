import os
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from app import app
from app.form import UserForm

from app import APP_GID, USER_DIR



# Initializing User Manager
from app.usermanager import UserManager

MANAGER = UserManager()
# MANAGER.update_table()

@app.route('/', methods=['GET'])
def index():
    form = UserForm(request.form, csr_enabled=False)
    return render_template('index.html', form=form, users=MANAGER.get_all_users(APP_GID))


@app.route("/user/add", methods=['POST'])
def add():
    form = UserForm(request.form, csr_enabled=False)
    user = {}
    user['username'] = request.form.get('username')
    user['home'] = os.path.join(USER_DIR, request.form.get("home"))
    if len(user["home"]) < 1:
        user["home"] = USER_DIR+user["username"]
    user['shell'] = request.form.get("shell")
    user['password'] = request.form.get("password")

    if MANAGER.find_user_by_name(user['username']) is None:
        print("Generating UID for this user... ")
        MANAGER.register_user(user, APP_GID)
        print("User registered... ")
        return redirect(url_for("index"))
    else:
        print("userexists")
        return render_template('index.html', form=form, users=MANAGER.get_all_users(APP_GID), error="User already exists")


@app.route("/user/update", methods=['POST'])
def update():

    user = MANAGER.find_user_by_uid(int(request.form.get("uid")))
    print(" User Name : %s is going to updated ."% user)
    user['previous_name'] = user["username"]
    user["username"] = str(request.form.get("username"))
    user["shell"] = str(request.form.get("shell"))
    user["home"] = str(request.form.get("home"))

    print(user)
    print("[+] This user going to be updated : %s" %(user['previous_name']))
    MANAGER.update_user(user, APP_GID)
    del user
    return redirect(url_for("index"))




@app.route("/user/delete", methods=['POST'])
def delete():
    print("[+] Deletion Initiated.....")
    uid = request.form.get("uid")

    MANAGER.remove_user(uid)
    print("[*] %s is deleted now! " % uid)

    return redirect(url_for("index"))