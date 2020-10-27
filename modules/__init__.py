from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

	
app=Flask(__name__) #app initialistaion
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/inventory'
app.config["SQLALCHEMY_ECHO"] = True
db=SQLAlchemy(app)


from modules import endpoints