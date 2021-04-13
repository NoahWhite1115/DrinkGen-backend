import csv
import numpy

#gets a list of all the ingredients present, used for indexing and lookup later
def buildIngredientList(infile):
    ingredients_list = []

    with open(infile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = [v for k,v in row.items() if 'Ingredient' in k]
            data = list(filter(None, data))
            for ingredient in data:
                if ingredient.lower() not in ingredients_list:
                    ingredients_list.append(ingredient.lower().strip())

    return ingredients_list 

#a matrix of the probabilities of getting one ingredient given another (markov chain)
def buildIngredientMatrix(infile, ingredients_list):
    ingredient_matrix = numpy.zeros(shape=(len(ingredients_list), len(ingredients_list)))

    with open(infile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = [v for k,v in row.items() if 'Ingredient' in k]
            data = list(filter(None, data))
            for ingredient1 in data:
                for ingredient2 in data:
                    x = ingredients_list.index(ingredient1.lower().strip())
                    y = ingredients_list.index(ingredient2.lower().strip())

                    ingredient_matrix[x][y] += 1

    return ingredient_matrix

#a list of all possible measurements, used for lookup/indexing
def buildMeasuresList(infile):
    measures_list = ['']
    with open(infile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = [v for k,v in row.items() if 'Measure' in k]
            data = list(filter(None, data))
            for measure in data:
                if measure.lower() not in measures_list:
                    measures_list.append(measure.lower())

    return measures_list

#build measures matrix (markov-like, normalized)
def buildMeasureMatrix(infile, ingredients_list, measures_list):
    measure_matrix = numpy.zeros(shape=(len(ingredients_list), len(measures_list)))

    with open(infile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for i in range(1,12):
                if row['strIngredient' + str(i)] == '':
                    break
                x = ingredients_list.index(row['strIngredient' + str(i)].lower().strip())
                y = measures_list.index(row['strMeasure' + str(i)].lower())

                measure_matrix[x][y] += 1

    return measure_matrix

def buildDataStructures(infile):
    ingredient_list = buildIngredientList(infile)
    measures_list = buildMeasuresList(infile)

    ingredient_matrix = buildIngredientMatrix(infile, ingredient_list)
    measure_matrix = buildMeasureMatrix(infile, ingredient_list, measures_list)

    #extract the diaganol (to build the starter array), then normalize the ingredient matrix
    starter_array = numpy.diag(ingredient_matrix)
    numpy.save("starter_array.npy", starter_array)

    numpy.fill_diagonal(ingredient_matrix, 0)
    numpy.save("ingredient_matrix.npy", ingredient_matrix)

    numpy.save("measure_matrix.npy", measure_matrix)

    with open('ingredients.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(ingredient_list)

    with open('measures.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(measures_list)

    return(ingredient_matrix, ingredient_list, starter_array, measure_matrix, measures_list)

   
buildDataStructures(r".\all_drinks.csv")