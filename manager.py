#!flask/bin/python
from app import app
from flask_script import Manager, Server, Shell

manager = Manager(app)
manager.add_command("runserver", Server())


manager.run()