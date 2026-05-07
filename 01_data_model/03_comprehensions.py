import collections

def main():
  print(collections.__file__)
  symbols = '$¢£¥!¤'
  codes=[]
  for symbol in symbols:
    codes.append(ord(symbol))

  # print(codes)
  codes2 = [ord(s) for s in symbols]
  # print(codes2)

  codes3 = [last:=ord(c) for c in symbols]
  # print(codes3)
  # print(last)

  colors=['white', 'black', 'red']
  size=['X', 'M', 'S']

  t_shirts=[(c, s) for c in colors for s in size]
  # print(t_shirts)
  t_shirts2=[(c, s) for s in size for c in colors]
  # print(t_shirts2)

  users = [
    {"id": 1, "name": "Alice", "age": 25, "active": True},
    {"id": 2, "name": "Bob", "age": 17, "active": False},
    {"id": 3, "name": "Charlie", "age": 30, "active": True},
    {"id": 4, "name": "Diana", "age": 22, "active": True},
  ]

  #задача. Получить массив имён активных пользователей старше 18
  #попробуем сначала в лоб:
  arr = []
  for u in users:
    if u['active']==True and u['age']>18:
      arr.append(u['name'])
  print(arr)
  active_users_18plus = [u['name'] for u in users if u['age']>18 and u['active']==True]
  print(active_users_18plus)

  user_dicts = {u['id']:u['name'] for u in users  }
  print(user_dicts)

  orders = [
    {"order_id": 101, "items": [{"name": "laptop", "price": 1000}, {"name": "mouse", "price": 20}]},
    {"order_id": 102, "items": [{"name": "keyboard", "price": 80}, {"name": "monitor", "price": 300}]},
  ]

  #создать список всех названий из всех заказов
  name_set = {i['name'] for o in orders for i in o['items']}
  name_set2 = [i['name'] for o in orders for i in cast(List[Dict[str, Any]], o.get('items', []))]
  for n in name_set:
    print(n)

  print(name_set)
  print(name_set2)

  transactions = [
    {"user": "Alice", "amount": 100, "currency": "USD"},
    {"user": "Bob", "amount": 50, "currency": "EUR"},
    {"user": "Alice", "amount": 200, "currency": "USD"},
    {"user": "Charlie", "amount": 30, "currency": "USD"},
  ]

  sum_trans = [u['amount'] for u in transactions if u['user']=='Alice']
  print(sum_trans)

  categories = [
    {"category": "electronics", "products": [{"id": 1, "name": "TV"}, {"id": 2, "name": "radio"}]},
    {"category": "books", "products": [{"id": 3, "name": "Python guide"}, {"id": 4, "name": "Java guide"}]},
  ]

  product_dict_list = [p for c in categories for p in c['products']]
  print(product_dict_list)

  orders = [
    {"order_id": 101, "items": [{"name": "laptop", "price": 1000, "qty": 1}, {"name": "mouse", "price": 20, "qty": 2}]},
    {"order_id": 102, "items": [{"name": "keyboard", "price": 80, "qty": 1}, {"name": "monitor", "price": 300, "qty": 0}]},
  ]

  sumquant = [i['price']*i['qty'] for o in orders for i in o['items']]
  #создать список общих стоимостей для товаров с кол-вом >0
  print(sumquant)


  transactions = [
    {"user": "Alice", "amount": 100, "currency": "USD"},
    {"user": "Bob",   "amount": 50,  "currency": "EUR"},
    {"user": "Alice", "amount": 200, "currency": "USD"},
    {"user": "Charlie","amount": 30, "currency": "USD"},
    {"user": "Bob",   "amount": 75,  "currency": "EUR"},
  ]

  #Задание: Построить словарь {user: total_amount} для пользователей, у которых сумма транзакций превышает 100.
  #Ограничение: Не использовать defaultdict и Counter, только dict comprehension и встроенные функции.
  sum_dict = {t.get('user'):sum([t['amount']]) for t in transactions if sum([t['amount']]) > 100}
  print(sum_dict)


if __name__=='__main__':
  main()