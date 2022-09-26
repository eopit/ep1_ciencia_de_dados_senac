from dataclasses import dataclass
from typing import List


@dataclass
class Evolution:
    name: str


@dataclass
class Type:
    value: str


@dataclass
class DamageByType:
    amount: float
    type: Type


@dataclass
class Pokemon:
    number: int
    name: str
    _evolutions: List[Evolution]
    height: float
    weight: float
    _types: List[Type]
    _damage_taken_by_type: List[DamageByType]

    def add_evolution(self, evolution: Evolution):
        self._evolutions.append(evolution)

    def add_type(self, type: Type):
        self._types.append(type)

    def next_evolution(self) -> str:
        pass

    def add_damage_taken_by_type(self, amount: float, type: Type):
        pass
