from flask import Flask
from flask_restplus import Api, Resource, fields
from source.environment.instance import environment_config
from flask_sqlalchemy import SQLAlchemy

class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite3'
        self.app.config['SECRET_KEY'] = "fkveF8c8V13i9r2"
        self.db = SQLAlchemy(self.app)
        self.api = Api(self.app,
            version='1.0',
            title='Sample Book API',
            description='A simple Book API',
            doc = environment_config["swagger-url"]
        )
        self.ns = self.api.namespace('api', description='API for authors and books')

    def run(self):
        self.db.create_all()
        self.app.run(
                debug = environment_config["debug"],
                port = environment_config["port"],
                host= environment_config["host"]
            )

server = Server()