from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@frontend_bp.route('/')
def index():
    return render_template('index.html')
