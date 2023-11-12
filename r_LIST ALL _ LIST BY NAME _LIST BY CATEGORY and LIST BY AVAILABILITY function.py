from flask import jsonify, request, abort
from . import app
from service.models import Product
from service.common import status

# ... (previous code)

@app.route("/products", methods=["GET"])
def get_products():
    """
    Lists all products
    This endpoint will return a list of all products.
    """

    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@app.route("/products/name/<string:name>", methods=["GET"])
def get_products_by_name(name):
    """
    Lists all products by name
    This endpoint will return a list of all products that match the given name.
    """

    products = Product.query.filter_by(name=name).all()
    return jsonify([product.serialize() for product in products])

@app.route("/products/category/<string:category>", methods=["GET"])
def get_products_by_category(category):
    """
    Lists all products by category
    This endpoint will return a list of all products that match the given category.
    """

    products = Product.query.filter_by(category=category).all()
    return jsonify([product.serialize() for product in products])

@app.route("/products/availability/<bool:availability>", methods=["GET"])
def get_products_by_availability(availability):
    """
    Lists all products by availability
    This endpoint will return a list of all products that match the given availability.
    """

    products = Product.query.filter_by(available=availability).all()
    return jsonify([product.serialize() for product in products])
