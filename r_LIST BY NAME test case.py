from flask import jsonify, request, abort
from flask import url_for  # noqa: F401 pylint: disable=unused-import
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import app


# ... (Existing code for healthcheck, index, and utility functions)


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based on the data in the body that is posted
    """
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")

    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product = Product()
    product.deserialize(data)
    product.create()
    app.logger.info("Product with new id [%s] saved!", product.id)

    message = product.serialize()

    # Uncomment this line of code once you implement READ A PRODUCT
    # location_url = url_for("get_products", product_id=product.id, _external=True)
    location_url = "/"  # delete once READ is implemented
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def get_all_products():
    """
    Lists all products
    This endpoint will return a list of all products.
    """
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])


######################################################################
# LIST PRODUCTS BY NAME
######################################################################
@app.route("/products/name/<string:name>", methods=["GET"])
def get_products_by_name(name):
    """
    Lists all products by name
    This endpoint will return a list of all products that match the given name.
    """
    products = Product.query.filter_by(name=name).all()
    return jsonify([product.serialize() for product in products])


######################################################################
# LIST PRODUCTS BY CATEGORY
######################################################################
@app.route("/products/category/<string:category>", methods=["GET"])
def get_products_by_category(category):
    """
    Lists all products by category
    This endpoint will return a list of all products that match the given category.
    """
    products = Product.query.filter_by(category=category).all()
    return jsonify([product.serialize() for product in products])


######################################################################
# LIST PRODUCTS BY AVAILABILITY
######################################################################
@app.route("/products/availability/<bool:availability>", methods=["GET"])
def get_products_by_availability(availability):
    """
    Lists all products by availability
    This endpoint will return a list of all products that match the given availability.
    """
    products = Product.query.filter_by(available=availability).all()
    return jsonify([product.serialize() for product in products])


######################################################################
# UPDATE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Updates a specific product by ID
    This endpoint will update the details of a product based on its ID.
    """
    check_content_type("application/json")
    data = request.get_json()

    product = Product.query.get(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND)

    product.deserialize(data)
    product.update()

    return jsonify(product.serialize())


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Deletes a specific product by ID
    This endpoint will delete a product based on its ID.
    """
    product = Product.query.get(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND)

    product.delete()

    return jsonify(status="Product deleted")
