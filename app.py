from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
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


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
