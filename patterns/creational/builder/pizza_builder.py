from dataclasses import dataclass, field
from typing import Self, Optional

@dataclass(frozen=True, slots =True)
class Pizza:

  chicken: int=field(default=0)
  sauce: Optional[str] = field(default=None)
  ketchup: bool = field(default=False)


  def __post_init__(self)-> None:
    if self.chicken < 0:
      raise ValueError(f'Take some chicken bro. It cannot be less then zero:{self.chicken}')
    if self.chicken > 100:
      raise ValueError(f'Too much chicken bro: {self.chicken}')
    if self.sauce and not self.sauce.strip():
      raise ValueError(f'Sauce cannot be empty string')

  def __str__(self):
    parts=[]
    if self.chicken:
      parts.append(f'{self.chicken}')
    if self.sauce:
      parts.append(f'{self.sauce}')
    if self.ketchup:
      parts.append(f'{self.ketchup}')
    return f'Pizza({', '.join(parts)})' if parts else 'Pizza(base)'


class PizzaBuilder:

  def __init__(self)->None:
    self.pizza = Pizza()


  def add_chicken(self, amount: int)-> Self:
    if amount < 0:
      raise ValueError(f'Add some chicken bro. It cannot be less then zero:{amount}')
    self._chicken=amount
    return self

  def add_sauce(self, sauce:str) -> Self:
    if not sauce or not sauce.strip():
      raise ValueError('Sauce cannot be empty bro')
    self._sauce=sauce
    return self


  def add_ketchup(self, enabled:bool=True)-> Self:
    self._ketchup=enabled
    return self

  def build(self)->Pizza:
    return Pizza(
      chicken=self._chicken,
      sauce=self._sauce,
      ketchup=self._ketchup
    )

  def reset(self)-> Self:
    self._chicken=0
    self._sauce=None
    self._ketchup=False


class PizzaDirector:

  @staticmethod
  def margarita(builder:PizzaBuilder)->Pizza:
    return builder.reset().add_ketchup('Tomato')

  @staticmethod
  def chicken_bbq(builder:PizzaBuilder)->Pizza:
    return

