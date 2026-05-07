from abc import ABCMeta, abstractstaticmethod, abstractmethod
from typing import Self


class IPerson(metaclass=ABCMeta):

  @abstractmethod
  def person_method():
    '''interface method'''

class Student(IPerson):

  def __init__(self):
    self.name= 'Basic Student Name'

  def person_method(self)->Self:
    print('I am a student')
    return self

class Teacher(IPerson):

  def __init__(self):
    self.name='Basic Teacher Name'

  def person_method(self) -> Self:
    print("I'm a teacher")
    return self

class PersonFactory:

  @staticmethod
  def build_person(person_type):
    if person_type=='Student':
      return Student()
    if person_type=='Teacher':
      return Teacher()
    raise ValueError('Invalid type')


if __name__ == '__main__':
  choice = input("What type of person do you want to create?\n")
  person = PersonFactory.build_person(choice).person_method()

