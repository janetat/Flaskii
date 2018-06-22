# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'Allen Secret Key'
USERNAME = 'admin'
PASSWORD = 'admin'

# create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)


# connect to database
def connect_db():
    """ Connects to the database. """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# get database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# init the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# close databse connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# Routes and view functions
@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    db = get_db()
    cur = db.execute('SELECT * FROM entries ORDER BY id DESC')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database."""
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute(
        'INSERT INTO entries (title, text) VALUES (?, ?)',
        [request.form['title'], request.form['text']]
    )
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run()



