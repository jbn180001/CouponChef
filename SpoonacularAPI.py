import requests
import json
import os

# Spoonacular API
def Spoonacular():

    print("1")
    api_key = 'b95671fa92e44186bbf2b6cb0058d25c'
    end_point = 'https://api.spoonacular.com/recipes/findByIngredients'
    file_path = "../food_prices.json"

    print("2")
    recipes_list = []

    print("3")
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        names = ','.join([recipe.get('name', '') for recipe in data.get('groceryItems', [])])

        parameters = {
            'ingredients': names,
            'apiKey': api_key,
            'addRecipeNutrition': True
        }

        print("4")
        response = requests.get(end_point, params=parameters)
        sorted_recipes = sorted(response.json(), key=lambda x: x.get('missedIngredientCount', 0))

        print("5")
        # Desired nutrition fields
        desired_nutrition = ['Calories', 'Protein', 'Fiber', 'Fat', 'Carbohydrates', 'Sodium']

        print("6")
        for index, recipe in enumerate(sorted_recipes[:5]):
            # Get nutrition data
            nutrition_response = requests.get(f'https://api.spoonacular.com/recipes/{recipe["id"]}/nutritionWidget.json', params={'apiKey': api_key})
            nutrition_data = nutrition_response.json()

            print("7")
            # Get recipe instructions
            recipe_response = requests.get(f'https://api.spoonacular.com/recipes/{recipe["id"]}/information', params={'apiKey': api_key})
            recipe_data = recipe_response.json()
            instructions = recipe_data.get('analyzedInstructions', [{}])[0].get('steps', [])

            print("8")
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

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Write to a JSON file
    output_file = 'recipes_output.json'
    # with open(output_file, 'w') as file:
    #     json.dump(recipes_list, file, indent=4)

    
    json_data = recipes_list
    return json_data

    # JSON VALIDATOR

    # # Generate TypeScript code
    # # Analyze the structure and generate TypeScript interfaces
    # interfaces = "interface NutritionType {\n"
    # for key, value in json_data['foodItems'][0]['nutrition'].items():
    #     interfaces += f"  {key}: string;\n"
    # interfaces += "}\n\n"

    # interfaces += "interface FoodItemType {\n"
    # for key, value in json_data['foodItems'][0].items():
    #     if key == 'nutrition':
    #         interfaces += f"  {key}: NutritionType;\n"
    #     elif isinstance(value, list):
    #         interfaces += f"  {key}: string[];\n"
    #     else:
    #         interfaces += f"  {key}: string;\n"
    # interfaces += "}\n\n"

    # # Generate TypeScript data assignment
    # ts_data = "const foodItems: FoodItemType[] = " + json.dumps(json_data['foodItems'], indent=2) + ";\n\n"
    
    # # Combine interfaces and data
    # ts_code = interfaces + ts_data + "export default foodItems;"

    # output_file = 'recipes_output.ts'  # Specify your file path here
    # with open(file_path, 'w') as file:
    #     file.write(typescript_code)


    print(f"Saved top 5 recipes to {output_file} JSON")
    print(f"Saved top 5 recipes to {output_file} TypeScript")


