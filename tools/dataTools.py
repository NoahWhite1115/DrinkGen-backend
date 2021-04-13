import csv
import numpy

def loadList(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        ingredient_list = next(reader)
    return ingredient_list

def maskStarter():

    starter_array = numpy.load('starter_array.npy')

    ingredient_list = loadList('ingredients.csv')
    starter_mask = loadList('mask.csv')
    
    values = []

    for i in starter_mask:
        values.append(ingredient_list.index(i))

    for i in range(len(starter_array)):
        if i not in values:
            starter_array[i] = 0

    numpy.save("starter_array.npy", starter_array)

maskStarter()