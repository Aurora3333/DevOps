from flask import jsonify, request, abort
from flask import url_for  # noqa: F401 pylint: disable=unused-import
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import app

# ... (previous code)

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieves a specific product by ID
    This endpoint will return the details of a product based on its ID.
    """

    product = Product.query.get(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND)
    return jsonify(product.serialize())

# ... (remaining code)
