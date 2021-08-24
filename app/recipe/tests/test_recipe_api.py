from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient


RECIPES_URL = reverse('recipe:recipe-list')


def _create_pizza_recipe(self):
    payload = {
        'name': 'Pizza',
        'description': 'Put it in the oven',
        'ingredients': [
            {'name': 'dough'},
            {'name': 'cheese'},
            {'name': 'tomato'}
        ]
    }
    res = self.client.post(RECIPES_URL, data=payload, format='json')
    return res


def _create_cheeseburger_recipe(self):
    payload = {
        'name': 'Cheeseburger',
        'description': 'Buy it from McDonalds',
        'ingredients': [
            {'name': 'beef patty'},
            {'name': 'cheese'},
            {'name': 'burger bun'},
            {'name': 'gherkin'}
        ]
    }
    res = self.client.post(RECIPES_URL, data=payload, format='json')
    return res


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def search_url(name):
    """Return recipe search URL"""
    return reverse('recipe:recipe-list') + f'?name={name}'


class RecipeApiTest(TestCase):
    """Tests for the Recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe_with_no_ingredients(self):
        """Test creating a recipe with no ingredients fails"""
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven'
        }
        res = self.client.post(RECIPES_URL, data=payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients is successful"""
        res = _create_pizza_recipe(self)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(getattr(recipe, 'name'), 'Pizza')
        self.assertEqual(
            getattr(recipe, 'description'), 'Put it in the oven'
        )
        ingredients = Ingredient.objects.filter(recipe=res.data['id'])
        self.assertEqual(len(ingredients), 3)
        for ingredient in ingredients:
            self.assertIn(
                getattr(ingredient, 'name'), 'dough cheese tomato'
            )

    def test_retrieving_all_recipes(self):
        """Test retrieving all recipes"""
        createResponse = _create_pizza_recipe(self)

        listResponse = self.client.get(RECIPES_URL)

        self.assertEqual(listResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listResponse.data), 1)
        recipe = listResponse.data[0]

        self.assertEqual(createResponse.data['id'], recipe['id'])
        self.assertEqual(createResponse.data['name'], recipe['name'])
        self.assertEqual(
            createResponse.data['description'], recipe['description']
        )
        self.assertEqual(
            createResponse.data['description'],
            recipe['description']
        )
        ingredients = recipe['ingredients']
        for ingredient in ingredients:
            self.assertIn(
                ingredient['name'], 'dough cheese tomato'
            )

    def test_retrieving_single_recipe_by_id(self):
        """Test retrieving a single recipe by ID"""
        createResponse = _create_pizza_recipe(self)
        recipe_id = createResponse.data['id']

        retrieveResponse = self.client.get(detail_url(recipe_id))

        self.assertEqual(retrieveResponse.status_code, status.HTTP_200_OK)
        recipe = retrieveResponse.data

        self.assertEqual(createResponse.data['id'], recipe['id'])
        self.assertEqual(createResponse.data['name'], recipe['name'])
        self.assertEqual(
            createResponse.data['description'], recipe['description']
        )
        self.assertEqual(
            createResponse.data['description'],
            recipe['description']
        )
        ingredients = recipe['ingredients']
        for ingredient in ingredients:
            self.assertIn(
                ingredient['name'], 'dough cheese tomato'
            )

    def test_updating_a_recipe(self):
        """Test updating a recipe"""
        createResponse = _create_pizza_recipe(self)
        recipe_id = createResponse.data['id']

        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [
                {'name': 'casa-tarradellas'}
            ]
        }
        updateResponse = self.client.patch(
            detail_url(recipe_id),
            data=payload,
            format='json'
        )

        self.assertEqual(updateResponse.status_code, status.HTTP_200_OK)

        retrieveResponse = self.client.get(detail_url(recipe_id))

        self.assertEqual(retrieveResponse.status_code, status.HTTP_200_OK)
        recipe = retrieveResponse.data

        self.assertEqual(createResponse.data['id'], recipe['id'])
        self.assertEqual(createResponse.data['name'], recipe['name'])
        self.assertEqual(
            createResponse.data['description'], recipe['description']
        )
        self.assertEqual(
            createResponse.data['description'],
            recipe['description']
        )
        ingredients = recipe['ingredients']
        for ingredient in ingredients:
            self.assertIn(
                ingredient['name'], 'casa-tarradellas'
            )
            self.assertNotIn(
                ingredient['name'], 'dough cheese tomato'
            )

    def test_searching_for_a_recipe_by_name_matches(self):
        """Test searching for a recipe by name where the recipe matches"""
        createResponse = _create_pizza_recipe(self)

        searchResponse = self.client.get(search_url('Pi'))

        self.assertEqual(searchResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(len(searchResponse.data), 1)
        recipe = searchResponse.data[0]

        self.assertEqual(createResponse.data['id'], recipe['id'])
        self.assertEqual(createResponse.data['name'], recipe['name'])
        self.assertEqual(
            createResponse.data['description'], recipe['description']
        )
        self.assertEqual(
            createResponse.data['description'],
            recipe['description']
        )
        ingredients = recipe['ingredients']
        for ingredient in ingredients:
            self.assertIn(
                ingredient['name'], 'dough cheese tomato'
            )

    def test_searching_for_a_recipe_by_name_no_match(self):
        """Test searching for a recipe by name where there is no match"""
        _create_pizza_recipe(self)

        searchResponse = self.client.get(search_url('Kebab'))

        self.assertEqual(searchResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(len(searchResponse.data), 0)

    def test_deleting_a_recipe(self):
        """Test deleting a recipe"""
        pizzaCreateResponse = _create_pizza_recipe(self)
        pizza_recipe_id = pizzaCreateResponse.data['id']

        cheeseburgerCreateResponse = _create_cheeseburger_recipe(self)
        cheeseburger_recipe_id = cheeseburgerCreateResponse.data['id']

        pizzaDeleteResponse = self.client.delete(detail_url(pizza_recipe_id))
        self.assertEqual(
            pizzaDeleteResponse.status_code, status.HTTP_204_NO_CONTENT
        )

        pizzaRetrieveResponse = self.client.get(detail_url(pizza_recipe_id))

        self.assertEqual(
            pizzaRetrieveResponse.status_code, status.HTTP_404_NOT_FOUND
        )

        cheeseburgerRetrieveResponse = self.client.get(
            detail_url(cheeseburger_recipe_id)
        )

        self.assertEqual(
            cheeseburgerRetrieveResponse.status_code, status.HTTP_200_OK
        )
