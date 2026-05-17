import sys
from dataclasses import dataclass, field
from siphash import siphash24

class Test:
  def __hash__(self):
    return (1 << 100) + 1

@dataclass(frozen=True, slots=True, kw_only=True)
class Person:
  name:str
  age:int
  sex:bool
  metadata:dict=field(default_factory=dict, compare=False, hash=False)

  def __eq__(self, other:object)->bool:
    if not isinstance(other, Person):
      return NotImplemented
    return(self.name, self.age)==(other.name, other.age)

  def __hash__(self)->int:
    return hash((self.name, self.age))

if __name__ == '__main__':

    a = (1700000000000000000000,)
    b = (1700000000000000000000,)
    print(a is b)
    # print((1 << 100) + 1)
    # print(hash(Test()))
    # print(sys.hash_info.modulus)
    # print(4449241812176275828&7)
    # print(-1806247072079675212&7)
    # print(hash('key0'))
    # print(hash('key1'))

    # print(f'{digest:#x}')




