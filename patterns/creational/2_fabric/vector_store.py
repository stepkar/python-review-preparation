import contextlib
import math
from dataclasses import field
from operator import index
from typing import Protocol, List, Type, Dict


class VectorStore(Protocol):
  host: str=field(default=None)

  def add(self, documents: list[dict])-> None:...
  def search(self, query: str, k:int)-> list[dict]:...
  def close(self)->None:...


class ElasticStore:
  def __init__(self, host:str, index:str):
    self.host = host
    self.index=index
    self._docs:List[dict]=[]
    print(f'Elk connected to {host}, index={index}')

  def add(self, documents) -> str:
    for doc in documents:
      doc_copy= doc.copy()
      doc_copy['_id']=len(self._docs)
      self._docs.append(doc_copy)
    print(f'Elastic indexed {len(documents)} docs. Total {len(self._docs)}')

  def search(self,query:str, k:int)->List[dict]:
    query_words=set(query.lower().split())
    results=[]
    for doc in self._docs:
      score=0
      if 'text' in doc:
        doc_words = set(doc['text'].lower().split())
        score=len(query_words&doc_words)
      if score>0:
        results.append({'id':doc['_id'], 'score':score, 'doc':doc})

    results.sort(key=lambda x: (-x['score'], x['id'],))
    top_k=results[:k]
    print(f'Elastic found {len(results)} matches, returning {len(top_k)}')
    return [{'id':r['id'], 'score':r['score']} for r in top_k]

  def close(self)->None:
    print('[Elastic] connection closed')

class FaissStore:
  """
  Эмуляция FAISS: хранит векторы и выполняет поиск k ближайших соседей
  по евклидову расстоянию. Векторы передаются в документах в поле "vector".
  """
  def __init__(self, dimension: int):
    self.dimension = dimension
    self._vectors: List[List[float]] = []
    self._metadata: List[dict] = []
    print(f"[FAISS] Initialized index for dim={dimension}")

  def add(self, documents: List[dict]) -> None:
    """Добавляет векторы и метаданные в индекс."""
    for doc in documents:
      vector = doc.get("vector")
      if vector is None or len(vector) != self.dimension:
        raise ValueError(f"All documents must have 'vector' of length {self.dimension}")
      self._vectors.append(vector)
      # сохраняем остальные поля как метаданные
      self._metadata.append({k:v for k,v in doc.items() if k != "vector"})
    print(f"[FAISS] Added {len(documents)} vectors. Total: {len(self._vectors)}")

  def search(self, query: str, k: int) -> List[dict]:
    try:
      query_vec = [float(x) for x in query.split(",")]
    except ValueError:
      raise ValueError("Query must be a comma-separated list of floats")
    if len(query_vec) != self.dimension:
      raise ValueError(f"Query vector dimension {len(query_vec)} != {self.dimension}")

    distances = []
    for i, vec in enumerate(self._vectors):
      # евклидово расстояние
      dist = math.sqrt(sum((a - b)**2 for a,b in zip(query_vec, vec)))
      distances.append((dist, i))
    distances.sort(key=lambda x: x[0])
    top_k = distances[:k]
    print(f"[FAISS] Found nearest {len(top_k)} neighbors")
    return [{"id": idx, "distance": round(dist, 4),
             "metadata": self._metadata[idx]} for dist, idx in top_k]

  def close(self) -> None:
    print("[FAISS] Index cleared (close)")

class StoreFactory:
  _registry:Dict[str, Type]={}

  @classmethod
  def register(cls, name:str, store_class:Type):
    cls._registry[name]=store_class

  @classmethod
  def create(cls, name:str, **kwargs)->VectorStore:
    store_class=cls._registry.get(name)
    if not store_class:
      raise KeyError(f'Unknown store type {name}. Registered: {list(cls._registry.keys())}')
    return store_class(**kwargs)

  @staticmethod
  @contextlib.contextmanager
  def session(store: VectorStore):
    try:
      yield store
    finally:
      store.close()

StoreFactory.register('elk', ElasticStore)
StoreFactory.register('faiss', FaissStore)

if __name__ == '__main__':
    store = StoreFactory.create('elk', host='http://localhost:9200', index='articles')
    with StoreFactory.session(store):
      store.add([
        {"text": "Python is great for machine learning"},
        {"text": "Java is popular for enterprise systems"},
        {"text": "Python and Java are both programming languages"}
      ])
    results = store.search("Python learning", k=2)
    print("Elastic results:", results)

    store2 = StoreFactory.create("faiss", dimension=3)
    with StoreFactory.session(store2):
      store2.add([
        {"vector": [1.0, 2.0, 3.0], "label": "A"},
        {"vector": [4.0, 5.0, 6.0], "label": "B"},
        {"vector": [1.1, 2.1, 3.1], "label": "A-like"}
      ])
      results = store2.search("1.0,2.0,3.0", k=2)
      print("FAISS results:", results)