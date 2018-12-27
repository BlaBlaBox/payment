import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

url = os.getenv("DATABASE_URL")
if url is None:
    url = os.getenv("DATABASE_URL_ANNO")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# "postgres://tqvclqfetowjot:cd47f43ff1d9dd9fe50862579fcea7321f1347a17d674f0bee66f56e6bfa94c0@ec2-54-247-125-116.eu-west-1.compute.amazonaws.com:5432/do29nfies91h4"
