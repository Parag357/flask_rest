from datetime import date,datetime 
from modules import db



class Category(db.Model): # tables
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  product=db.relationship('Product',backref='category',lazy=True) # we use the value of backref in 'many side' i.e. Product to get the category of the product.
    #lazy=True means sqlalchemy will load the data from db at one go
  def __init__(self, name):
    self.name = name

  def __repr__(self): # used to decide how the object will be printed
    return self.name




class Product(db.Model): # tables
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True, nullable=False)
  price = db.Column(db.Float, nullable=False)
  expiry = db.Column(db.Date, nullable=False)# mm/dd/yyyy format
  category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)


  def __init__(self, name, price,expiry,category_id):
    self.name = name
    self.price = price
    self.expiry=expiry
    self.category_id=category_id

  def __repr__(self): # used to decide how the object will be printed
    return str({'name':self.name,'price':self.price,'expiry':self.expiry})
