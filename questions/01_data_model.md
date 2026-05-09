# Вопросы: Data Model и объектная модель Python

---

## Junior

### J1. Что такое `id()` в Python и что он возвращает?

<details>
<summary>Подсказка</summary>

`id(obj)` возвращает целое число — уникальный идентификатор объекта на время его жизни.  
В CPython это адрес объекта в памяти. Гарантия уникальности только пока объект жив.

```python
a = "hello"
b = "hello"
print(id(a), id(b))  # могут совпасть из-за интернирования
```
</details>

---

### J2. В чём разница между `is` и `==`?

<details>
<summary>Подсказка</summary>

- `is` — сравнивает **идентичность** (один ли это объект в памяти, через `id()`).
- `==` — сравнивает **значение** (вызывает `__eq__`).

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b   # True — одинаковые значения
a is b   # False — разные объекты

# Правило: is использовать только для None, True, False, enum
x is None       # правильно
x == None       # плохо — кто-то мог переопределить __eq__
```
</details>

---

### J3. Зачем нужны `__repr__` и `__str__`? В чём разница?

<details>
<summary>Подсказка</summary>

- `__str__` — читаемое представление для пользователя, вызывается `print()`, `str()`.
- `__repr__` — однозначное представление для разработчика, вызывается в REPL, `repr()`, в `f"{obj!r}"`.  
  Идеал: строка, по которой можно воссоздать объект (`eval(repr(obj)) == obj`).

Если определён только `__repr__` — он используется вместо `__str__`. Обратное неверно.

```python
class Point:
    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return f"Point({self.x}, {self.y})"
    def __str__(self): return f"({self.x}, {self.y})"
```
</details>

---

### J4. Что происходит когда ты вызываешь `len(obj)`?

<details>
<summary>Подсказка</summary>

Python вызывает `obj.__len__()`. Это не магия — просто синтаксический сахар.  
`len()` ожидает целое неотрицательное число. Если вернуть отрицательное — `ValueError`.

```python
class MyList:
    def __init__(self, data): self.data = data
    def __len__(self): return len(self.data)

m = MyList([1, 2, 3])
len(m)  # 3
```
</details>

---

### J5. Что такое dunder-методы (magic methods)? Приведи 5 примеров.

<details>
<summary>Подсказка</summary>

Методы с двойным подчёркиванием с обеих сторон (`__method__`). Python вызывает их неявно в ответ на операторы и встроенные функции. Примеры:

| Метод | Когда вызывается |
|-------|-----------------|
| `__init__` | при создании объекта |
| `__str__` | при `str(obj)`, `print(obj)` |
| `__len__` | при `len(obj)` |
| `__add__` | при `obj + other` |
| `__eq__` | при `obj == other` |
| `__iter__` | при `for x in obj` |
| `__contains__` | при `x in obj` |
</details>

---

### J6. Что делает `__bool__`? Что если его не определить?

<details>
<summary>Подсказка</summary>

`__bool__` определяет правдивость объекта в булевом контексте (`if obj:`, `bool(obj)`).

Порядок проверки:
1. `__bool__` — если определён, возвращает `True`/`False`
2. `__len__` — если `__bool__` нет, `True` если `len() != 0`
3. Иначе — объект всегда `True`

```python
class Empty:
    def __len__(self): return 0

e = Empty()
bool(e)  # False — через __len__
if e:    # не войдёт
    ...
```
</details>

---

## Middle

### M1. Чем `__getattr__` отличается от `__getattribute__`?

<details>
<summary>Подсказка</summary>

- `__getattribute__` — вызывается **всегда** при доступе к любому атрибуту (`obj.x`). Если переопределить без `super()`, сломаешь всё.
- `__getattr__` — вызывается только когда атрибут **не найден** обычным путём (fallback). Безопаснее переопределять.

```python
class Proxy:
    def __init__(self, target):
        object.__setattr__(self, '_target', target)  # обход __setattr__

    def __getattr__(self, name):
        # вызывается только если атрибут не найден в self
        return getattr(self._target, name)

    def __getattribute__(self, name):
        # вызывается ВСЕГДА — осторожно с рекурсией!
        print(f"Доступ к {name}")
        return super().__getattribute__(name)
```

Порядок поиска атрибута: data descriptors → instance `__dict__` → non-data descriptors → `__getattr__`.
</details>

---

### M2. Что произойдёт если переопределить `__eq__` без `__hash__`?

<details>
<summary>Подсказка</summary>

Python **автоматически** выставит `__hash__ = None`. Объект станет unhashable — нельзя будет положить в `set` или использовать как ключ в `dict`.

```python
class Foo:
    def __eq__(self, other): return True

