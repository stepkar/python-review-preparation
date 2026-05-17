from typing import Protocol, Type, Dict


class Animal(Protocol):
  def say(self)->str:...

class AnimalFabric:
  _register: Dict[str, Type[Animal]]={}

  @classmethod
  def register(cls, animal_type:str):
    def wrapper(wrapped_class: Type[Animal]):
      cls._register[animal_type]=wrapped_class
      return wrapped_class
    return wrapper

  @classmethod
  def create(cls, animal_type:str)->Animal:
    if animal_type not in cls._register:
      raise ValueError(f'Unsupported animal: {animal_type}')
    return cls._register[animal_type]()


@AnimalFabric.register('dog')
class Dog:
  def say(self):return 'Gav!'

@AnimalFabric.register('cat')
class Cat:
  def say(self):return 'Meow!'

if __name__ == '__main__':
    cat = AnimalFabric.create('cat')
    print(cat.say())
