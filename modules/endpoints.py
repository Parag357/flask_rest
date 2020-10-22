from flask import Flask, request, jsonify
from modules import app, db
from modules.tables import Category, Product
import json
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime
from psycopg2.errors import ForeignKeyViolation

def configure_routes(app):

  @app.route('/create', methods=['POST'])
  def create():
    try:
      name = request.json['name']
      price = request.json['price']
      expiry = request.json['expiry']
      category_id=request.json['category_id']

    except KeyError as e:      # key error for missing items
      return jsonify({"error":"missing"+str(e)}), 400

    if price <= 0.0:
      return jsonify({"error":"price must be > 0"}),400

    product = Product(name, price, expiry, category_id)


    try:
      db.session.add(product)
      db.session.commit()

    except IntegrityError as e:

      if "violates unique constraint" in str(e):
          return jsonify({"error":name+" already exists"}),400
      elif "violates foreign key constraint" in str(e):
          return jsonify({"error":"category "+str(category_id)+ " is unavailable"}),404

    return jsonify({"msg":product.name+" is created"}),201



  @app.route('/get', methods=['GET'])
  def list():

    category_id = request.json.get('category_id')
    sort = request.json.get('sort')
    order = request.json.get('order')

    result=[]

    product=Product.query

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
    try:
      product=Product.query.filter_by(id=id).delete()
    except:
      return jsonify([{'msg':"product is deleted"}]),404
    db.session.commit()
    return jsonify([{'msg':"product is deleted"}]),200


  @app.route('/update/<id>', methods=['POST'])
  def update(id):
    try:
      product = Product.query.get(id)

    except AttributeError as e:
      return jsonify({"error":"product unavailable"}),404 # for wrong product id

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
      db.session.commit()

    except IntegrityError as e:
      if "violates unique constraint" in str(e):
        return jsonify({"error":name+" already exists"}),400
      elif "violates foreign key constraint" in str(e):
          return jsonify({"error":"category "+str(category_id)+ " is unavailable"}),404

    return jsonify([{'msg':"product is updated"}]),201
