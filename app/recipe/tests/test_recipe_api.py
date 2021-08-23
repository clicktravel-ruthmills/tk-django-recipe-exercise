from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe


RECIPES_URL = reverse('recipe:recipe-list')


class RecipeApiTest(TestCase):
    """Tests for the Recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe_with_no_ingredients(self):
        """Test creating a recipe with no ingredients"""
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven'
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients"""
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [
                {'name': 'dough'},
                {'name': 'cheese'},
                {'name': 'tomato'}
            ]
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
