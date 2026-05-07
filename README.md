# Python Core подготовка к собесу — структура повторения

---

## 1. Data Model и объектная модель Python [понять] [задачи] [глубина]

- Всё — объект: id, type, value; разница `is` vs `==`; интернирование (int, str).
- Специальные методы: `__repr__`, `__str__`, `__eq__`, `__hash__`, `__bool__`, `__len__`, `__contains__`.
- `__getattr__` vs `__getattribute__` vs `__setattr__` vs `__delattr__`: порядок вызова, ловушки.
- `__call__`, `__enter__`/`__exit__`, `__del__` и когда он вызывается (предостережение).
- `__slots__`: зачем, влияние на память и наследование, несовместимость с `__dict__`.
- `__init_subclass__`, `__set_name__`, `__class_getitem__` — метахуки без метаклассов.

## 2. Функции и замыкания [понять] [задачи] [глубина]

- First-class functions: передача, возврат, хранение; `__code__`, `__closure__`, `__defaults__`.
- Замыкания: ячейки (cell objects), `nonlocal`, классическая ловушка с циклом и `lambda`.
- Аргументы: positional/keyword, `*args/**kwargs`, keyword-only (после `*`), positional-only (до `/` в Python 3.8+).
- `functools`: `wraps`, `partial`, `lru_cache`/`cache`, `reduce`, `total_ordering`, `singledispatch`.
- `operator`: `attrgetter`, `itemgetter`, `methodcaller`.

## 3. Декораторы и метапрограммирование [понять] [задачи] [глубина]

- Декоратор без аргументов, с аргументами, class-based декоратор.
- Цепочка декораторов: порядок применения (bottom-up) и порядок вызова (top-down).
- `functools.wraps` — зачем нужен, что копирует (`__name__`, `__doc__`, `__wrapped__`).
- `@singledispatch`, `@singledispatchmethod`.
- Дескрипторы: `__get__`/`__set__`/`__delete__`; data vs non-data descriptor; порядок поиска атрибута (MRO → instance dict → class dict → descriptor).
- `property`, `classmethod`, `staticmethod` — как дескрипторы под капотом.
- Практика: написать `retry(n, exceptions)`, `singleton`, `timing`, `cached_property`, `access_log`.

## 4. ООП и наследование [понять] [задачи] [глубина]

- MRO (Method Resolution Order): C3 linearization, `super()`, порядок вызовов в diamond.
- `type()` как метакласс; как Python создаёт класс (`__prepare__`, `__new__`, `__init__` у type).
- Метаклассы: когда нужны, `__new__` vs `__init__`, автоматическая регистрация классов.
- ABC (`abc.ABC`, `abstractmethod`, `abstractclassmethod`, `__subclasshook__`, `instancecheck`).
- `dataclasses`: `__post_init__`, `field(default_factory)`, `frozen`, `KW_ONLY`, сравнение с `NamedTuple`/`TypedDict`.
- `__init_subclass__` как альтернатива метаклассу.

## 5. Итераторы, генераторы, контекстные менеджеры [понять] [задачи]

- Итерируемый vs итератор: `__iter__`/`__next__`, `StopIteration`.
- Генераторные функции: `yield`, `yield from`, `send()`, `throw()`, `close()`; состояние стека.
- Генераторные выражения vs list/dict/set comprehensions: ленивость, memory footprint.
- `itertools`: `chain`, `islice`, `groupby`, `product`, `permutations`, `accumulate`, `takewhile/dropwhile`.
- Context managers: `__enter__`/`__exit__`, `contextlib.contextmanager`, `asynccontextmanager`, `suppress`, `ExitStack`, `nullcontext`.
- `with` и exception propagation: когда `__exit__` подавляет исключение.

## 6. Typing и аннотации [понять] [задачи]

- Базовые: `Optional`, `Union`, `Any`, `Literal`, `Final`, `ClassVar`, `Type`.
- Дженерики: `TypeVar`, `Generic`, `ParamSpec`, `Concatenate`, `TypeVarTuple`.
- `Protocol` vs ABC: structural subtyping (duck typing статически), `runtime_checkable`.
- `overload`, `TypeGuard`, `Annotated`, `get_type_hints()`.
- `mypy`/`pyright` в strict mode: что проверяется, как работает type narrowing.
- `dataclasses` + `TypedDict` + `NamedTuple` — когда что выбрать.

## 7. Память и управление объектами [понять] [глубина]

- Reference counting: `sys.getrefcount()`, когда объект удаляется, cyclic references.
- Cyclic GC: три поколения (`gc.get_count()`), `gc.collect()`, `gc.disable()`.
- `weakref`: `WeakValueDictionary`, `WeakSet`, `ref()`, `finalize()` — использование в кэшах.
- `__del__`: ненадёжность, альтернативы (`weakref.finalize`, `contextmanager`).
- `sys.getsizeof()`, `tracemalloc`: профилирование памяти.
- Интернирование строк: `sys.intern()`, когда и зачем.
- Small int cache (-5..256), string interning автоматически.

