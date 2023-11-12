from flask import jsonify, abort
from service.models import Product
from service.common import status
from . import app

# ... (previous code)

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

# ... (remaining code)
