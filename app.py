from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'torrent'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


class RegisterForm(Form):
    login = StringField('Login', [
        validators.DataRequired(),
        validators.Length(min=5, max=25)])
    email = StringField('Email', [
        validators.DataRequired(),
        validators.Length(min=6, max=75)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# Register form class
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        active = 1

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(login, email, password, active) VALUES(%s, %s, %s, %s)", (login, email, password, active))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        redirect(url_for('index'))
    return render_template('register.html', form=form)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        login = request.form['login']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM user WHERE login = %s", [login])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['login'] = login
                return redirect(url_for('dashboard'))
            else:
                error = 'Username or password did not match'
                cur.close()
                return render_template('login.html', error=error)
        else:
            error = 'Username or password did not match'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unathorized access denied', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
