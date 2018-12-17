from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://blablabox:passw@localhost:5432/payment'
app.config['SQLALCHEMY_ECHO'] = True