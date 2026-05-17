from typing import Protocol, Dict, Type


class Document(Protocol):
  def load(self, path:str)->str:...
  def save(self, path:str)->None:...

class DocumentFactory:
  _registry:Dict[str, Type[Document],]

  @classmethod
  def registry(cls, type_doc):
    def wrapper(wrapped_class:Type[Document]):
      cls._registry[type_doc]=wrapped_class
      return wrapped_class
    return wrapper

  @classmethod
  def create(cls, type_doc)->Document:
    if type_doc not in cls._registry:
      raise ValueError(f'Unsupported type:{type_doc}')
    return cls._registry[type_doc]()

@DocumentFactory.registry('pdf')
class PdfDoc:
  def load(self, path:str)->str:return f'Loaded from {path}'
  def save(self, path:str): print(f'Saved to {path}')

