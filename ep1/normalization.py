import json
import re

import pandas

class DamageByTypeInput:
    def __init__(self, amount: str, type: str):
        self.amount = amount
        self.type = type


class DamageByTypeOutput:
    def __init__(self, amount: float, type: str):
        self.amount = amount
        self.type = type

    def __repr__(self):
        return f'Amount={self.amount} Type={self.type}'


class Pokemon:
    def __init__(self, number: str, name: str, evolutions: [str], height: str, weight: str, types: [str],
                 damage_taken_by_type: [DamageByTypeInput]):
        self.number = number
        self.name = self._normalize_name(name)
        self.next_evolution = self._get_next_evolution(self.name, [re.sub(r'[^a-zA-Z]', '', i) for i in evolutions])
        self.height_in_cm = height
        self.weight_in_kg = weight
        self.types = ';'.join(types)
        self.damage_taken_by_type = ';'.join([self._format_damage_amount(input).__repr__() for input in damage_taken_by_type])

    def _get_next_evolution(self, name: str, evolutions: [str]) -> str:
        size = len(evolutions)
        try:
            index = evolutions.index(name)
        except ValueError:
            return ""

        if index == size - 1:
            return ""

        return evolutions[index + 1]

    def _format_damage_amount(self, input: DamageByTypeInput) -> DamageByTypeOutput:
        value = 0
        if input['amount'] == '4':
            value = 4
        elif input['amount'] == '2':
            value = 2
        elif input['amount'] == '½':
            value = 0.5
        elif input['amount'] == '¼':
            value = 0.25
        elif input['amount'] == '0':
            value = 0
        elif input['amount'] == '':
            value = 1

        return DamageByTypeOutput(value, input['type'])

    def _normalize_name(self, name: str):
        return name.replace('♂ (male)', '').replace('♀ (female)', '')


with open('pokemon.json', 'r') as f:
    input = json.load(f)
    pokemons = []

    for row in input:
        pokemon = Pokemon(
            row['number'],
            row['name'],
            row['_evolutions'],
            row['height'],
            row['weight'],
            row['_types'],
            row['_damage_taken_by_type'],
        )
        pokemons.append(pokemon)

    df = pandas.DataFrame([vars(i) for i in pokemons])
    df['height_in_cm'] = df['height_in_cm'].apply(lambda a: round(float(a.split(' ')[0])*100))
    df['weight_in_kg'] = df['weight_in_kg'].apply(lambda a: float(a.split(' ')[0]))
    df = df.sort_values('number')

    df.to_csv("pokemon.csv", index=False)
