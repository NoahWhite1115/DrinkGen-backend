import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import random

class DynamoDrinkGenerator():
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
    
    def generateDrink(self):
        #generate starting point
        starter = self.getStarter()

        return self.generateDrinkWith(starter)

    def generateDrinkWith(self, starter):
        drink_data = []
        measure_data = []

        drink_data.append(starter)
        last_generated = starter

        times_run = 1
        len_modifier = 0.6
        while random.uniform(0, 1) < 1/(times_run * len_modifier):
            times_run += 1

            last_generated = self.markovStep(last_generated)
            drink_data.append(last_generated)

        for ingredient in drink_data:
            measure_data.append(self.getMeasure(ingredient))

        out_data = []
        for drink, measure in zip(drink_data, measure_data):
            out_data.append(drink, measure)
        
        return out_data


    #TODO: except on any markov step if passed ingredient doesn't exist
    def markovStep(self, ingredient):
        table = self.dynamodb.Table('Drink_Ingredients')
        rand = random.uniform(0, 1)

        response = table.query(
            KeyConditionExpression=Key('ingredient').eq(ingredient) & Key('probability').lt(Decimal(str(rand))),
            ScanIndexForward=False
        )

        return response['Items'][0]['next_ingredient']

    def getStarter(self):
        table = self.dynamodb.Table('Drink_Ingredients')
        rand = random.uniform(0, 1)
        response = table.query(
            KeyConditionExpression=Key('ingredient').eq('starter') & Key('probability').lt(Decimal(str(rand))),
            ScanIndexForward=False
        )
        return response['Items'][0]['next_ingredient']

    def getMeasure(self, ingredient):
        table = self.dynamodb.Table('Drink_Measures')
        rand = random.uniform(0, 1)
        response = table.query(
            KeyConditionExpression=Key('ingredient').eq(ingredient) & Key('probability').lt(Decimal(str(rand))),
            ScanIndexForward=False
        )

        return response['Items'][0]['measure']


gen = DynamoDrinkGenerator()
print(gen.generateDrinkWith('vodka'))