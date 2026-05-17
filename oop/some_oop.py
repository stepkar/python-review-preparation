from dataclasses import field, dataclass


@dataclass
class Person:
  name: str = field(init=False)
  age: int = field(init=False)
  _name:str=field(default='John Doe')
  _age:int=field(default=None)

  @property
  def name(self)->str:
    return self._name

  @name.setter
  def name(self, value:str):
    if not value:
      raise ValueError('No empty names')
    self._name=value

  # @property
  # def age(self)->str:
  #   return self._age
  #
  # @age.setter
  # def age(self, val:int):
  #   self._age=val

if __name__ == '__main__':
    person = Person('ljh', 23)
    print(person.name, person._age)
    person.name = 'asdf'
    print(person.name)
    person._age = 2
    print(person._age)
    PyLongObject

