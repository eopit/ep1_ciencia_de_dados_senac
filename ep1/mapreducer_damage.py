from dataclasses import dataclass
from typing import List

from mrjob.job import MRJob
from mrjob.step import MRStep


@dataclass
class DamageByType:
    amount: float
    type: str


@dataclass
class Pokemon:
    name: str
    types: [str]
    damage_taken: List[DamageByType]


@dataclass
class PokemonDamageReceived:
    pokemonType: str
    amount: float
    attackerType: str


class MapReducerDamage(MRJob):
    # skip first line since it's the csv header
    csv_header = True
    headers = []

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer)
        ]

    def mapper(self, _, line):
        if MapReducerDamage.csv_header:  # static due variable random reset
            MapReducerDamage.csv_header = False
            MapReducerDamage.headers = line.split(',')
        else:
            line = line.split(',')

            for amountAndType in line[self._column("damage_taken_by_type")].split(';'):
                amount, type = amountAndType.split(' ')

                yield type.split('=')[1], 100 * float(amount.split('=')[1])

    def reducer(self, type, damages):
        damages = list(damages)
        quantity = len(damages)
        total = sum(damages)
        mean = total / quantity

        yield ">", f"The average damage taken by pokemons of type {type} is {round(mean)}"

    def _column(self, column: str) -> int:
        return MapReducerDamage.headers.index(column)


if __name__ == '__main__':
    MapReducerDamage.run()
