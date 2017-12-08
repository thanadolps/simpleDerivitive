from graph import *
from Parse import parse

if False:
    x   =  Variable('x')
    y   =  Variable('y')
    z   =  Variable('z')
    A   =  x + y * z

    param = {x : 2, y : 1, z : 3}

    print(A.eval(param))
    print(A.gradient(param, x))
    print(A)
else:
    G = parse(input())





