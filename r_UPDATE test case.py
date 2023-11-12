import os
import logging
from decimal import Decimal
from unittest import TestCase
from service import app
from service.common import status
from service.models import db, init_db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/products"

class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        # ... (same as before)

    def test_update_product(self):
        """It should update an existing product"""
        product = self._create_products()[0]

        # Update the product data
        new_product_data = {
            "name": "Updated Product",
            "description": "A much better product",
            "price": 99.99,
            "available": False,
        }

        # Update the product
        response = self.client.put(f"{BASE_URL}/{product.id}", json=new_product_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the updated product
        retrieved_product = response.get_json()

        # Check the updated product data
        self.assertEqual(retrieved_product["id"], product.id)
        self.assertEqual(retrieved_product["name"], "Updated Product")
        self.assertEqual(retrieved_product["description"], "A much better product")
        self.assertEqual(retrieved_product["price"], 99.99)
        self.assertEqual(retrieved_product["available"], False)
