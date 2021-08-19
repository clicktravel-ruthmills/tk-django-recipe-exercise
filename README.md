# tk-django-recipe-exercise
## TK Django Recipe Exercise

Create a CRUD API with Django and DRF that allows you to CRUD recipes and add/delete ingredients to it.

Create automated tests for every action similar to https://slides.com/israelsaetaperez/test-driven-development/#/5/1

Recipe: Name, Description

Ingredient: Name, Recipe (ForeignKey) ← assume a given ingredient belongs only to one recipe, even if that means multiple Ingredient instances with the exact same name

## Example JSON response when GET /recipes/1/
    {
      “id”: 1,
      “name”: “Pizza”,
      “description”: “Put it in the oven”,
      “ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
    }

## Example recipe creation
### POST /recipes/
    {
      “name”: “Pizza”,
      “description”: “Put it in the oven”,
      “ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
    }

### Response:
    {
      “id”: 1,
      “name”: “Pizza”,
      “description”: “Put it in the oven”,
      “ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
    }

## Example recipe list
### GET /recipes/
    [
      {
        “id”: 1,
        “name”: “Pizza”,
        “description”: “Put it in the oven”,
        “ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
      }
    ]

### Add search view by name substring:
### GET /recipes/?name=Pi
    [
      {
        “id”: 1,
        “name”: “Pizza”,
        “description”: “Put it in the oven”,
        “ingredients”: [{“name”: “dough”}, {“name”: “cheese”}, {“name”: “tomato”}]
      }
    ]

## Example recipe edit
### PATCH /recipes/1/
    {
      “name”: “Pizza”,
      “description”: “Put it in the oven”,
      “ingredients”: [{“name”: “casa-tarradellas”}]
    }

Should delete the previous existing ingredients and put “casa-tarradellas” as only ingredient for recipe.

### Response:
    {
      “id”: 1,
      “name”: “Pizza”,
      “description”: “Put it in the oven”,
      “ingredients”: [{“name”: “casa-tarradellas”}]
    }

## Example recipe delete
### DELETE /recipes/1/

### Response:
### HTTP 204 (NO CONTENT)

Should delete the targeted recipe AND its ingredients.
