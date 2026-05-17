class A:
  def method(self):
    return 'A'

class B:
  def method(self):
    return 'B'

class C:
  def method(self):
    return 'C'

class D:
  pass

class E:
  def method(self):
    return 'E'

class F(A, B, C):
  def method(self):
    return 'F'

class G(D, B, E):
  def method(self):
    return 'G'

class H(D, A):
  pass

class Z(F, G, H):
  pass

if __name__ == '__main__':
    print(Z.__mro__)
    print(Z().method())
    print(H().method())