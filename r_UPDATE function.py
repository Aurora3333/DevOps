from flask import jsonify, request, abort
from service.models import Product
from service.common import status
from . import app

# ... (previous code)

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

# ... (remaining code)
