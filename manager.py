#!flask/bin/python

import subprocess

from app import app, APP_GID, APP_GRP, USER_DIR
from flask_script import Manager, Server



manager = Manager(app)

@manager.command
def initialize():
    #Create application group
    try:
        subprocess.call(["groupadd" ,
                         "-g %d" % APP_GID,
                         "%s" % APP_GRP
                        ])
    except OSError as e:
        print(e)
    finally:
        subprocess.call(["mkdir",
                         "%s" % USER_DIR])

manager.add_command("runserver", Server())
#manager.add_command("initialize", initialize)

manager.run()