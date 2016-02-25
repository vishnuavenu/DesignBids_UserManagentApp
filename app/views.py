import os

from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from app import app
from app.form import UserForm

DEFUALT_GID = 1002
ROOT_DIR = "/tmp/"


# Initializing User Manager
from app.userandgrpmanager import UserandGrpManager

MANAGER = UserandGrpManager()
MANAGER.update()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm(request.form, csr_enabled = False)
    if request.method == 'POST':
        user = {}
        user['username'] = request.form.get('username')
        user['home'] = ROOT_DIR+request.form.get("home")
        if len(user["home"]) < 1: user["home"] = ROOT_DIR+user["username"]
        user['shell'] = request.form.get("shell")
        user['password'] = request.form.get("password")

        if MANAGER.find_user_by_name(user['username']) is None:
            print("[+] User Seems not exist in System table ...... ")
            print("Generating UID for this user .... ")

            MANAGER.register_user(user, DEFUALT_GID)
            print("User registered .... ")
            return redirect(url_for("index"))

    return render_template('index.html', form=form, people=MANAGER.getallusers(DEFUALT_GID))


@app.route("/action/", methods=['POST'])
def actionOnRecord():
    if request.method == "POST":
        if request.form['submit'] == 'Update':
            user = {}

            user["actual_name"] = request.form.get("actual_name")
            user["username"] = request.form.get("username")
            user["password"] = request.form.get("password")
            user["shell"] = request.form.get("shell")
            user["gid"] = request.form.get("gid")
            user["home"] = request.form.get("home")

            print("[+] This user going to be updated .... %s"%(user["username"]))
            MANAGER.update_user(user, DEFUALT_GID)
            del user # Cleaning of Previous Mess
            return redirect(url_for("index"))

        if request.form['submit'] == 'Delete':

            print("[+] Deletion Initiated.....")
            username = request.form.get("actual_name")
            print("[*] [ He/She ]Going to be deleted ...... %s "%(username))

            MANAGER.remove_user(username)
            print("[*] %s is deleted now! " % username)

            return redirect(url_for("index"))