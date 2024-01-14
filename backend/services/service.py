import json
import requests
import base64
from openai import OpenAI

class Service:
    def requestGPT4(self, base64_image, api_key):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Can you give me the items with the prices next to it?",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 300,
        }

        # gpt4_response received
        gpt4_response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )

        # Check the status code and handle errors
        if gpt4_response.status_code == 200:
            # The request was successful, return the response content
            print("gpt4 response success")
            return gpt4_response
        else:
            return "Error"
        
    def encodeImage(self, uploaded_image):
        # image read
        image_data = uploaded_image.read()
        print("image read")

        #image encoded
        base64_image = base64.b64encode(image_data).decode("utf-8")

        return base64_image
    
    def requestGPT3(self, listed_food, api_key):
        
        client = OpenAI(api_key=api_key)
        
        #gpt3_response received
        gpt3_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to output JSON.",
                },
                {
                    "role": "user",
                    "content": f"Please help me convert this response into JSON, where it is organized by groceryItems, name, price, and unit: {listed_food}",
                },
            ],
        )

        data = json.loads(gpt3_response.json())

        #gpt3_response parsed (content extracted)
        message_content = data["choices"][0]["message"]["content"]
        
        print("gpt3 response success")
        return json.loads(message_content)
    
    def extractNames(self, message_content):
        # parsed gpt3_response's names are extracted and appended
        names = ''
        for recipe in message_content.get('groceryItems', []):
            names += recipe.get('name', '') + ','

        names = names.rstrip(',')
        
        return names
    
    def requestSpoonacular(self, names, spoon_key, spoon_endpoint):
        parameters = {
            'ingredients': names,
            'apiKey': spoon_key,
            'ignorePantry': False
        }

        # Spoonacular response parsed
        spoon_response = requests.get(f'{spoon_endpoint}', params=parameters)
        spoon_data = spoon_response.json()

        sorted_recipes = sorted(spoon_data, key=lambda x: x.get('missedIngredientCount', 0), reverse=False)
        
        return sorted_recipes
    
    def templateRecipes(self, top_recipes, spoon_key):
        recipes_list = []
        desired_nutrition = ['Calories', 'Protein', 'Fiber', 'Fat', 'Carbohydrates', 'Sodium']

        for index, recipe in enumerate(top_recipes):
            # Get nutrition data
            nutrition_response = requests.get(f'https://api.spoonacular.com/recipes/{recipe["id"]}/nutritionWidget.json', params={'apiKey': spoon_key})
            nutrition_data = nutrition_response.json()

            # Get recipe instructions
            recipe_response = requests.get(f'https://api.spoonacular.com/recipes/{recipe["id"]}/information', params={'apiKey': spoon_key})
            recipe_data = recipe_response.json()
            instructions = recipe_data.get('analyzedInstructions', [{}])[0].get('steps', [])

            # Build recipe info
            recipe_info = {
                "title": recipe['title'],
                "image": recipe['image'],
                "usedIngredients": [item['name'] for item in recipe['usedIngredients']],
                "missedIngredients": [item['name'] for item in recipe['missedIngredients']],
                "nutrition": {nutrient["name"]: f"{nutrient['amount']} {nutrient['unit']}" for nutrient in nutrition_data.get('nutrients', []) if nutrient["name"] in desired_nutrition},
                "instructions": [f"Step {step['number']}: {step['step']}" for step in instructions]
            }
            recipes_list.append(recipe_info)
       
        return recipes_list
    
    
    
    