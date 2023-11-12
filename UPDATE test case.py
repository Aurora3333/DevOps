import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    # Test the UPDATE endpoint
    def test_update_product(self):
        """It should update an existing product"""
        product = ProductFactory()
        product.create()

        updated_product = Product.query.get(product.id)
        updated_product.name = "Updated Fedora"
        updated_product.description = "A stylish red hat"
        updated_product.price = 15.00
        updated_product.available = False
        updated_product.update()

        # Fetch the updated product and assert that the changes were made
        fetched_product = Product.query.get(product.id)
        self.assertEqual(fetched_product.name, "Updated Fedora")
        self.assertEqual(fetched_product.description, "A stylish red hat")
        self.assertEqual(Decimal(fetched_product.price), 15.00)
        self.assertEqual(fetched_product.available, False)


# If you have other test methods in your file, they would go here.

if __name__ == "__main__":
    unittest.main()
