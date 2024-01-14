import requests
import json
import os

# Spoonacular API
api_key = ''
end_point = 'https://api.spoonacular.com/recipes/findByIngredients'
file_path = "food_prices.json"

recipes_list = []

try:
    with open(file_path, 'r') as file:
        data = json.load(file)

    names = ','.join([recipe.get('name', '') for recipe in data.get('groceryItems', [])])

    parameters = {
        'ingredients': names,
        'apiKey': api_key,
        'addRecipeNutrition': True
    }

    response = requests.get(end_point, params=parameters)
    sorted_recipes = sorted(response.json(), key=lambda x: x.get('missedIngredientCount', 0))

    # Desired nutrition fields
    desired_nutrition = ['Calories', 'Protein', 'Fiber', 'Fat', 'Carbohydrates', 'Sodium']

    for index, recipe in enumerate(sorted_recipes[:5]):
        # Get nutrition data
        nutrition_response = requests.get(f'https://api.spoonacular.com/recipes/{recipe["id"]}/nutritionWidget.json', params={'apiKey': api_key})
        nutrition_data = nutrition_response.json()

        # Get recipe instructions
        recipe_response = requests.get(f'https://api.spoonacular.com/recipes/{recipe["id"]}/information', params={'apiKey': api_key})
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

except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

# Write to a JSON file
output_file = 'recipes_output.json'
with open(output_file, 'w') as file:
    json.dump(recipes_list, file, indent=4)

data = recipes_list

# Generate TypeScript code
typescript_code = "import { title } from 'process'\n\n"
typescript_code += "interface NutritionType { Calories: string; Fat: string; Carbohydrates: string; Sodium: string; Protein: string; Fiber: string }\n"
typescript_code += "interface DataType { title: string; image: string; usedIngredients: string[]; missedIngredients: string[]; nutrition: NutritionType; instructions: string[] }\n\n"
typescript_code += "const data: DataType[] = [\n"

# Loop through each item and format it
for item in data["groceryItems"]:
    typescript_code += "    {\n"
    typescript_code += f"        title: \"{item['title']}\",\n"
    typescript_code += f"        image: \"{item['image']}\",\n"
    typescript_code += f"        usedIngredients: {json.dumps(item['usedIngredients'])},\n"
    typescript_code += f"        missedIngredients: {json.dumps(item['missedIngredients'])},\n"
    typescript_code += f"        nutrition: {json.dumps(item['nutrition'])},\n"
    typescript_code += f"        instructions: {json.dumps(item['instructions'])}\n"
    typescript_code += "    },\n"

# Close the array and export statement
typescript_code += "]\nexport default data"

output_file = 'recipes_output.ts'  # Specify your file path here
with open(file_path, 'w') as file:
    file.write(typescript_code)


print(f"Saved top 5 recipes to {output_file} JSON")
print(f"Saved top 5 recipes to {output_file} TypeScript")

