from flask import render_template
from app import app
from . import generateDrink

drinkgen = generateDrink.DrinkGenerator()

@app.route('/')
@app.route('/index')
def index():
    (ingredients, measures) = drinkgen.generateDrink()
    ingredient_strings = drinkgen.lookupValues(ingredients, measures)
    return render_template('index.html', ingredients = ingredient_strings)
