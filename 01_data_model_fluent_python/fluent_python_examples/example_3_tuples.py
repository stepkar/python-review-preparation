from dis import dis

def main():
  a = (10, 20, 30)
  b = a
  print(a is b)

  c = tuple(a)
  print(b is c)
  print(b == c)

  d = [10, 20, 30]
  e = d
  f = list(d)
  print(d is e)
  print(d is f)

  dis(compile("a = (10, 'abc')", '', 'exec'))



if __name__ == "__main__":
  main()