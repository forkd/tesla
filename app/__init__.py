from flask import Flask

from app.config import configure_app
from app.views import resp
from app.database import db

app = Flask('tesla')
configure_app(app)
app.register_blueprint(resp)
db.init_app(app)

