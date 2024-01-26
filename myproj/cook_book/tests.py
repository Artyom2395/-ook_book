
from django.test import TestCase, Client
from cook_book.models import Product, Recipe

class RecipeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Творог", times_used=0)
        self.recipe = Recipe.objects.create(name="Сырник")

    def test_add_product_to_recipe(self):
        response = self.client.get('/add_product_to_recipe/', {
            'recipe_id': self.recipe.id,
            'product_id': self.product.id,
            'weight': 200
        })
        self.assertEqual(response.status_code, 200)
