from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from marshmallow import Schema, fields
#from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
#import os



app=Flask(__name__) #app initialistaion
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/inventory'
app.config["SQLALCHEMY_ECHO"] = True
db=SQLAlchemy(app)



from modules import endpoints