from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample recipes data
recipes = [
    {"id": 1, "name": "Pasta", "ingredients": ["pasta", "tomato sauce", "cheese"], "storage": "fridge", "expiration": "2025-01-30"},
    {"id": 2, "name": "Salad", "ingredients": ["lettuce", "tomato", "cucumber", "dressing"], "storage": "fridge", "expiration": "2025-01-28"},
    {"id": 3, "name": "Sandwich", "ingredients": ["bread", "cheese", "lettuce", "tomato"], "storage": "fridge", "expiration": "2025-02-05"},
    {"id": 4, "name": "Smoothie", "ingredients": ["banana", "milk", "yogurt"], "storage": "fridge", "expiration": "2025-02-01"},
    {"id": 5, "name": "Omelette", "ingredients": ["eggs", "cheese", "milk", "onion"], "storage": "fridge", "expiration": "2025-01-25"},
]

# Sample inventory data
inventory = [
    {"ingredient": "pasta", "quantity": 2, "expiration": "2025-02-01"},
    {"ingredient": "tomato sauce", "quantity": 1, "expiration": "2025-01-29"},
    {"ingredient": "lettuce", "quantity": 1, "expiration": "2025-01-26"},
    {"ingredient": "bread", "quantity": 1, "expiration": "2025-02-10"},
    {"ingredient": "banana", "quantity": 5, "expiration": "2025-02-02"},
    {"ingredient": "milk", "quantity": 2, "expiration": "2025-02-04"},
    {"ingredient": "eggs", "quantity": 6, "expiration": "2025-01-27"},
    {"ingredient": "cheese", "quantity": 3, "expiration": "2025-01-30"},
    {"ingredient": "onion", "quantity": 1, "expiration": "2025-02-15"},
]

# Convert expiration date to datetime object
def convert_dates(inventory):
    for item in inventory:
        item['expiration'] = datetime.strptime(item['expiration'], "%Y-%m-%d")
    return inventory

# Recommendation based on available ingredients
def recommend_meals(inventory, recipes):
    inventory = convert_dates(inventory)
    recommended_meals = []

    for recipe in recipes:
        # Check if all ingredients are available in the inventory
        available_ingredients = [ingredient for ingredient in recipe['ingredients'] if any(ingredient == item['ingredient'] and item['expiration'] > datetime.now() for item in inventory)]
        
        if len(available_ingredients) == len(recipe['ingredients']):
            recommended_meals.append(recipe)

    return recommended_meals

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend_meals', methods=['GET'])
def get_recommendations():
    recommended = recommend_meals(inventory, recipes)
    return jsonify([meal['name'] for meal in recommended])

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    ingredient = request.json.get('ingredient')
    if ingredient:
        inventory.append({"ingredient": ingredient, "quantity": 1, "expiration": "2025-12-31"})  # Add a dummy expiration date for now
    return jsonify({"status": "success", "inventory": [item['ingredient'] for item in inventory]})

if __name__ == '__main__':
    app.run(debug=True)
