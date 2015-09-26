"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import sys, os
sys.dont_write_bytecode = True

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage/test.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'x6dgbjldprk3lm52')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def home():
    from app import db
    db.create_all()
    admin = User('justin', '2@example.com')
    guest = User('paul', '3@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    """Render website's home page."""
    return render_template('home.html')

@app.route('/load')
def load():
    users = User.query.all()
    test = "paul"
    admin = User.query.filter_by(username='admin').first()
    return render_template('load.html', user=admin, test=test)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.template_global(name='zip')
def _zip(*args, **kwargs):  # to not overwrite builtin zip in globals
    return __builtins__.zip(*args, **kwargs)

if __name__ == '__main__':
    app.run(debug=True)
