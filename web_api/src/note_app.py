"""
Web Note API - Flask application for managing text highlights
"""
import json
from datetime import datetime
from functools import wraps

import flask
from flask import request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import and_, desc

from models import Note
from database import db_session, init_db, close_db_session
from config import current_config
from logger import app_logger


app = flask.Flask(__name__)
app.config.from_object(current_config)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[current_config.RATELIMIT_DEFAULT]
)

# Initialize database
with app.app_context():
    init_db()


# ============== Utility Functions ==============

def require_json(f):
    """Decorator to validate JSON request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_note_data(data):
    """Validate note data from request"""
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    
    required_fields = ['user_id', 'text', 'source']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    if len(data.get('text', '')) < 3:
        return False, "Text must be at least 3 characters"
    
    if len(data.get('user_id', '')) > 50:
        return False, "User ID too long"
    
    return True, None


def error_response(message, status_code=400):
    """Return standardized error response"""
    return jsonify({'error': message, 'status': 'error'}), status_code


def success_response(data=None, message='success', status_code=200):
    """Return standardized success response"""
    return jsonify({'status': 'success', 'message': message, 'data': data}), status_code


# ============== Routes ==============

@app.route('/', methods=['GET'])
@limiter.limit("5/second")
def home():
    """
    Home page - displays all non-deleted notes
    """
    try:
        page = request.args.get('page', 1, type=int)
        offset = (page - 1) * current_config.ITEMS_PER_PAGE
        
        notes = db_session.query(Note).filter(
            Note.deleted == False
        ).order_by(
            desc(Note.created_on)
        ).offset(offset).limit(current_config.ITEMS_PER_PAGE).all()
        
        total = db_session.query(Note).filter(Note.deleted == False).count()
        
        return render_template(
            'index.html',
            notes=[note.serialize() for note in notes],
            total=total,
            page=page,
            items_per_page=current_config.ITEMS_PER_PAGE
        )
    except Exception as e:
        app_logger.error(f"Error in home route: {str(e)}")
        return error_response("Internal server error", 500)


@app.route('/notes', methods=['POST'])
@limiter.limit(current_config.RATELIMIT_STRICT)
@require_json
def create_note():
    """
    Create a new note from POST request
    """
    try:
        data = request.get_json()
        is_valid, error_msg = validate_note_data(data)
        
        if not is_valid:
            app_logger.warning(f"Invalid note data: {error_msg}")
            return error_response(error_msg, 400)
        
        note = Note(
            user_id=data['user_id'],
            text=data['text'],
            source=data['source']
        )
        
        if 'tags' in data:
            note.tags = data['tags']
        if 'comments' in data:
            note.comments = data['comments']
        
        db_session.add(note)
        db_session.commit()
        
        app_logger.info(f"Note created: id={note.id}, user_id={note.user_id}")
        return success_response(note.serialize(), "Note created successfully", 201)
        
    except Exception as e:
        db_session.rollback()
        app_logger.error(f"Error creating note: {str(e)}")
        return error_response("Failed to create note", 500)


@app.route('/note/<int:note_id>', methods=['GET'])
@limiter.limit(current_config.RATELIMIT_STRICT)
def get_note(note_id):
    """
    Retrieve a specific note by ID
    """
    try:
        note = db_session.query(Note).filter(Note.id == note_id).first()
        
        if not note:
            app_logger.warning(f"Note not found: id={note_id}")
            return error_response("Note not found", 404)
        
        if note.deleted:
            return error_response("Note not found", 404)
        
        return success_response(note.serialize())
        
    except Exception as e:
        app_logger.error(f"Error retrieving note {note_id}: {str(e)}")
        return error_response("Internal server error", 500)


@app.route('/note/<int:note_id>', methods=['PUT'])
@limiter.limit(current_config.RATELIMIT_STRICT)
@require_json
def update_note(note_id):
    """
    Update a note's tags and comments
    """
    try:
        note = db_session.query(Note).filter(Note.id == note_id).first()
        
        if not note:
            return error_response("Note not found", 404)
        
        if note.deleted:
            return error_response("Cannot update deleted note", 400)
        
        data = request.get_json()
        
        if 'tags' in data:
            note.tags = data['tags']
        if 'comments' in data:
            note.comments = data['comments']
        
        note.modified_on = datetime.utcnow()
        db_session.commit()
        
        app_logger.info(f"Note updated: id={note_id}")
        return success_response(note.serialize(), "Note updated successfully")
        
    except Exception as e:
        db_session.rollback()
        app_logger.error(f"Error updating note {note_id}: {str(e)}")
        return error_response("Failed to update note", 500)


@app.route('/note/<int:note_id>', methods=['DELETE'])
@limiter.limit(current_config.RATELIMIT_STRICT)
def delete_note(note_id):
    """
    Soft delete a note (mark as deleted)
    """
    try:
        note = db_session.query(Note).filter(Note.id == note_id).first()
        
        if not note:
            return error_response("Note not found", 404)
        
        note.deleted = True
        note.modified_on = datetime.utcnow()
        db_session.commit()
        
        app_logger.info(f"Note deleted: id={note_id}")
        return success_response(note.serialize(), "Note deleted successfully")
        
    except Exception as e:
        db_session.rollback()
        app_logger.error(f"Error deleting note {note_id}: {str(e)}")
        return error_response("Failed to delete note", 500)


@app.route('/search', methods=['GET'])
@limiter.limit("5/second")
def search_notes():
    """
    Search notes by text and tags with pagination
    """
    try:
        search_text = request.args.get('text', '').strip()
        search_tags = request.args.get('tags', '').strip()
        page = request.args.get('page', 1, type=int)
        offset = (page - 1) * current_config.ITEMS_PER_PAGE
        
        query = db_session.query(Note).filter(Note.deleted == False)
        
        if search_text:
            search_text = f"%{search_text}%"
            query = query.filter(Note.text.ilike(search_text))
        
        if search_tags:
            tag_list = [tag.strip() for tag in search_tags.split(',')]
            query = query.filter(Note.tags.in_(tag_list))
        
        total = query.count()
        results = query.order_by(desc(Note.created_on)).offset(offset).limit(
            current_config.ITEMS_PER_PAGE
        ).all()
        
        app_logger.info(f"Search performed: text='{search_text}', tags='{search_tags}', results={len(results)}")
        
        return render_template(
            'index.html',
            notes=[note.serialize() for note in results],
            total=total,
            page=page,
            items_per_page=current_config.ITEMS_PER_PAGE,
            search_text=search_text,
            search_tags=search_tags
        )
        
    except Exception as e:
        app_logger.error(f"Error in search: {str(e)}")
        return error_response("Search failed", 500)


# ============== Error Handlers ==============

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    app_logger.warning(f"404 error: {request.path}")
    return error_response("Resource not found", 404)


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    app_logger.warning(f"400 error: {str(error)}")
    return error_response("Bad request", 400)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app_logger.error(f"500 error: {str(error)}")
    return error_response("Internal server error", 500)


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    app_logger.warning(f"Rate limit exceeded: {request.remote_addr}")
    return error_response("Rate limit exceeded. Please try again later", 429)


# ============== Request/Response Handlers ==============

@app.before_request
def log_request():
    """Log incoming requests"""
    app_logger.debug(f"{request.method} {request.path}")


@app.after_request
def add_cors_headers(response):
    """Add CORS headers to all responses"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Clean up database session"""
    close_db_session()


if __name__ == '__main__':
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=current_config.DEBUG,
            use_reloader=current_config.DEBUG
        )
    except KeyboardInterrupt:
        app_logger.info("Application shutdown")
    except Exception as e:
        app_logger.error(f"Application error: {str(e)}")
        raise
