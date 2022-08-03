from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField


app = Flask(__name__)
cnx = mysql.connector.connect(user="Jack", password="Zangetsu88", host="dbiownit.mysql.database.azure.com", port=3306, database=" dbiownit.mysql.database.azure.com", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)

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
        return render_template('signin.html', form = form, username=username)
    else:
        return render_template('home.html', form = form, username="")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
