import csv
import numpy
import random

def loadList(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        ingredient_list = next(reader)
    return ingredient_list

def markovStep(array):
    rand = random.uniform(0, 1)
    for index, val in enumerate(array):
        if val > rand:
            return(index-1)

def main(ingredient_matrix = None, ingredient_list = None, 
    starter_array = None, measure_matrix = None, measures_list = None):
    #load data 
    if ingredient_matrix is None:
        ingredient_matrix = numpy.load("ingredient_matrix.npy")
    if starter_array is None:
        starter_array = numpy.load("starter_array.npy")
    if measure_matrix is None:
        measure_matrix = numpy.load("measure_matrix.npy")

    if ingredient_list is None:
        ingredient_list = loadList('ingredients.csv')

    if measures_list is None:
        measures_list = loadList('measures.csv')

    #normalize all the input data, then cumulative sum it
    norm = starter_array.sum()
    normalized_starter_array = starter_array/norm
    starter_array = numpy.cumsum(normalized_starter_array)
    normalized_starter_array = numpy.insert(starter_array, 0, 0)

    ingredient_matrix = ingredient_matrix * 25
    ingredient_matrix = ingredient_matrix + 1
    numpy.fill_diagonal(ingredient_matrix, 0)
    sum_of_rows = ingredient_matrix.sum(axis=1)
    normalized_ing_matrix = ingredient_matrix / sum_of_rows[:, numpy.newaxis]
    normalized_ing_matrix = numpy.cumsum(normalized_ing_matrix, axis=1)
    new_col = numpy.zeros(len(ingredient_list))
    normalized_ing_matrix = numpy.insert(normalized_ing_matrix, 0, new_col, axis=1)

    sum_of_rows = measure_matrix.sum(axis=1)
    normalized_measure_matrix = measure_matrix / sum_of_rows[:, numpy.newaxis]
    normalized_measure_matrix = numpy.cumsum(normalized_measure_matrix, axis=1)
    new_col = numpy.zeros(len(ingredient_list))
    normalized_measure_matrix = numpy.insert(normalized_measure_matrix, 0, new_col, axis=1)

    drink_data = []
    measure_data = []
    last_generated = 0

    #generate starting point
    last_generated = markovStep(starter_array)
    drink_data.append(last_generated)

    measure_data.append(markovStep(normalized_measure_matrix[last_generated]))

    #pass starting point to markov process
    times_run = 1
    len_modifier = 0.6
    while random.uniform(0, 1) < 1/(times_run * len_modifier):
        times_run += 1
        
        last_generated = markovStep(normalized_ing_matrix[last_generated])
        drink_data.append(last_generated)

        measure_data.append(markovStep(normalized_measure_matrix[last_generated]))

    print(drink_data)

    #turn list of generated numbers into names
    for i,j in zip(drink_data, measure_data):
        if not measures_list[j] == '':
            print(ingredient_list[i].strip("\n") + " : " + measures_list[j].strip("\n"))
        else:
            print(ingredient_list[i])

for i in range(100): 
    main()