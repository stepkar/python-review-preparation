items = [1, 2, 3, 4, 5]
test = items[:-5:-1]
print(test)
reversed_items = items[::-1]
print(reversed_items)  # [5, 4, 3, 2, 1]

slice(0, 3)

text = "Python"
# reversed_text = ...
# print(reversed_text)   # "nohtyP"


numbers = [10, 20, 30, 40, 50, 60, 70, 80]
# Ваш код

original = [1, 2, 3, 4, 5, 6]
# Ваш код
print(original)  # [1, 2, 100, 200, 5, 6]


filepath = "/home/user/docs/example.txt"
# filename = ???
# extension = ???
# print(filename)  # "example"
# print(extension) # "txt"

def remove_by_slice(lst, k):
  # ваш код
  pass

print(remove_by_slice([10, 20, 30, 40, 50], 2))  # [10, 20, 40, 50]
print(remove_by_slice([10, 20], 0))              # [20]
print(remove_by_slice([10, 20], 5))              # [10, 20] (индекс вне границ)


def main():
  pass


if __name__ == '__main__':
  main()