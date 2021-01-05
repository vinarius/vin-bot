import requests
import json
import os
import random

from mysecrets import SPOONACULAR_API_KEY

class Food_Commands:
    def getRecipe(self, message=None):
        try:
            script_path = os.path.dirname(__file__)
            json_file = os.path.join(script_path, '../api-info.json')
            with open(json_file, 'r') as apiH:
                api = json.loads(apiH.read())
                pass
            complex_search_uri = '{base_uri}{api_key}'.format(
                base_uri = api['food']['get']['complexSearch'],
                api_key = SPOONACULAR_API_KEY
            )
            recipe_metadata = requests.get(complex_search_uri)
            recipe_metadata = recipe_metadata.json()

            instructions = {
                'result': ''
            }

            random_index = random.randrange(0, len(recipe_metadata['results']))
            instructions['id'] = recipe_metadata['results'][random_index]['id']
            instructions['title'] = recipe_metadata['results'][random_index]['title']
            instructions['image'] = recipe_metadata['results'][random_index]['image']

            instructions['result'] = '{title}\n\n'.format(**instructions)

            ingredientsUri = '{base_uri}{api_key}'.format(
                base_uri = api['food']['get']['ingredients'],
                api_key = SPOONACULAR_API_KEY
            ).replace('__id__', str(instructions['id']))

            ingredients_response = requests.get(ingredientsUri)
            ingredients_response = ingredients_response.json()
            instructions['ingredients'] = ingredients_response['ingredients']

            instructions['result'] = '{result}Ingredients:\n'.format(**instructions)
            hyphen_count = len('ingredients')
            hyphen_line = ''
            for index in range(hyphen_count):
                hyphen_line = hyphen_line + '-'
            instructions['result'] = '{result}{hyphen_line}\n'.format(
                result=instructions['result'],
                hyphen_line=hyphen_line
            )

            for ingredient in instructions['ingredients']:
                formatted_ingredient = '{value} {unit} {name}'.format(
                    value = ingredient['amount']['us']['value'],
                    unit = ingredient['amount']['us']['unit'],
                    name = ingredient['name']
                )

                instructions['result'] = '{result}{new_ingredient}\n'.format(
                    result=instructions['result'],
                    new_ingredient=formatted_ingredient
                )

            instructions['result'] = '{result}\nInstructions:\n'.format(**instructions)

            analyzedInstructionsUri = '{base_uri}{api_key}'.format(
                base_uri = api['food']['get']['analyzedInstructions'],
                api_key = SPOONACULAR_API_KEY
            ).replace('__id__', str(instructions['id']))

            instruction_steps_response = requests.get(analyzedInstructionsUri)
            instruction_steps_response = instruction_steps_response.json()
            instruction_steps_response = instruction_steps_response[0]

            for step in instruction_steps_response['steps']:
                formatted_step = '{step_number}. {text}'.format(
                    step_number = step['number'],
                    text = step['step']
                )
                instructions['result'] = '{result}{new_step}\n'.format(
                    result = instructions['result'],
                    new_step = formatted_step
                )
            
            return instructions
        except Exception as error:
            print(error)
            return {
                'result': 'oops, something went wrong',
                'image': ''
            }
