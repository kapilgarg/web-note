"""
"""
import json
from os import abort
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
    if request.method == 'POST':
        data = request.data.decode('UTF-8')
        data = json.loads(data)
        if data:
            db.save(data)
        return {
            'status':'success'
        }
    else:
        return {
            'status' : 'success',
            'data' : get_all()
        }        

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

def get_all(limit, offset):
    return db.get_all(limit, offset)



app.run()