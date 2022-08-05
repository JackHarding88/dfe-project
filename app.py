from os import environ
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from application import app

app = Flask(__name__)
cnx = mysql.connector.connect(user="Jack", password="{your_password}", host="dbiownit.mysql.database.azure.com", port=3306, database="{your_database}", ssl_ca="{ca-cert filename}", ssl_disabled=False)

app.config['SECRET_KEY']='SOME_KEY'

class UserCheck:
    def __init__(self, banned, message=None):
        self.banned = banned
        if not message:
            message = 'Please choose another username'
        self.message = message

    def __call__(self, form, field):
        if field.data.lower() in (word.lower() for word in self.banned):
            raise ValidationError(self.message)

class myForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        UserCheck(message="That username is not allowed", banned = ['root','admin','sys']),
        Length(min=2,max=15)
        ])
    submit = SubmitField('Sign up')

db.create_all()

@app.route('/', methods=['GET','POST'])
def postName():
    form = myForm()
    if form.validate_on_submit():
        username = form.username.data
        return render_template('add.html', form = form, username=username)
    else:
        return render_template('home.html', form = form, username="")
    
    @app.route('/add')
def add():
    new_game = Games(name="New Game")
    db.session.add(new_game)
    db.session.commit()
    return "Added new game to database"

@app.route('/read')
def read():
    all_games = Games.query.all()
    games_string = ""
    for game in all_games:
        games_string += "<br>"+ game.name
    return games_string

@app.route('/update/<name>')
def update(name):
    first_game = Games.query.first()
    first_game.name = name
    db.session.commit()
    return first_game.name

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
