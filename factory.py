import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product, Category


class ModProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""

        model = Product

    title = factory.Faker("name")
    details = factory.Faker("text")
    cost = FuzzyDecimal(50, 800)
    product_category = factory.SubFactory(ModCategoryFactory)

    def create(self):
        """Creates a fake product and returns it"""

        product = Product(
            title=self.title,
            details=self.details,
            cost=self.cost,
            product_category=self.product_category,
        )
        product.save()
        return product


class ModCategoryFactory(factory.Factory):
    """Creates fake categories for testing"""

    class Meta:
        """Maps factory to data model"""

        model = Category

    category_name = factory.Faker("name")

    def create(self):
        """Creates a fake category and returns it"""

        category = Category(category_name=self.category_name)
        category.save()
        return category
