from flask import request
from app import app
from . import generateDrink
from . import base64

drinkgen = generateDrink.DrinkGenerator()
converter = base64.Base64Converter()

@app.route('/make_drink')
def index():
    (ingredients, measures) = drinkgen.generateDrink()
    ingredient_strings = drinkgen.lookupValues(ingredients, measures)
    encoded_str = converter.num_encode(ingredients) + converter.num_encode(measures)
    return {'ingredients': ingredient_strings, 'encoded string': encoded_str}

@app.route('/get_drink')
def link():
    code = request.args.get('code')
    data = converter.num_decode(code)
    middle = len(data)//2
    ingredients = data[:middle]
    measures = data[middle:]
    ingredient_strings = drinkgen.lookupValues(ingredients, measures)
    #maybe remove encoded str for links?
    return {'ingredients': ingredient_strings}