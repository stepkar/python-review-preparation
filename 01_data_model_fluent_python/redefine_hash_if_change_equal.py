from dataclasses import dataclass, field


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




