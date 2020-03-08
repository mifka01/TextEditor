y = [1, 2]


def x(y):
    print(y)
    o = y
    print(o)
    for x in o:
        print(o)
        print(x)
        delete(y)
        print(o)


def delete(y):
    y.pop(0)
 

x(y)