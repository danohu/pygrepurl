import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask.ext.restful import abort
from flask.ext.migrate import Migrate
from flask.ext.cors import CORS

app = flask.Flask(__name__)
app.config.from_object('config')
# currently unneeded
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources=r'/*', allow_headers='*')

@app.errorhandler(404)
def not_found(error):
    err = {'message': "Resource doesn't exist."}
    return flask.jsonify(**err)


from app.urlsearch.resources import urlsearch_bp
from app.urlsearch.frontend import frontend_bp
from app.auth.resources import auth_bp

app.register_blueprint(
    urlsearch_bp,
    url_prefix='/urlsearch'
)

app.register_blueprint(
    frontend_bp,
    url_prefix = ''
    )

app.register_blueprint(
    auth_bp,
    url_prefix='/auth'
)
