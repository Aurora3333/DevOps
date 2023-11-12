import os
import logging
from decimal import Decimal
from unittest import TestCase
from service import app
from service.common import status
from service.models import db, init_db, Product
from tests.factories import ProductFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
# logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/products"

######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    # ... (other setup and teardown methods)

    # Test the LIST BY CATEGORY endpoint
    def test_list_products_by_category(self):
        """It should retrieve a list of products by category"""
        # Create some test products with different categories
        products_category1 = self._create_products(count=2)
        products_category2 = self._create_products(count=2)

        # Get the list of products for category 1
        response = self.client.get(f"{BASE_URL}/category/{products_category1[0].category.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that products for category 1 are returned
        product_list_category1 = response.get_json()
        self.assertEqual(len(product_list_category1), 2)

        # Check that the returned product names match the created ones for category 1
        for i, product in enumerate(products_category1):
            self.assertEqual(product_list_category1[i]["name"], product.name)

        # Get the list of products for category 2
        response = self.client.get(f"{BASE_URL}/category/{products_category2[0].category.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that products for category 2 are returned
        product_list_category2 = response.get_json()
        self.assertEqual(len(product_list_category2), 2)
