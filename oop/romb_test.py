class A:
  def method(self):
    return 'A'

class B(A):
  def method(self):
    return 'B'

class C(A):
  def method(self):
    return 'C'

class D(B,C):
  pass

if __name__ == '__main__':
    print(D.__mro__)
    print(D().method())
    print(B().method())
    print(C().method())

