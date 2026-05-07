metro_areas = [
  ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
  ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
  ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
  ('New York-Newark', 'US', 20.104, (40.808611,-74.020386)),
  ('São Paulo', 'BR', 19.649, (-23.547778,-46.635833)),
]
requests = [
  ("GET", "/home", {}, 200),
  ("POST", "/api/users", {"Content-Type": "application/json"}, 201),
  ("GET", "/about", {}, 404),
  ("DELETE", "/api/session", {"Authorization": "Bearer token"}, 204),
  ("POST", "/api/login", {}, 401),
]
transactions = [
  ("pay", 100, "USD"),
  ("pay", 250, "EUR"),
  ("refund", 50, "USD"),
  ("pay", 300, "GBP"),
  ("refund", 20, "EUR"),
]
users = [
  {"name": "Alice", "age": 30, "role": "admin", "email": "alice@example.com"},
  {"name": "Bob", "age": 17, "role": "user", "email": "bob@example.com"},
  {"name": "Charlie", "age": 25, "role": "moderator", "email": None},
  {"name": "Diana", "age": 22, "role": "user", "email": "diana@example.com"},
]
def main():
  # for record in metro_areas:
  #   match record:
  #     case[name, *_, (lat,lon)] if lon<=0:
  #       print(f'{name:15}|{lat:9.4f}|{lon:9.4f}')
  for record in transactions:
    match record:
      case ['pay', amount, currency] if amount >100:
        print(f'Payed {amount} {currency}')

  for user in users:
    match user:
      case{'role':'user', 'age':age, 'email':email, **rest}if age>18 and email is not None:
        print(f'{rest.get("name")},age:{age}, role:user, email:{email}')
      case{'role':'admin', **rest}:
        print(f'{rest.get("name")},age:{rest.get("age")}, role:admin, {rest.get("email")}')
      case{'email':None, **rest}:
        print(f'{rest.get("name")} has no email')


  requests = [
    ("GET", "/home", {}, 200),
    ("POST", "/api/users", {"Content-Type": "application/json"}, 201),
    ("GET", "/about", {}, 404),
    ("DELETE", "/api/session", {"Authorization": "Bearer token"}, 204),
    ("POST", "/api/login", {}, 401),
  ]

  for request in requests:
    match request:
      case ('GET', path, _, 200) |('POST', path, _, 201):
        print(f'Success: {path}')
      case ("DELETE", path, _, _):
        print(f"Deleted: {path}")
      case (_, path, _, status) if 400 <= status < 500:
        print(f"Client error: {status} on {path}")



if __name__ == "__main__":
  main()