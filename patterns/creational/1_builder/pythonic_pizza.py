from dataclasses import dataclass

@dataclass(frozen=True)
class Pizza:
  size:int
  cheese:bool=False
  pepperoni=False
  mushrooms:bool=False

  @property
  def description(self)->str:
    content=[]
    if self.size: content.append(self.size)
    if self.cheese: content.append(self.cheese)
    if self.pepperoni: content.append(self.pepperoni)
    if self.mushrooms:content.append(self.mushrooms)

    return f"{', '.join(str(c) for c in content)}"