f = Foo()
hash(f)     # TypeError: unhashable type: 'Foo'
{f}         # TypeError
{f: 1}      # TypeError
```

Отличие от Java: в Java `equals()` без `hashCode()` — тихий баг (ломается HashMap), объект хешируем. В Python — немедленный `TypeError`.

Решение: переопределять оба вместе:
```python
def __eq__(self, other): return self.x == other.x
def __hash__(self): return hash(self.x)
```
</details>

---

### M3. Что такое `__slots__`? Когда и зачем использовать?

<details>
<summary>Подсказка</summary>

`__slots__` — кортеж/список имён атрибутов, которые разрешены у объекта. Вместо `__dict__` Python создаёт фиксированные слоты.

Преимущества:
1. **Меньше памяти** — нет `__dict__` (словарь занимает ~200–400 байт на объект).
2. **Быстрее доступ** — атрибуты через C-уровень слотов.
3. **Защита** — нельзя добавить незадекларированный атрибут.

```python
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y): self.x, self.y = x, y

p = Point(1, 2)
p.z = 3  # AttributeError — нет слота для z
```

Ограничения:
- Несовместимо с `__dict__` (если нет явного `'__dict__'` в `__slots__`).
- При наследовании: родитель с `__slots__`, ребёнок без — у ребёнка появится `__dict__`, экономия теряется.
</details>

---

### M4. Как работает `__contains__`? Что если его не определить, а `__iter__` есть?

<details>
<summary>Подсказка</summary>

`__contains__` вызывается при `x in obj`. Если не определён, Python падает назад на `__iter__` и перебирает элементы линейно.

```python
class MySet:
    def __init__(self, data): self.data = data
    def __contains__(self, item): return item in self.data  # O(1) для set

class MyList:
    def __init__(self, data): self.data = data
    def __iter__(self): return iter(self.data)
    # нет __contains__ — Python будет итерировать: O(n)

s = MySet({1, 2, 3})
3 in s  # вызывает __contains__

l = MyList([1, 2, 3])
3 in l  # итерирует через __iter__ до нахождения: O(n)
```
</details>

---

### M5. Что такое `__call__`? Как сделать объект вызываемым?

<details>
<summary>Подсказка</summary>

`__call__` позволяет вызывать экземпляр класса как функцию.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
double(5)   # 10 — вызывает __call__
callable(double)  # True
```

Используется для: stateful callables (декораторы-классы), функторы, моки.
</details>

---

### M6. Как работают `__enter__` и `__exit__`? Когда `__exit__` подавляет исключение?

<details>
<summary>Подсказка</summary>

`with` statement — это вызов `__enter__` в начале блока и `__exit__` в конце (даже при исключении).

```python
class Transaction:
    def __enter__(self):
        print("начало транзакции")
        return self  # это присваивается переменной после as
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("commit")
        else:
            print(f"rollback: {exc_val}")
        return False  # False/None — не подавлять исключение
                      # True — подавить (исключение не пойдёт дальше)
```

`__exit__` получает три аргумента: тип, значение, traceback исключения (все `None` если исключения не было). Возврат `True` подавляет исключение.
</details>

---

### M7. Что такое интернирование строк и целых чисел? На что влияет?

<details>
<summary>Подсказка</summary>

**Интернирование** — повторное использование одного объекта вместо создания нового.

Целые числа: CPython кэширует `-5..256`. Числа вне диапазона — новые объекты.
```python
a = 256; b = 256; a is b  # True
a = 257; b = 257; a is b  # False (зависит от контекста!)
```

Строки: интернируются автоматически если "выглядят как идентификатор" (буквы, цифры, `_`). Можно принудительно через `sys.intern()`.
```python
a = "hello"; b = "hello"
a is b  # True — автоинтернирование
a = "hello world"; b = "hello world"
a is b  # False — содержит пробел
```

**Практический вывод**: никогда не используй `is` для сравнения строк и чисел в продакшне — полагаться на интернирование нельзя (деталь реализации CPython).
</details>

---

### M8. Когда вызывается `__del__`? Почему на него нельзя полагаться?

<details>
<summary>Подсказка</summary>

`__del__` вызывается когда объект собирается удалить сборщик мусора. **Не финализатор** в Java-смысле.

Проблемы:
1. Не гарантирован порядок вызова при завершении программы.
2. При циклических ссылках cyclic GC может не вызвать `__del__` вообще (в старых Python).
3. Исключения внутри `__del__` подавляются (выводятся в stderr, не пробрасываются).
4. Объект может "воскреснуть" если `__del__` создаст новую ссылку на себя.

Альтернативы:
- `contextmanager` / `with` — явный контроль жизни ресурса.
- `weakref.finalize(obj, callback)` — вызывается при удалении объекта, надёжнее.
</details>

---

## Senior

### S1. Опиши полный порядок поиска атрибута в Python (`obj.attr`). Где участвует descriptor protocol?

<details>
<summary>Подсказка</summary>

