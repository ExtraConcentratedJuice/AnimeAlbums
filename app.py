from flask import Flask, request, session, url_for, redirect, \
render_template, abort, g, flash, _app_ctx_stack
from flask_login import LoginManager, UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import sha256
import wtforms
import dbhandler
import re

app = Flask(__name__)
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = app.config['SECRET_KEY']

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/createalbum', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        try:
            if not session['logged_in']:
                return 'You are not logged in.'
        except:
            return 'You are not logged in.'
        
        n = request.form['name']
        d = request.form['description']

        if not (len(n) > 4 and len(n) < 70):
            flash('Name length must be between 4 and 70 characters.')
            return render_template('createalbum.html')

        if not (len(d) < 350):
            flash('Your description must be less than 350 characters long.')
            return render_template('createalbum.html')

        if dbhandler.create_new_album(n, d, session['id']):
            return render_template('success.html', action='createalbum', redirect=True, url='/')
        else:
            flash('Failed to create album.')
            return render_template('createalbum.html')
    else:
        try:
            if not session['logged_in']:
                return render_template('login.html')
        except:
            return render_template('login.html')
        
        return render_template('createalbum.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
      if request.method == 'POST':
            u = request.form['username']
            p = request.form['password']
            
            data = dbhandler.fetch_user(u)
            
            if not data:
                  flash('Invalid login.')
                  return render_template('login.html', login_page=True)

            if check_password_hash(data[0].replace('\n', ''), p):
                  session['logged_in'] = True
                  session['id'] = data[1]
                  session['username'] = data[2]
                  return render_template('success.html', action='login', redirect=True, url='/')
            else:
                  flash('Invalid login.')
                  return render_template('login.html', login_page=True)
                  
      else:
            return render_template('login.html', login_page=True)

@app.route('/logout')
def logout():
    try:
        if session['logged_in']:
            session.clear()
            return render_template('success.html', action='logout', redirect=True, url='/')
    except:
        return render_template('success.html', redirect=True, url='/')
    return render_template('success.html', redirect=True, url='/')

@app.route('/register', methods=['GET', 'POST'])
def register():
      if request.method == 'POST':
            u = request.form['username']
            p = request.form['password']
            c = request.form['confirm-password']
            e = request.form['email']

            if not (len(u) > 3 and len(u) < 20):
                  flash('Invalid username. Min length (3), max length (20)')
                  return render_template('register.html')
            
            if not (len(p) > 7):
                  flash('Invalid password. Your password must be at least 8 characters long.')
                  return render_template('register.html')

            if not (p == c):
                  flash('Your password and it\'s confirmation do not match.')
                  return render_template('register.html')

            reg = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

            if not reg.search(e):
                  flash('Invalid email.')
                  return render_template('register.html')

            p = generate_password_hash(p)

            if not dbhandler.create_new_user(u, p, e):
                  flash('That username is taken!')
                  return render_template('register.html')

            return render_template('success.html', action='register', username=u, redirect=True, url='/')
      else:
            return render_template('register.html')

@app.route('/users')
def userpage():
      users = dbhandler.get_users()
      return render_template('users.html', users=users)

@app.route('/logged')
def logged():
      if session.get('logged_in'):
            return 'yes'
      else:
            return 'no'

