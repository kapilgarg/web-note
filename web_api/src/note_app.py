"""
"""
import json
import flask
from flask import request
from models import Note
from database import db_session


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
        data = json.loads(data)
        if data:
            _save_note(data)
        return {'status': 'success'}

    if request.method == 'GET':
        all_notes = [note.serialize() for note in  Note.query.all()]
        return {
            'status': 'success',
            'data': all_notes
        }
    raise Exception('unsupported method - request.method')

def _save_note(data):
    note = Note(user_id=data.get('user_id'), text=data.get(
                'text'), source=data.get('source'))
    db_session.add(note)
    db_session.commit()



@app.route('/note/<note_id>', methods=['GET'])
def get(note_id):
    """
    handler for /note/<note_id>
    returns a note by note id
    if note is not presnt, raise 404
    """
    note = Note.query.filter(Note.id == note_id).first()
    if not note:
        flask.abort(404)
    return dict(status='success', data=note.serialize())


@app.errorhandler(404)
def page_not_found(error):
    """
    handler for 404
    """
    return "request resource is not available", 404


@app.after_request
def add_header(response):
    """
        adds additional headers in the response
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True
    response.headers['Access-Control-Allow-Methods'] = "GET,POST,OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Origin, Content-Type, Accept"
    return response

app.run(host='0.0.0.0')
