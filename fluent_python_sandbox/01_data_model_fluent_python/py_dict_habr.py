"""
Заглядываем внутрь dict в CPython 3.14 (GIL build).

Раскладка PyDictObject:
    ob_refcnt, ob_type, ma_used, ma_version_tag, ma_keys, ma_values

Раскладка PyDictKeysObject (GIL build, 3.13/3.14):
    Py_ssize_t dk_refcnt;
    uint8_t    dk_log2_size;          // 1<<dk_log2_size = число слотов sparse-таблицы
    uint8_t    dk_log2_index_bytes;   // log2(РАЗМЕР ВСЕГО dk_indices В БАЙТАХ), минимум SIZEOF_VOID_P
    uint8_t    dk_kind;               // 0 GENERAL, 1 UNICODE, 2 SPLIT (устар.)
    uint32_t   dk_version;            // монотонный счётчик мутаций
    Py_ssize_t dk_usable;             // свободные слоты в dense
    Py_ssize_t dk_nentries;           // занятые слоты в dense
    char       dk_indices[];          // sparse-таблица
    // далее лежит dense-массив: PyDictUnicodeEntry или PyDictKeyEntry
    //
    // Размер ОДНОГО слота индекса определяется через dk_size:
    //   dk_size <= 0xFF        -> 1 байт  (int8_t)
    //   dk_size <= 0xFFFF      -> 2 байта (int16_t)
    //   dk_size <= 0xFFFFFFFF  -> 4 байта (int32_t)
    //   иначе                  -> 8 байт  (int64_t)
    // Общий блок dk_indices = 1 << dk_log2_index_bytes (минимум SIZEOF_VOID_P=8).
    // dk_entries начинается ровно после dk_indices: indices_addr + (1 << dk_log2_index_bytes).

В free-threaded сборке (python3.14t) добавлен дополнительный мьютекс — здесь его нет.
"""

import ctypes
import sys
import sysconfig


# uint8 + uint8 + uint8 + (pad 1) + uint32 уложатся в 8 байт без _pack_,
# но _pack_ = 0 (default) уже даст native alignment, что нам и нужно.
class PyDictKeysObject(ctypes.Structure):
    _fields_ = [
        ("dk_refcnt",           ctypes.c_ssize_t),
        ("dk_log2_size",        ctypes.c_uint8),
        ("dk_log2_index_bytes", ctypes.c_uint8),
        ("dk_kind",             ctypes.c_uint8),
        # 1 байт padding до uint32 поставит сам ctypes
        ("dk_version",          ctypes.c_uint32),
        ("dk_usable",           ctypes.c_ssize_t),
        ("dk_nentries",         ctypes.c_ssize_t),
    ]


# kind == 1 (UNICODE): только key+value, хеш берётся из PyUnicodeObject
class PyDictUnicodeEntry(ctypes.Structure):
    _fields_ = [
        ("me_key",   ctypes.c_void_p),
        ("me_value", ctypes.c_void_p),
    ]


# kind == 0 (GENERAL): полная запись с хешем
class PyDictKeyEntry(ctypes.Structure):
    _fields_ = [
        ("me_hash",  ctypes.c_ssize_t),
        ("me_key",   ctypes.c_void_p),
        ("me_value", ctypes.c_void_p),
    ]


DKIX_EMPTY = -1
DKIX_DUMMY = -2

KIND_NAMES = {0: "GENERAL", 1: "UNICODE", 2: "SPLIT"}


def safe_repr(ptr, maxlen=30):
    if not ptr:
        return "NULL"
    try:
        obj = ctypes.cast(ptr, ctypes.py_object).value
        r = repr(obj)
        return r if len(r) <= maxlen else r[: maxlen - 1] + "…"
    except Exception:
        return f"<0x{ptr:x}>"


def fmt_index(x):
    if x == DKIX_EMPTY:
        return " . "
    if x == DKIX_DUMMY:
        return " X "
    return f"{x:3d}"


