import csv
import numpy
import random
import os 

class DrinkGenerator():
    def __init__(self, ingredient_matrix = None, ingredient_list = None, 
        starter_array = None, measure_matrix = None, measures_list = None):
        root = os.path.join(os.getcwd(), "data")

        if ingredient_matrix is None:
            ingredient_matrix = numpy.load(os.path.join(root, "ingredient_matrix.npy"))
        if starter_array is None:
            starter_array = numpy.load(os.path.join(root, "starter_array.npy"))
        if measure_matrix is None:
            measure_matrix = numpy.load(os.path.join(root, "measure_matrix.npy"))

        if ingredient_list is None:
            self.ingredient_list = self.loadList(os.path.join(root, 'ingredients.csv'))

        if measures_list is None:
            self.measures_list = self.loadList(os.path.join(root, 'measures.csv'))

        #normalize all the input data, then cumulative sum it
        norm = starter_array.sum()
        normalized_starter_array = starter_array/norm
        starter_array = numpy.cumsum(normalized_starter_array)
        self.normalized_starter_array = numpy.insert(starter_array, 0, 0)

        ingredient_matrix = ingredient_matrix * 25
        ingredient_matrix = ingredient_matrix + 1
        numpy.fill_diagonal(ingredient_matrix, 0)
        sum_of_rows = ingredient_matrix.sum(axis=1)
        normalized_ing_matrix = ingredient_matrix / sum_of_rows[:, numpy.newaxis]
        normalized_ing_matrix = numpy.cumsum(normalized_ing_matrix, axis=1)
        new_col = numpy.zeros(len(self.ingredient_list))
        self.normalized_ing_matrix = numpy.insert(normalized_ing_matrix, 0, new_col, axis=1)

        sum_of_rows = measure_matrix.sum(axis=1)
        normalized_measure_matrix = measure_matrix / sum_of_rows[:, numpy.newaxis]
        normalized_measure_matrix = numpy.cumsum(normalized_measure_matrix, axis=1)
        new_col = numpy.zeros(len(self.ingredient_list))
        self.normalized_measure_matrix = numpy.insert(normalized_measure_matrix, 0, new_col, axis=1)


    def loadList(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            ingredient_list = next(reader)
        return ingredient_list

    def markovStep(self, array):
        rand = random.uniform(0, 1)
        for index, val in enumerate(array):
            if val > rand:
                return(index-1)

    def generateDrink(self):
        drink_data = []
        measure_data = []
        last_generated = 0

        #generate starting point
        last_generated = self.markovStep(self.normalized_starter_array)
        drink_data.append(last_generated)

        measure_data.append(self.markovStep(self.normalized_measure_matrix[last_generated]))

        #pass starting point to markov process
        times_run = 1
        len_modifier = 0.6
        while random.uniform(0, 1) < 1/(times_run * len_modifier):
            times_run += 1
            
            last_generated = self.markovStep(self.normalized_ing_matrix[last_generated])
            drink_data.append(last_generated)

            measure_data.append(self.markovStep(self.normalized_measure_matrix[last_generated]))

        return(drink_data, measure_data)

    def lookupValues(self, drink_data, measure_data):
        data = []

        #turn list of generated numbers into names
        for i,j in zip(drink_data, measure_data):
            data.append(
                {'ingredient': self.ingredient_list[i].strip("\n"), 
                 'measure': self.measures_list[j].strip("\n")})
        return data