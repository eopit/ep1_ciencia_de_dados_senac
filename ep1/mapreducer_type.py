from mrjob.job import MRJob
from mrjob.step import MRStep


class MapReducerType(MRJob):
    # skip first line since it's the csv header
    csv_header = True
    headers = []

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer)
        ]

    def mapper(self, _, line):
        if MapReducerType.csv_header:  # static due variable random reset
            MapReducerType.csv_header = False
            MapReducerType.headers = line.split(',')
        else:
            line = line.split(',')

            for type in line[self._column("types")].split(';'):
                yield type, line[self._column("name")]

    def reducer(self, type, value):
        quantity = len(list(value))
        yield ">", f'Type {type} has {quantity} pokemons'

    def _column(self, column: str) -> int:
        return MapReducerType.headers.index(column)


if __name__ == '__main__':
    MapReducerType.run()
