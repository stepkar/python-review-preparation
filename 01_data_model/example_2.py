import math

class Vector:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y=y

  def __repr__(self):
    return f'Vector({self.x!r},{self.y!r})'

  def __abs__(self):
    return math.hypot(self.x, self.y)

  #Если бул не реализован, пайтон обращается к len - если 0 то False, иначе True
  def  __bool__(self):
    return bool(abs(self))

  def __add__(self, other):
    x = self.x + other.x
    y = self.y + other.y
    return Vector(x, y)

  def __mul__(self, scalar):
    return Vector(self.x * scalar, self.y * scalar)


if __name__ == '__main__':
  v1 = Vector(3, 4)
  print(abs(v1))
