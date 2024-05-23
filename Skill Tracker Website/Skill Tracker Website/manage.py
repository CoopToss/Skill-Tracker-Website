from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app, db  # Replace 'your_application' with the name of your Flask application package

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
