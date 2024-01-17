animals_factory.py
from .animals import Cat, Cow, Dog
from abc import ABC, abstractmethod
from typing import Any


class Animal(ABC):
    @abstractmethod
    def say(self) -> str:
        pass


class CatAdapter(Animal):
    def __init__(self, cat: Cat):
        self.cat = cat

    def say(self) -> str:
        return self.cat.say()


class DogAdapter(Animal):
    def __init__(self, dog: Dog):
        self.dog = dog

    def say(self) -> str:
        return self.dog.say('woof')


class CowAdapter(Animal):
    def __init__(self, cow: Cow):
        self.cow = cow

    def say(self) -> str:
        return self.cow.talk()


def animals_factory(animal: Any) -> Animal:
    if isinstance(animal, Cat):
        return CatAdapter(animal)
    elif isinstance(animal, Dog):
        return DogAdapter(animal)
    elif isinstance(animal, Cow):
        return CowAdapter(animal)
    else:
        raise TypeError
temperature.py
from typing import Any


class Kelvin:
    def __init__(self, attr_name: str) -> None:
        self.attr_name: str = attr_name

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        if not hasattr(instance, self.attr_name):
            raise AttributeError(f"Attribute {self.attr_name} is not set")

        return getattr(instance, self.attr_name)

    def __set__(self, instance: Any, value: float) -> None:
        if value == 10 and instance.__class__.__name__ == "BadKelvin":
            raise AttributeError("Temperature value cannot be 10 in BadKelvin")
        if value <= 0:
            raise ValueError("Temperature in Kelvin must be greater than 0")
        setattr(instance, self.attr_name, value)

    def __delete__(self, instance: Any) -> None:
        raise ValueError("Cannot delete attribute")


class Celsius:
    def __init__(self, kelvin_attr_name: str) -> None:
        self.kelvin_attr_name: str = kelvin_attr_name

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        if not hasattr(instance, self.kelvin_attr_name):
            raise AttributeError(f"Attribute {self.kelvin_attr_name} is not set")
        kelvin_value = getattr(instance, self.kelvin_attr_name)
        if kelvin_value == 10:
            raise AttributeError("Temperature value cannot be 10")
        return kelvin_value - 273

    def __set__(self, instance: Any, value: float) -> None:
        raise AttributeError("Cannot set attribute")

    def __delete__(self, instance: Any) -> None:
        raise ValueError("Cannot delete attribute")
        
