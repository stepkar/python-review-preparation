import dis

if __name__ == '__main__':
    a= (1, 2, 3)
    print(f'Tuple_size_of_three: {a.__sizeof__()}')
    b=[1, 2, 3]
    b.append(4)
    b.append(5)
    print(f'List_size_of_three: {b.__sizeof__()}')
    a= ()

    c = tuple(b)
    d = tuple(b)
    dis_dis = dis.dis(d)
    print(dis_dis)
    a = (1)
    b = (1)
    print(a is b)
    print(c is d)
    print(c == d)
    print(([1]) is ([1]))



