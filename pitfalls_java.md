# Python: подводные камни для Java-разработчика

## 1. Мутируемые дефолты в параметрах — самая частая ловушка

```python
def append_to(element, to=[]):   # список создаётся ОДИН раз при определении функции
    to.append(element)
    return to

append_to(1)  # [1]
append_to(2)  # [1, 2] — НЕ [2]!
```
В Java каждый вызов метода создаёт новый объект. В Python дефолт — это атрибут объекта функции (`f.__defaults__`), живёт пока живёт функция.

Правильно: `def append_to(element, to=None): if to is None: to = []`

---

## 2. `is` vs `==`

- `is` — сравнивает идентичность (адрес в памяти, как `==` для объектов в Java).
- `==` — сравнивает значение (вызывает `__eq__`).

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b   # True
a is b   # False — разные объекты

# Ловушка с интернированием:
x = 256; y = 256
x is y  # True (кэш -5..256)
x = 257; y = 257
x is y  # False (вне кэша, зависит от реализации)
```
Правило: всегда используй `is` только для `None`, `True`, `False` и enum-значений.

---

## 3. Нет перегрузки методов

В Java можно `void process(String s)` и `void process(int n)`. В Python — нет.

```python
def process(x):      # последнее определение перезаписывает предыдущее
    print("str")

def process(x):
    print("int")     # это выживет
```
Варианты решения:
- `isinstance(x, str)` внутри одного метода.
- `@functools.singledispatch` для dispatch по типу первого аргумента.
- `@overload` из typing (только для type checkers, не runtime).

---

## 4. GIL и потоки — не то что в Java

- Java threads реально параллельны для CPU-bound кода.
- Python threads: GIL позволяет только одному потоку исполнять Python-байткод в момент времени.
- Потоки в Python полезны для I/O-bound задач (сетевые запросы, файлы) — там GIL освобождается.
- Для CPU-bound — `multiprocessing` или `concurrent.futures.ProcessPoolExecutor`.

```python
# Это НЕ ускорит CPU-bound:
import threading
threads = [threading.Thread(target=heavy_computation) for _ in range(4)]
```

---

## 5. Всё — объект, нет примитивов

В Java `int`, `boolean` — примитивы, `Integer` — обёртка. В Python всё — объект, даже `1`.

```python
x = 1
x.bit_length()  # 1 — метод у числа
type(x)         # <class 'int'>
```

---

## 6. Замыкания и позднее связывание (late binding)

```python
funcs = [lambda: i for i in range(5)]
funcs[0]()  # 4, не 0 — i берётся в момент вызова, не создания lambda!
```
В Java с effectively final переменными такой ловушки нет.

Правильно: `lambda i=i: i` — зафиксировать значение через дефолтный аргумент.

---

## 7. `__eq__` убивает `__hash__`

Это та же идея что в Java (переопределяй оба вместе), но Python реализует её жёстче.

- **Java**: переопределил `equals()` без `hashCode()` — объект **остаётся хешируемым**, просто нарушается контракт. Тихая бага: `HashMap` работает неправильно, но `HashSet.add(obj)` не бросит исключение.
- **Python**: переопределил `__eq__` без `__hash__` — Python **автоматически ставит `__hash__ = None`**. Объект немедленно становится unhashable. Не тихий баг, а `TypeError` при первой же попытке.

```python
class Foo:
    def __eq__(self, other): return True

f = Foo()
hash(f)  # TypeError: unhashable type: 'Foo'
{f}      # TypeError: unhashable type: 'Foo'
{f: 1}   # TypeError: unhashable type: 'Foo'
```

Правило то же что в Java: переопределять оба вместе:
```python
def __eq__(self, other): return self.x == other.x
def __hash__(self): return hash(self.x)
```

---

## 8. `__init__` — не конструктор

Объект уже создан к моменту вызова `__init__`. Настоящий конструктор — `__new__`.

```python
class Foo:
    def __new__(cls, *args, **kwargs):
        print("создаётся объект")
        return super().__new__(cls)
    
    def __init__(self):
        print("инициализируется объект")
```

---

## 9. `super()` — не то же что в Java

В Java `super()` всегда вызывает прямого родителя. В Python `super()` следует MRO (C3 linearization), что при множественном наследовании может вести к неожиданным классам.

```python
class A:
    def method(self): print("A")

class B(A):
    def method(self):
        super().method()  # вызывает следующий по MRO, не обязательно A!
        print("B")
```

---

## 10. Генераторы исчерпываются молча

Java Stream бросает исключение при повторном использовании. Python-генератор просто даёт пустоту:

```python
gen = (x for x in range(5))
list(gen)   # [0, 1, 2, 3, 4]
list(gen)   # [] — генератор исчерпан, нет ошибки!
```

---

## 11. Декораторы — не аннотации Java

Java `@Transactional` — метаданные, обрабатываемые фреймворком. Python декоратор — это функция, которая исполняется в момент определения класса/функции.

```python
@my_decorator        # это вызов: my_decorator(func)
def func(): ...
```

---

## 12. `None` — синглтон, проверять через `is`

```python
x = None
x == None   # True, но плохо — кто-то мог переопределить __eq__
x is None   # True, правильно
```

---

## 13. Shallow copy по умолчанию везде

```python
a = [1, [2, 3]]
b = a[:]          # shallow copy
b[1].append(4)
print(a)          # [1, [2, 3, 4]] — вложенный список изменился!
```
Для глубокого копирования: `import copy; copy.deepcopy(a)`

---

## 14. `+=` на мутируемых и немутируемых — разное поведение

```python
# Список (мутируемый):
a = [1, 2]
b = a
a += [3]        # вызывает __iadd__, изменяет объект на месте
print(b)        # [1, 2, 3] — b видит изменение

# Кортеж (немутируемый):
a = (1, 2)
b = a
a += (3,)       # создаёт НОВЫЙ объект
print(b)        # (1, 2) — b не изменился
```

---

## 15. Строки — итерируемые, не массив символов

```python
for c in "hello":  # итерируется посимвольно
    print(c)

"e" in "hello"     # True — проверка подстроки
```
В Java `String` не итерируемый напрямую, нужен `toCharArray()` или `charAt()`.
