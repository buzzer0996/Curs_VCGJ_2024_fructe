import os
import json
from flask import Flask, request, jsonify, abort, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import exc

from .database.models import db_drop_and_create_all, setup_db, Fruct
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Adaugă cheia secretă
setup_db(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    """Add CORS headers to the response."""
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

# Uncomment to drop and create database tables
# db_drop_and_create_all()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if username == 'buzzer0996' and password == '****************************************':
            return redirect(url_for('get_fructe'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

# ROUTES
@app.route('/fructe', methods=['GET'])
def get_fructe():
    """Retrieve all fruits."""
    fructe = Fruct.query.all()
    if not fructe:
        abort(404)

    return jsonify({
        'success': True,
        'fructe': [fruct.short() for fruct in fructe]
    }), 200

@app.route('/fructe', methods=['POST'])
@requires_auth('post:fructe')
def create_fructe(jwt):
    """Create a new fruit entry."""
    body = request.get_json()
    if not body:
        abort(400)

    title = body.get('title')
    color = body.get('color')
    parts = body.get('parts')
    description = body.get('description')

    if not title or not color or parts is None:
        abort(400)

    fruct = Fruct(title=title, color=color, parts=parts, description=description)
    try:
        fruct.insert()
    except Exception as e:
        print(e)
        abort(422)

    return jsonify({
        'success': True,
        'fructe': [fruct.long()]
    }), 201
    
@app.route('/logout')
def logout():
    # Aici poți adăuga logica de logout, cum ar fi ștergerea sesiunii.
    # De exemplu:
    # session.pop('user', None)  # Dacă folosești sesiuni

    return redirect(url_for('login'))  # Redirecționare la pagina de autentificare


# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Permission not allowed'
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
    }), 422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server error'
    }), 500

