"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

# Starting app in venu
. venv/bin/activate


This file creates your application.
"""
import sys, os
sys.dont_write_bytecode = True

from flask import Flask, render_template
from call.module import User, mod_call_db as db
app = Flask(__name__)
#app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'x6dgbjldprk3lm52')

@app.route('/')
def home():
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
    admin = User.query.with_entities(User.id, User.username, User.email)
    #admin = User.query.order_by(User.id.asc()).limit(10).all()
    #admin = User.query.filter(User.email.endswith('@example.com')).order_by(User.id.asc())
    #admin = User.query.filter(User.email.startswith('guest')).order_by(User.id.asc())
    return render_template('load.html', admin=admin)

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
