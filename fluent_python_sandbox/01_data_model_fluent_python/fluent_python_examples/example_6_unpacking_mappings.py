def dump(**kwargs):
  return kwargs


if __name__ == '__main__':
    print(dump(**{'x':1}, y=2, **{'z':3}))
    b1 = dict(api=1, author='Douglas Hofstadter', type='book', title='Gödel, Escher, Bach')
    print(b1)
