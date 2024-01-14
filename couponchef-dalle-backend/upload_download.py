import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import base64
import requests
import json
import certifi
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.abspath('../'))
from SpoonacularAPI import Spoonacular

MONGO_URI = "mongodb+srv://johnqnguyen10:dJPMb7paDUYFHfvN@cluster0.h4nqxna.mongodb.net/?retryWrites=true&w=majority"
MONGO_CLIENT = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where(), tls=True)
MONGO_DB = MONGO_CLIENT["DEV"]
collection = MONGO_DB['recipe']

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = 'Content-Type'

load_dotenv()
api_key = os.environ.get("API_KEY")

@app.route("/getrecipes", methods=["GET"])
@cross_origin()
def getRecipes():
    print("1")
    collection.find()
    recipes = list(collection.find())
    print(recipes)
    return recipes

@app.route("/upload", methods=["POST"])
@cross_origin()
def saveImage():
    print("image received.")
    uploaded_image = request.files["image"]

    if uploaded_image:
        image_data = uploaded_image.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

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

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )

        listed_food = response.json()["choices"][0]["message"]["content"]
        print(listed_food)

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
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

        file_path = "../food_prices.json"
        data = json.loads(response.json())
        message_content = data["choices"][0]["message"]["content"]

        with open(file_path, "w") as json_file:
            json.dump(json.loads(message_content), json_file, indent=4)
        print(message_content)

        print( "Image received")
        print("i'm here")
        json_data = Spoonacular()
        print(json_data)
        collection.insert_many(json_data)
        return jsonify(json_data)


    else:
        return "No image file uploaded"
    



if __name__ == "__main__":
    app.run(port=5000)