def dict_internals(d: dict):
    assert isinstance(d, dict)

    print("=" * 100)
    print(f"DICT @ 0x{id(d):x}  len={len(d)}")

    # ma_keys: 5-й указатель в PyDictObject (после refcnt, type, ma_used, ma_version_tag).
    ob = ctypes.cast(id(d), ctypes.POINTER(ctypes.c_void_p))
    keys_addr = ob[4]
    keys = ctypes.cast(keys_addr, ctypes.POINTER(PyDictKeysObject)).contents

    dk_size = 1 << keys.dk_log2_size
    indices_total_bytes = 1 << keys.dk_log2_index_bytes  # размер ВСЕГО блока dk_indices
    if dk_size <= 0xFF:
        slot_bytes, index_ctype = 1, ctypes.c_int8
    elif dk_size <= 0xFFFF:
        slot_bytes, index_ctype = 2, ctypes.c_int16
    elif dk_size <= 0xFFFFFFFF:
        slot_bytes, index_ctype = 4, ctypes.c_int32
    else:
        slot_bytes, index_ctype = 8, ctypes.c_int64
    kind = keys.dk_kind

    print(
        f"ma_keys=0x{keys_addr:x} | kind={kind} ({KIND_NAMES.get(kind, '?')}) | "
        f"dk_log2_size={keys.dk_log2_size} (dk_size={dk_size}) | "
        f"slot={slot_bytes}B, dk_indices block={indices_total_bytes}B | "
        f"dk_usable={keys.dk_usable} | dk_nentries={keys.dk_nentries} | "
        f"dk_version={keys.dk_version}"
    )

    # --- SPARSE: dk_indices сразу за заголовком ---
    indices_addr = ctypes.addressof(keys) + ctypes.sizeof(PyDictKeysObject)
    indices = (index_ctype * dk_size).from_address(indices_addr)

    print(f"\nSPARSE dk_indices @ 0x{indices_addr:x} (всего {dk_size} слотов):")
    print("  [" + " ".join(fmt_index(int(x)) for x in indices) + "]")
    print("  легенда: ' . ' = EMPTY(-1), ' X ' = DUMMY(-2), число = индекс в dense")

    # --- DENSE: ровно через indices_total_bytes байт после начала dk_indices ---
    entries_addr = indices_addr + indices_total_bytes
    if kind == 0:
        EntryT = PyDictKeyEntry
    else:
        EntryT = PyDictUnicodeEntry
    entries = (EntryT * keys.dk_nentries).from_address(entries_addr)

    print(f"\nDENSE entries @ 0x{entries_addr:x} (тип={EntryT.__name__}, "
          f"размер записи={ctypes.sizeof(EntryT)} байт, всего={keys.dk_nentries}):")
    for i in range(keys.dk_nentries):
        e = entries[i]
        if kind == 0:
            print(f"  [{i:2d}] hash={e.me_hash:>20d}  "
                  f"key={safe_repr(e.me_key):32}  value={safe_repr(e.me_value)}")
        else:
            print(f"  [{i:2d}] key={safe_repr(e.me_key):32}  "
                  f"value={safe_repr(e.me_value)}")

    print()


if __name__ == "__main__":


    h = hash('some_key')
    print(h)
    print()

    assert sysconfig.get_config_var("Py_GIL_DISABLED") in (0, None), (
        "Этот скрипт рассчитан на GIL-сборку CPython. "
        "Для python3.14t раскладка PyDictKeysObject другая."
    )
    print(f"Python {sys.version}")

    d = {}
    for i in range(12):
        d[f"key{i}"] = i * 100
        dict_internals(d)
        input("Enter для следующего шага... ")

    print("\n--- удалим пару ключей, чтобы увидеть DUMMY (-2) в sparse ---")
    del d["key3"]
    del d["key7"]
    dict_internals(d)
