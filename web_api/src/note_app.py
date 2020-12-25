"""
"""
import json
import flask
from flask import request, render_template
from models import Note
from database import db_session


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    """
    Home
    """
    all_notes = [note.serialize() for note in  Note.query.all()]
    return render_template('index.html', notes=all_notes) 


@app.route('/notes', methods=['POST'])
def notes():
    """
    handler for /notes
    """
    data = request.data.decode('UTF-8')
    data = json.loads(data)
    if data:
        _save_note(data)
    return {'status': 'success'}               

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
