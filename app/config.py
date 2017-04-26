import os


class Production:
    DEBUG = False
    JSON_AS_ASCII = False
    DBUSER = 'postgres'
    DBPASS = 'foobar'
    DBHOST = '127.0.0.1'
    DBPORT = '5432'
    DBNAME = 'tesla'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}\
        /{4}'.format(DBUSER, DBPASS, DBHOST, DBPORT, DBNAME)
    SECRET_KEY = 'Q.\=wNpSa=J}1>9bH*VPyYgWf1[<R[%*0NJ-?jJ"H*g"|S=aP]]'

class Development(Production):
    DEBUG = True


config = {
    'development': 'app.config.Development',
    'production': 'app.config.Production'
}


def configure_app(app):
    app.config.from_object(config[os.getenv('TESLA_MODE', 'production')])

