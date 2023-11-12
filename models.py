import logging
from enum import Enum
from decimal import Decimal
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def initialize_db(app):
    """Initialize the SQLAlchemy app"""
    ModProduct.initialize_db(app)


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class ProductCategory(Enum):
    """Enumeration of valid Product Categories"""

    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class ModProduct(db.Model):
    """
    Class that represents a Modified Product

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object-relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(250), nullable=False)
    cost = db.Column(db.Numeric, nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(
        db.Enum(ProductCategory),
        nullable=False,
        server_default=(ProductCategory.UNKNOWN.name),
    )

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return f"<ModProduct {self.title} id=[{self.id}]>"

    def create(self):
        """Creates a Modified Product in the database"""
        logger.info("Creating %s", self.title)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Modified Product in the database"""
        logger.info("Saving %s", self.title)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Modified Product from the data store"""
        logger.info("Deleting %s", self.title)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes a Modified Product into a dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "cost": str(self.cost),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data: dict):
        """Deserializes a Modified Product from a dictionary"""
        try:
            self.title = data["title"]
            self.details = data["details"]
            self.cost = Decimal(data["cost"])
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
            self.category = getattr(ProductCategory, data["category"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid product: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data " + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def initialize_db(cls, app: Flask):
        """Initializes the database session"""
        logger.info("Initializing database")
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls) -> list:
        """Returns all of the Modified Products in the database"""
        logger.info("Processing all Modified Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """Finds a Modified Product by its ID"""
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Modified Products with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.title == name)

    @classmethod
    def find_by_price(cls, price: Decimal) -> list:
        """Returns all Modified Products with the given price"""
        logger.info("Processing price query for %s ...", price)
        price_value = price
        if isinstance(price, str):
            price_value = Decimal(price.strip(' "'))
        return cls.query.filter(cls.cost == price_value)

    @classmethod
    def find_by_availability(cls, available: bool = True) -> list:
        """Returns all Modified Products by their availability"""
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_category(cls, category: ProductCategory = ProductCategory.UNKNOWN) -> list:
        """Returns all Modified Products by their Category"""
        logger.info("Processing category query for %s ...", category.name)
        return cls.query.filter(cls.category == category)
