import csv
import numpy

def loadList(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        ingredient_list = next(reader)
    return ingredient_list

def maskStarter():

    starter_array = numpy.load('../data/starter_array.npy')

    ingredient_list = loadList('../data/ingredients.csv')
    starter_mask = loadList('../data/mask.csv')
    
    values = []

    for i in starter_mask:
        values.append(ingredient_list.index(i))

    for i in range(len(starter_array)):
        if i not in values:
            starter_array[i] = 0

    numpy.save("../data/starter_array.npy", starter_array)

def displayMeasures(measure_list):
    for index, i in enumerate(measure_list):
        print(str(index) + ": " + i)


def mergeMeasures(index_summed, index_removed):
    measure_list = loadList('../data/measures.csv')
    measures_array = numpy.load('../data/measure_matrix.npy')
    measures_array[:,index_summed] = measures_array[:,index_summed] + measures_array[:,index_removed]
    measures_array = numpy.delete(measures_array, index_removed, axis = 1)
    

measure_list = loadList('../data/measures.csv')
mergeMeasures(55, 66)