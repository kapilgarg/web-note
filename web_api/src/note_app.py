"""
"""
import json
import flask
from flask import request
import db

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    """
    Home
    """
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    """
    handler for /notes
    """
    if request.method == 'POST':
        data = request.data.decode('UTF-8')
        print("******************************************"+data)
        data = json.loads(data)
        if data:
            db.save(data)
        response = flask.Response('success')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = True
        response.headers['Access-Control-Allow-Methods']= "GET,POST,OPTIONS"
        response.headers['Access-Control-Allow-Headers']= "Origin, Content-Type, Accept"
        response.headers['Access-Control-Allow-Headers']= "Origin, Content-Type, Accept"
        return response 

    if request.method == 'GET':
        return {
            'status': 'success',
            'data': db.get_all(limit=20, offset=0)
        }
    raise Exception('unsupported method - request.method')


@app.route('/note/<note_id>')
def get(note_id):
    """
    returns a note by id
    """
    note = db.get(note_id)
    if not note:
        flask.abort(404)
    return dict(status='success', data=note)


@app.errorhandler(404)
def page_not_found(error):
    return "request resource is not available", 404


def get_all(limit=20, offset=0):
    return db.get_all(limit, offset)


app.run(host='0.0.0.0')
