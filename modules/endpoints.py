from flask import Flask, request, jsonify
from modules import app, db
from modules.tables import Category, Product
import json
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime


@app.route('/create', methods=['POST'])
def create():
  try:
    name = request.json['name']
    price = request.json['price']
    expiry = request.json['expiry']
    category_id=request.json['category_id']

  except KeyError as e:      # key error for missing items
    return jsonify({"error":"missing"+str(e)}), 500

  if price <= 0.0:
    return jsonify({"error":"price must be > 0"}),400

  product = Product(name, price, expiry, category_id)

  try:
    product.new() # created in tables.py for add and commit

  except IntegrityError as e:

    if "violates unique constraint" in str(e):
      return jsonify({"error":name+" already exists"}),400
    elif "violates foreign key constraint" in str(e):
      return jsonify({"error":"category "+str(category_id)+ " is unavailable"}),404

  return jsonify({"msg":product.name+" is created"}),201



@app.route('/get', methods=['GET'])
def list():
  product=Product.Query()
  result=[]

  if request.data:
    category_id = request.json.get('category_id')
    sort = request.json.get('sort')
    order = request.json.get('order')

    if category_id:
      product=product.filter_by(category_id=category_id)

    if sort == "price":
      if order == "desc":
        product=product.order_by(Product.price.desc())
      else:
        product=product.order_by(Product.price)

    elif sort == "expiry":
      if order == "desc":
        product=product.order_by(Product.expiry.desc())
      else:
        product=product.order_by(Product.expiry)

  product=product.all()

  if not product:
    return jsonify({"error":"unavailable category"}),404

  for products in product:
    result.append([{"name":products.name,"price":products.price,"expiry":str(products.expiry),"category_id":products.category_id}])

  return jsonify(result),200

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
  print(id)
  try:
    product=Product.delete(id)
  except Exception as e:
    return jsonify([{'msg':"product is deleted"}]),200
  db.session.commit()
  return jsonify([{'msg':"product is deleted"}]),200


@app.route('/update/<id>', methods=['POST'])
def update(id):
  product = Product.query.get(id)

  if not product:
    return jsonify({"error":"product unavailable"}),404 # for wrong product id
  if request.data: # if request.body is not empty
    name = request.json.get('name',product.name)
    price = request.json.get('price',product.price)
    expiry = request.json.get('expiry',product.expiry)
    category_id= request.json.get('category_id',product.category_id)

    if price <= 0.0:
      return jsonify({"error":"price must be > 0"}),400

    try:
      product.name=name
      product.price=price
      product.expiry=expiry
      product.category_id=category_id
      product.save()

    except IntegrityError as e:
      if "violates unique constraint" in str(e):
        return jsonify({"error":name+" already exists"}),400
      elif "violates foreign key constraint" in str(e):
        return jsonify({"error":"category "+str(category_id)+ " is unavailable"}),404

    return jsonify([{'msg':"product is updated"}]),201
  return jsonify({'msg':'nothing to update'}),404

  @app.route('/',methods=['GET'])
  def welcome():
    return jsonify({"msg":"welcome"})
