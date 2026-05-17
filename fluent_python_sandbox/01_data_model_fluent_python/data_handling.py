#array.array
from array import array
from random import random


def array_handling():
  '''
  list — у нас хранит массив указателей на PyObject*. Крайне невыгодно если использовать для большого
  объёма данных.
  array.array — хранит сырые данные нужного С-типа, без объектных заголовков.
  некоторые флаги в сигнатуре:
  i - signed int
  I - unsigned int
  q - signed long
  Q - unsigned long
  f - float
  d - double
  :return:
  '''
  floats = array('d', (random() for i in range(10**7)))
  print(floats[-1])

if __name__ == '__main__':
    array_handling()

