import os
from flask import Flask, request
from flask_cors import CORS, cross_origin

from services.service import Service

import requests
import json
from dotenv import load_dotenv
from openai import OpenAI


app = Flask(__name__)
CORS(app)
service = Service()

load_dotenv()
api_key = os.environ.get("API_KEY")
spoon_key = os.environ.get("SPOON_KEY")
spoon_endpoint = 'https://api.spoonacular.com/recipes/findByIngredients'


@app.route("/upload", methods=["POST"])
@cross_origin()
def saveImage():
    
    # Top 10 recipes 
    top_ten = sorted_recipes[:10]
    
    # Nutrients for the top 10 recipes
    for id in top_ten:
        recipe_id = id['id']
        nutrition_parameters = {
            'id': recipe_id,
            'apiKey': api_key
        }
        
        # nutrional response for top 10
        nutrition_response = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json', params=nutrition_parameters)
        nutrition_data = nutrition_response.json()
        
        desired_nutrition = [
            'Calories', 
            'Protein', 
            'Fiber', 
            'Fat', 
            'Carbohydrates', 
            'Sodium'
            ]
        
        for nutrient in desired_nutrition:
            if nutrient in nutrition_data:
                value = nutrition_data[nutrient]

@app.route("/test", methods=["POST"])
@cross_origin()
def test():
    # uploaded image
    uploaded_image = request.files["image"]
    base64_image = service.encodeImage(uploaded_image)
    
    # gpt4_response received
    gpt4_response = service.requestGPT4(base64_image, api_key)
    
    # gpt4_response parsed into json
    listed_food = gpt4_response.json()["choices"][0]["message"]["content"]
    
    # gpt3_response parsed into dictionary
    message_content = service.requestGPT3(listed_food, api_key)
    
    # ingredient_names extracted from gpt3_response
    ingredient_names = service.extractNames(message_content)
    
    # Spoonacular request for recipes (sorted by least amount of missing ingredients)
    sorted_recipes = service.requestSpoonacular(ingredient_names, spoon_key, spoon_endpoint)
    #works
    
    # extract top recipes
    number_of_dishes = 2
    top_recipes = sorted_recipes[:number_of_dishes]
    
    # save top_recipes
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data.json")
    json_string = json.dumps(top_recipes)
    
    with open(file_path, "w") as json_file:
        json_file.write(json_string)
    
    return "hello!"
    

if __name__ == "__main__":
    app.run(port=5000)