## 8. Конкурентность [понять] [задачи] [глубина]

- GIL глубоко: что он защищает, когда освобождается (I/O, C-extensions), check interval (`sys.getswitchinterval`).
- `threading`: `Thread`, `Lock`, `RLock`, `Semaphore`, `Event`, `Condition`, `Barrier`, `local()`.
- `multiprocessing`: Process, Pool, Queue, Pipe, shared memory, `Manager`.
- `concurrent.futures`: `ThreadPoolExecutor`, `ProcessPoolExecutor`, `Future`, `as_completed`, `wait`.
- CPU-bound vs I/O-bound: что выбрать и почему.
- `asyncio`: event loop, coroutines vs callbacks, `Task`, `gather`, `wait`, `shield`, `Semaphore`, `Queue`.
- `asyncio` ловушки: блокирующий вызов в корутине, `run_in_executor`, `CancelledError`.
- `TaskGroup` (Python 3.11+) и structured concurrency.
- `asyncio.Protocol`/`Transport` — низкоуровневый async I/O.

## 9. Async и asyncio глубже [понять] [задачи]

- `await` под капотом: отправка в event loop, `__await__`, `send(None)`.
- `aiohttp`, `httpx`, `aiomysql` — async-экосистема обзорно.
- Отличие от trio / anyio — структурная конкурентность.
- `uvloop` — почему быстрее стандартного event loop.
- Дебаг asyncio: `asyncio.set_event_loop_policy`, `asyncio.get_event_loop`, логирование медленных callbacks.

## 10. Import system и пакеты [понять] [глубина]

- Механизм поиска: `sys.path`, finders (`PathFinder`, `MetaPathFinder`), loaders.
- `importlib`: `import_module`, `reload`, `find_spec`.
- Relative imports: когда работают, когда ломаются.
- Circular imports: причины, способы решения (перенести import внутрь функции, реструктуризация).
- `__init__.py`, `__all__`, `__package__`, `__spec__`.
- `pkgutil`, `importlib.resources` — ресурсы пакета.

## 11. Стандартная библиотека: важное [понять] [задачи]

- `collections`: `defaultdict`, `OrderedDict`, `Counter`, `deque`, `ChainMap`, `namedtuple`.
- `pathlib`: `Path` API vs `os.path`; почему предпочитать.
- `enum`: `Enum`, `IntEnum`, `Flag`, `auto()`, кастомные методы.
- `logging`: уровни, handlers, formatters, `LoggerAdapter`, `structlog` обзорно.
- `argparse` / `click` обзорно.
- `re`: compile, groups, named groups, lookahead/lookbehind, `re.VERBOSE`.
- `json`, `pickle`, `csv`, `configparser`, `tomllib` (3.11+).
- `datetime`: naive vs aware, `timezone`, `zoneinfo` (3.9+).

## 12. Производительность и профилирование [понять] [задачи]

- `cProfile` / `profile`: как запускать, читать вывод, `pstats`.
- `line_profiler`, `memory_profiler` — построчное профилирование.
- `timeit` — микробенчмарк.
- Узкие места: атрибутный доступ, `global` lookup, list vs generator, local variables быстрее global.
- `__slots__` влияние на производительность.
- `numpy` vectorization vs Python loops — порядки разницы.
- `Cython`, `ctypes`, `cffi` обзорно — когда и как расширить CPython.

## 13. Тестирование [понять] [задачи]

- `pytest`: fixtures, parametrize, marks, conftest.py.
- `unittest.mock`: `Mock`, `MagicMock`, `patch`, `patch.object`, `side_effect`, `spec`.
- Тестирование async: `pytest-asyncio`, `anyio`.
- Тестирование с БД: `pytest-django` / `SQLAlchemy` fixtures.
- Property-based testing: `hypothesis` обзорно.
- Coverage: `pytest-cov`, что такое branch coverage.

## 14. Инструменты и экосистема [понять]

- Управление зависимостями: `pip`, `poetry`, `uv` (новый, быстрый), `pyproject.toml` vs `setup.py`.
- Виртуальные окружения: `venv`, `virtualenv`, `.python-version` (pyenv).
- Линтеры/форматтеры: `ruff` (заменяет flake8+isort+black), `black`, `mypy`/`pyright`.
- `pre-commit` хуки.
- `pdb` / `ipdb` — отладка; `breakpoint()` (3.7+).

## 15. Python для ML (специфика) [понять] [задачи]

- `numpy`: ndarray, broadcasting, view vs copy, `dtype`, memory layout (C vs Fortran order).
- `pandas`: `DataFrame`/`Series`, `groupby`, `merge`, NA handling, `apply` vs vectorized ops.
- Ленивые вычисления: `dask` обзорно.
- `scikit-learn` API: estimator, transformer, pipeline.
- `PyTorch` / `TensorFlow`: autograd, `Dataset`/`DataLoader`, training loop.
- `joblib`: параллелизм для ML, сериализация больших объектов.

