from graph import *
from time import clock
from matplotlib import pyplot

x   =  Variable('x')
y   =  Variable('y')
a1  =  x**3 * 3

def f(x):
    return x**3 * 3
h = 10**-10

L = []

print(a1.gradient({x:3}, x))

for i in range(2, 1000) :
    param = {x : i}
    print("{}".format(param[x]))
    print("eval : {}".format(a1.eval(param)))
    tt = clock()
    V1 = a1.gradient(param, x)
    T1 = clock()-tt
    print("grad : {}".format(V1))



    tt = clock()
    V2 = (f(i + h) - f(i)) / h
    T2 = clock()-tt

    print("Nu G : {}".format(V2))
    print("gradT: {}s".format(T1))
    print("NGT  : {}s".format(T2))
    L.append(abs((T2-T1)/(V1-V2)))
    print("Cost : {}s\n".format(L[-1]))
    #T =

print('\n' + str(a1))

#L = L[:]

print("avarge cost -> " + str(sum(L)/len(L)))

pyplot.plot(L)
pyplot.show()
pyplot.close()



