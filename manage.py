from flask_script import Manager, Command

from app import app


manager = Manager(app)


@manager.command
def initdb():
    from app.models import db
    db.create_all()

@manager.command
def upd8db():
    from app.pflog import PFLogger
    PFLogger('pflog.0', 'geolite.mmdb').parser()  #TODO test if args are valid


if __name__ == '__main__':
    manager.run()