---

Блоки с [задачи] — практические упражнения руками; [глубина] — разбирать внутренности CPython, память, GIL.

---

### Неделя 1: Data Model + функции + замыкания

- Изучить: разделы 1–2 (data model, special methods, closures, functools).
- Практика: реализовать кастомный `Vector` с арифметикой через `__add__`/`__mul__`/`__abs__`; написать `lru_cache` вручную без `functools`.
- Проверка: объяснить вслух, почему `__getattr__` vs `__getattribute__`, ловушка с замыканием в цикле.

### Неделя 2: Декораторы + дескрипторы + ООП/MRO

- Изучить: разделы 3–4 (decorators, descriptors, metaclasses, dataclasses, ABC).
- Практика: написать `retry(n, exceptions)`, `singleton`, class-based декоратор; реализовать `property` через дескриптор вручную; метакласс-реестр классов.
- Проверка: нарисовать MRO для diamond-иерархии; объяснить data vs non-data descriptor.

### Неделя 3: Итераторы + генераторы + контекстные менеджеры

- Изучить: раздел 5 (iterators, generators, contextlib, itertools).
- Практика: бесконечный генератор Фибоначчи, `yield from` для обхода дерева, `ExitStack` для нескольких ресурсов, `@contextmanager` для db-транзакции.
- Проверка: объяснить `send()` и `throw()` у генератора; когда `__exit__` подавляет исключение.

### Неделя 4: Typing + память + import system

- Изучить: разделы 6–7, 10 (typing, Protocol, memory, GC, import).
- Практика: написать `Protocol` для duck typing, добавить strict mypy в проект, профилировать `tracemalloc`, воспроизвести circular import и починить.
- Проверка: объяснить `TypeVar` vs `ParamSpec`; когда `WeakValueDictionary` вместо обычного dict.

### Неделя 5: Конкурентность + asyncio

- Изучить: разделы 8–9 (GIL, threading, multiprocessing, asyncio, TaskGroup).
- Практика: producer-consumer на `asyncio.Queue`, `ThreadPoolExecutor` для I/O-bound, `ProcessPoolExecutor` для CPU-bound, `asyncio.shield` в cancel-сценарии.
- Проверка: когда GIL не защищает; разница `gather` vs `TaskGroup`; как отлаживать медленный event loop.

### Неделя 6: stdlib + производительность + тестирование

- Изучить: разделы 11–13 (collections, pathlib, logging, cProfile, pytest, mock).
- Практика: написать полный тест-сьют с фикстурами и `patch`; профилировать мини-скрипт и найти узкое место; написать custom `logging.Handler`.
- Проверка: `Counter` vs `defaultdict` — когда что; `MagicMock` vs `Mock` — разница.

### Неделя 7–8: ML-специфика + mock-собесы

- Изучить: раздел 15 (numpy internals, pandas, sklearn API, PyTorch pipeline).
- Практика: реализовать линейную регрессию без sklearn (numpy only); написать кастомный `sklearn.Pipeline`-шаг.
- Проверка: 20 senior-вопросов вслух (GIL, metaclass, asyncio internals, descriptor, Protocol).

### Что проверять после каждой недели

- Объяснить 3–5 концептов вслух, как на собесе, без заглядывания.
- Написать код без подсказок: один из задачных примеров недели с нуля.
- Разобрать один реальный open-source PR на Python и объяснить каждое решение.

### Ресурсы

- **Fluent Python** (Ramalho, 3rd ed.) — главная книга, читать параллельно.
- **Effective Python** (Slatkin) — конкретные советы по идиоматике.
- Exercism.io Python track — без ИИ, с ревью.
- LeetCode medium/hard с фокусом на Pythonic solutions.
- CPython source на GitHub — читать `Objects/`, `Lib/functools.py` и т.д.


---------------------------------

## Дополнительные файлы

- [`weekly_checklist.md`](./weekly_checklist.md) — чеклист по каждой неделе: "Могу объяснить X" и "Могу написать Y" без ИИ.
- [`pitfalls_java.md`](./pitfalls_java.md) — подводные камни для Java-разработчика: GIL, мутируемые дефолты, `is` vs `==`, замыкания, `__hash__` и т.д.

---

## Структура python-core:
```bash
python-core/
  README.md
  weekly_checklist.md   # прогресс и чеклист
  pitfalls_java.md      # ловушки для Java-разработчика
  01_data_model/
    notes.md            # конспект: что изучил, ловушки
    example_1.py        # примеры из теории
    practice.py         # задачи, которые ты решал руками
    test_practice.py    # тесты на свои решения
  02_functions/
    ...
  03_decorators/
    ...
```
