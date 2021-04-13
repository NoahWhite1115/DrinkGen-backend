from flask import render_template
from app import app
from generateDrink import DrinkGenerator

drinkgen = DrinkGenerator()

@app.route('/')
@app.route('/index')
def index():
    (ingredients, measures) = DrinkGenerator.generateDrink()
    ingredient_strings = DrinkGenerator.lookupValues(ingredients, measures)
    return render_template('index.html', ingredients = ingredient_strings)