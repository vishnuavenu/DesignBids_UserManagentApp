from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from app import app
from app.form import UserForm
DEFUALT_GID = 1002

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
        user['home'] = request.form.get("home")
        user['shell'] = request.form.get("shell")
        user['password'] = request.form.get("password")

        if MANAGER.find_user_by_name(user['username']) is None:
            print("[+] User Seems not exist in System table ...... ")
            print("Generating UID for this user .... ")

            MANAGER.register_user(user, DEFUALT_GID)
            print("User registered .... ")
            return redirect(url_for("index"))

    return render_template('index.html', form=form, people=MANAGER.getallusers(2)


@app.route("/action/" , methods=['POST'])
def actionOnRecord():
    if request.method == "POST":
        if request.form['submit'] == 'Update':
            pass
            return redirect(url_for("index"))
        if request.form['submit'] == 'Delete':
            pass
    return redirect(url_for("index"))