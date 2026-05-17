
a, b=0,1

for i in range(0, 50):
  print(a)
  a,b = b, a+b



if __name__ == '__main__':
    a, b = 0, 1
    a = b
    b = a+b
