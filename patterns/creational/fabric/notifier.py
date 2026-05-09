from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, Type, Dict


class Notifier(Protocol):
    def send(self, message:str)->str:...

class NotifierFabric:
  _register:Dict[str, Type[Notifier]]={}

  @classmethod
  def register(cls, notifier_type:str):
    def wrapper(wrapped_class: Type[Notifier]):
      cls._register[notifier_type] = wrapped_class
      return wrapped_class
    return wrapper

  @classmethod
  def create(cls, notifier_type:str)->Notifier:
    if notifier_type not in cls._register:
      raise ValueError(f'Unsupported type: {notifier_type}')
    return cls._register[notifier_type]()

@NotifierFabric.register('telegram')
class TelegramNotifier:
  def send(self, message:str)->str:
    return f'Sent to Telegram {message}'


@NotifierFabric.register('email')
class EmailNotifier:
  def send(self, message:str)->str:
    return f'Sent to email {message}'


if __name__ == '__main__':
    fabric = NotifierFabric()
    email = fabric.create('email')
    print(email.send("test message"))




