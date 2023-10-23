import typing as tp

from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass, field, InitVar

a = 15


@dataclass(frozen=True, order=True)
class Item(object):
    title: str = field(compare=True)
    item_id: int = field(compare=False)
    cost: int = field(compare=True)

    def __post_init__(self) -> None:
        if self.cost <= 0 or not len(str(self.title)):
            raise AssertionError()

@dataclass
class Position(ABC):
    item: Item

    @abstractclassmethod
    def cost(self) -> tp.Any:
        return self.item.cost

@dataclass
class CountedPosition(Position):
    count: float = 1.0

    @property
    def cost(self) -> tp.Any:
        return self.count * self.item.cost


@dataclass
class WeightedPosition(Position):
    weight: float = 1.0

    @property
    def cost(self) -> tp.Any:
        return self.weight * self.item.cost


@dataclass
class Order:
    order_id: int = 0
    positions: list[Position] = field(default_factory=list[tp.Any])
    cost: int = 0
    have_promo: InitVar[tp.Any] = False

    def __post_init__(self, have_promo: tp.Any) -> None:
        op = 0

        for p in self.positions:
            op += p.cost

        if have_promo:
            dis = 1 - a / 100
        else:
            dis = 1

        self.cost = int(op * dis)