Полный алгоритм `object.__getattribute__(self, name)`:

1. Ищем `name` в `type(obj).__mro__` (цепочка классов).
2. Если нашли **data descriptor** (есть `__get__` И `__set__`/`__delete__`) — вызываем `descriptor.__get__(obj, type(obj))`.
3. Иначе ищем в `obj.__dict__`.
4. Если нашли в `__dict__` — возвращаем значение.
5. Если нашли **non-data descriptor** (только `__get__`) — вызываем `descriptor.__get__`.
6. Если нашли в классе обычный атрибут (не дескриптор) — возвращаем его.
7. Если ничего не нашли — вызываем `__getattr__` (если определён).
8. Иначе `AttributeError`.

```
MRO → data descriptor → instance __dict__ → non-data descriptor / class attr → __getattr__
```

`property` — data descriptor (`__get__` + `__set__`). Поэтому instance dict не может перекрыть property.  
Метод (функция в классе) — non-data descriptor. Поэтому `obj.method = lambda: ...` перекрывает его.

```python
class DataDesc:
    def __get__(self, obj, objtype=None): return "data"
    def __set__(self, obj, val): pass  # есть __set__ => data descriptor

class NonDataDesc:
    def __get__(self, obj, objtype=None): return "non-data"

class Foo:
    data = DataDesc()
    nondata = NonDataDesc()

f = Foo()
f.__dict__['data'] = "instance"
f.__dict__['nondata'] = "instance"

f.data     # "data" — data descriptor выиграл у instance dict
f.nondata  # "instance" — instance dict выиграл у non-data descriptor
```
</details>

---

### S2. Как работает `__set_name__`? Когда он вызывается и зачем нужен?

<details>
<summary>Подсказка</summary>

`__set_name__(self, owner, name)` вызывается Python автоматически при создании **класса** (не экземпляра!), когда дескриптор присваивается атрибуту класса.

До Python 3.6 дескриптор не знал своё имя в классе — приходилось передавать явно.

```python
class Validated:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name  # знаем куда хранить!

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.public_name} must be int")
        setattr(obj, self.private_name, value)

class MyClass:
    age = Validated()  # здесь вызывается Validated.__set_name__(MyClass, 'age')

m = MyClass()
m.age = 25   # OK
m.age = "x"  # TypeError: age must be int
```
</details>

---

### S3. Что такое `__init_subclass__` и как это альтернатива метаклассам?

<details>
<summary>Подсказка</summary>

`__init_subclass__` вызывается на **базовом классе** каждый раз, когда создаётся его подкласс. Проще метакласса для простых случаев (регистрация, валидация, настройка).

```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            Plugin._registry[plugin_name] = cls

class AudioPlugin(Plugin, plugin_name="audio"):
    pass

class VideoPlugin(Plugin, plugin_name="video"):
    pass

Plugin._registry  # {'audio': AudioPlugin, 'video': VideoPlugin}
```

Когда нужен метакласс вместо `__init_subclass__`:
- Нужно контролировать `__prepare__` (порядок атрибутов в теле класса).
- Нужно перехватывать создание самого класса (не подклассов).
- Нужна совместимость с другими метаклассами.
</details>

---

### S4. Как `__slots__` влияет на наследование? Какие ловушки?

<details>
<summary>Подсказка</summary>

```python
class Base:
    __slots__ = ('x',)

class Child(Base):
    pass  # нет __slots__ — у Child появится __dict__!

c = Child()
c.x = 1    # OK — слот от Base
c.y = 2    # OK — через __dict__ Child (экономия памяти потеряна)
```

Ловушки:
1. Если ребёнок не объявляет `__slots__` — у него будет `__dict__`, смысл `__slots__` теряется.
2. Если оба (родитель и ребёнок) объявляют одно поле — `AttributeError` при доступе (дублирующий слот).
3. Multiple inheritance: `__slots__` работает корректно только если **все** родители используют `__slots__`.

```python
class A:
    __slots__ = ('x',)

class B:
    __slots__ = ('y',)

class C(A, B):
    __slots__ = ('z',)  # OK — объединяет слоты x, y, z
    
class D(A, B):
    pass  # у D будет __dict__ — слоты A и B сохранены, но D добавит __dict__
```
</details>

---

### S5. Как работает `__class_getitem__`? Зачем он нужен?

<details>
<summary>Подсказка</summary>

`__class_getitem__` вызывается при `MyClass[something]` — то есть при subscripting класса. Используется для поддержки generic-синтаксиса.

```python
class TypedList:
    def __class_getitem__(cls, item):
        # item — это тип внутри скобок
        return f"TypedList[{item.__name__}]"

TypedList[int]     # "TypedList[int]"
TypedList[str]     # "TypedList[str]"
```

