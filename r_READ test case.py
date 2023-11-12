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

    def test_read_product(self):
        """It should retrieve a product by its ID"""
        product = self._create_products()[0]

        # Get the product by ID
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the returned product data
        retrieved_product = response.get_json()
        self.assertEqual(retrieved_product["id"], product.id)
        self.assertEqual(retrieved_product["name"], product.name)
        self.assertEqual(retrieved_product["description"], product.description)
        self.assertEqual(retrieved_product["price"], product.price)
        self.assertEqual(retrieved_product["available"], product.available)
        self.assertEqual(retrieved_product["category"], product.category.name)
