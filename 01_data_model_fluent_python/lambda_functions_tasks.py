from functools import reduce

'''
task1
Используя map и лямбду, возведите каждое число в квадрат
Используя filter и лямбду, оставьте только нечётные числа
Используя reduce, найдите произведение всех чисел
'''
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
def task1():

  print(list(map(lambda x: x**2, numbers)))
  print(list(filter(lambda x: x%2==0, numbers)))
  print(reduce(lambda acc, x: acc*x, numbers, 1))
  return None
'''
task2
Отсортируйте пользователей по возрасту (от младшего к старшему)
Отсортируйте пользователей по имени в обратном порядке
Отфильтруйте пользователей старше 18 лет
Отфильтруйте пользователей из NYC
Используя map, получите список имён всех пользователей
'''
users = [
  {"name": "Alice", "age": 17, "city": "NYC"},
  {"name": "Bob", "age": 25, "city": "LA"},
  {"name": "Charlie", "age": 30, "city": "NYC"},
  {"name": "Diana", "age": 22, "city": "Chicago"},
  {"name": "Eve", "age": 35, "city": "LA"},
]
def task2():
  by_age=[(user['name'], user['age']) for user in list(sorted(users, key=lambda user: user['age']))]
  print(f'По возрасту: {by_age}')
  by_name_reverse =[user['name'] for user in (sorted(users, key= lambda user: user['name'], reverse=True))]
  print(f'По имени(обратный): {by_name_reverse}')
  filter_by_age_18=[(user['name'], user['age']) for user in (filter(lambda user: user['age'] > 18, users))]
  print(f'По возрасту: {filter_by_age_18}')
  filter_by_nyc = [user['name'] for user in  list(filter(lambda user: user['city']=='NYC', users))]
  print(f'Filter by NYC: {filter_by_nyc}')
  map_names= list(map(lambda user: user['name'], users))
  print(f'Имена пользователей: {map_names}')

  return None

'''
task3
Используя match/case, обработайте каждую транзакцию:
Депозит: если сумма положительная → вывести "Deposit: {sum}", если отрицательная → "Invalid deposit amount"
Снятие (с валютой или без): если сумма <= 2000 → "Withdraw: {sum} {currency}", если больше → "Withdraw denied: limit exceeded"
Перевод: вывести "Transfer: {sum} {currency} to {account}"
Неизвестный тип: "Unknown transaction type"
Для всех успешных транзакций добавьте их в список processed_transactions
'''

transactions = [
  ("deposit", 1000),
  ("withdraw", 200, "USD"),
  ("transfer", 500, "EUR", "DE123456"),
  ("deposit", -50),  # ошибочная: отрицательный депозит
  ("withdraw", 3000, "USD"),  # превышение лимита
  ("unknown", 100),  # неизвестный тип
  ("withdraw", 100, "USD"),
]

def task3():
  processed_transactions =[]
  for tr in transactions:
    match tr:
      case ['deposit', amount]if amount>0:
        processed_transactions.append(tr)
        print(f'Deposit: {amount}')
      case['deposit', int(amount)] if amount<0:
        print('Invalid deposit amount')
      case('withdraw', amount, currency) if amount <=2000:
        processed_transactions.append(tr)
        print(f'Withdraw {amount} {currency}')
      case('withdraw', amount, currency) if amount > 2000:
        print('Withdraw denied: limit exceeded')
      case('transfer', amount, currency, account):
        processed_transactions.append(tr)
        print(f'Transfer: {amount}, {currency}, to {account}')
      case _:
        print('Unknown transaction type')

  return None



'''
task4
filter: отфильтруйте заказы со статусом "delivered"
map: для каждого доставленного заказа вычислите общую сумму (сумма price всех items)
reduce: найдите общую выручку со всех доставленных заказов
sorted: отсортируйте доставленные заказы по убыванию общей суммы
match/case: при обработке каждого заказа:
Если items пуст → вывести "Order {id}: empty"
Если status не "delivered" → вывести "Order {id}: {status}"
Если есть товар с ценой больше 500 → вывести "Order {id}: contains expensive item"
В остальных случаях → вывести "Order {id}: {total} USD"
'''
orders = [
  {"id": 1, "items": [{"name": "book", "price": 15}, {"name": "pen", "price": 2}], "status": "delivered"},
  {"id": 2, "items": [{"name": "laptop", "price": 1000}], "status": "delivered"},
  {"id": 3, "items": [{"name": "phone", "price": 500}, {"name": "case", "price": 20}], "status": "delivered"},
  {"id": 4, "items": [], "status": "cancelled"},
  {"id": 5, "items": [{"name": "book", "price": 15}, {"name": "book", "price": 15}], "status": "delivered"},
]
def task4():
  delivered = list(filter(lambda order: order['status']=='delivered', orders))
  print(f'delivered={delivered}')
  sum_pr = [(f'Order {order['id']}:', f'{sum(item['price'] for item in order['items'])} USD') for order in delivered]
  sum_prices= list(map(lambda order: sum(item['price'] for item in order['items']), delivered))
  print(f'sum_prices = {sum_pr}')
  print(f'sum_prices2={sum_prices}')
  sum_all_prices= reduce(lambda acc, order: acc+sum(item['price'] for item in order['items']), delivered, 0)
  print(sum_all_prices)
  sorted_delivered = sorted((sum(item['price'] for item in order['items']) for order in delivered), reverse=True)
  print(sorted_delivered)

  for order in orders:
    match order:
      case {'id':id, 'items':[], 'status':status}:
        print(f'Order {id} is {status}')
      case {'id':id, 'status':status,  **extra} if status != 'delivered':
        print(f'Order {id} is {status}')
      case{'id':id, 'items':items, 'status':status} if any(item['price'] > 500 for item in items):
        print("Too expensive")
      case {'id':id, 'items':items, 'status':status}:
        total = reduce(lambda acc, _: acc+sum(item['price'] for item in items), delivered, 0)
        print(f'Order {id}: {total} USD')





  return None

if __name__ == '__main__':
    task1()
    task2()
    task3()
    task4()