В стандартной библиотеке так работают `list[int]`, `dict[str, int]` (Python 3.9+). До 3.9 нужен был `from typing import List` — `List[int]` вызывал `__class_getitem__` на `List`.

`Generic[T]` из typing реализует `__class_getitem__` автоматически — можно писать `class Stack(Generic[T])`.
</details>

---

### S6. Как именно `type()` создаёт класс? Что происходит под капотом?

<details>
<summary>Подсказка</summary>

Когда Python видит `class Foo(Base): body`, это примерно равно:

```python
namespace = type.__prepare__('Foo', (Base,))  # 1. создать namespace (обычно dict)
exec(body, namespace)                          # 2. выполнить тело класса в namespace
Foo = type('Foo', (Base,), namespace)          # 3. создать класс через type(name, bases, dict)
```

`type.__call__` при создании класса:
1. `type.__new__(mcs, name, bases, namespace)` — создаёт объект класса.
2. `type.__init__(cls, name, bases, namespace)` — инициализирует его.

Именно поэтому метакласс — это класс, чьи экземпляры — классы.

```python
# Явный эквивалент
def my_body(ns):
    ns['x'] = 10
    ns['greet'] = lambda self: "hi"

ns = {}
my_body(ns)
MyClass = type('MyClass', (object,), ns)
MyClass.x       # 10
MyClass().greet()  # "hi"
```
</details>

---

### S7. Объясни разницу между data и non-data descriptor. Почему это важно на практике?

<details>
<summary>Подсказка</summary>

| | Data descriptor | Non-data descriptor |
|---|---|---|
| Методы | `__get__` + `__set__` (или `__delete__`) | только `__get__` |
| Приоритет | выше instance `__dict__` | ниже instance `__dict__` |
| Примеры | `property`, `__slots__` | обычные методы (функции) |

```python
class DataDesc:
    def __get__(self, obj, t): return "from descriptor"
    def __set__(self, obj, val): pass

class NonDataDesc:
    def __get__(self, obj, t): return "from descriptor"

class MyClass:
    data = DataDesc()
    nondata = NonDataDesc()

obj = MyClass()
obj.__dict__['data'] = "from dict"
obj.__dict__['nondata'] = "from dict"

obj.data     # "from descriptor" — data descriptor выиграл
obj.nondata  # "from dict" — instance dict выиграл
```

Практическая важность:
- `property` — data descriptor, поэтому `obj.prop = x` не запишет в `obj.__dict__`, а вызовет setter.
- Методы — non-data descriptors, поэтому `obj.method = lambda: ...` переопределяет метод для конкретного экземпляра (monkey patching).
</details>

---

### S8. Можно ли "воскресить" объект в `__del__`? Что происходит?

<details>
<summary>Подсказка</summary>

Да, можно — это называется object resurrection. `__del__` может создать новую ссылку на `self`.

```python
class Zombie:
    instances = []
    
    def __del__(self):
        print("умираю...")
        Zombie.instances.append(self)  # воскресение: добавляем ссылку на себя

z = Zombie()
del z        # "умираю..." — __del__ вызван, но объект добавил себя в список
Zombie.instances[0]  # объект жив!
```

После воскресения `__del__` **не будет вызван снова** при следующем удалении объекта. Python отслеживает это через `tp_finalize` в CPython.

Это считается анти-паттерном — непредсказуемо, нарушает RAII. Используй `weakref.finalize` или `contextmanager`.
</details>

---

## Быстрые вопросы (flash-cards)

1. `repr(obj)` вызывает какой метод?
2. Что возвращает `len(obj)` если `__len__` вернул отрицательное число?
3. Почему `[] == []` — True, а `[] is []` — False?
4. Что значит если `callable(obj)` — True?
5. `obj.missing_attr` — в каком порядке Python ищет атрибут?
6. Если `__bool__` не определён и `__len__` возвращает 0, то `bool(obj)` — что?
7. Чем `sys.intern("hello")` полезен в продакшне?
8. `__slots__ = ('x', 'y')` — что произойдёт при `obj.z = 1`?
9. Когда `__set_name__` вызывается — при создании класса или экземпляра?
10. Почему `is None` лучше `== None`?

<details>
<summary>Ответы</summary>

1. `__repr__`
2. `ValueError` — `len()` требует неотрицательное целое
3. Разные объекты в памяти (разные `id`), но с одинаковым значением (`__eq__`)
4. У объекта определён `__call__`
5. data descriptors в MRO → instance `__dict__` → non-data descriptors → `__getattr__`
6. `False` — Python использует `__len__` как fallback для `__bool__`
7. Экономит память если одна строка используется тысячи раз (один объект вместо тысячи)
8. `AttributeError` — слота для `z` нет
9. При создании **класса** (не экземпляра)
10. `None` — синглтон, `is` проверяет идентичность; `== None` может быть перекрыт кастомным `__eq__`
</details>
