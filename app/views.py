from flask import Blueprint, render_template


resp = Blueprint('resp', __name__, template_folder='templates')


@resp.route('/')
def index():
    return render_template('index.html')

@resp.route('/packets/')
@resp.route('/packets/<int:days>')
def route_packets(days=1):
    return get_packets(days)

