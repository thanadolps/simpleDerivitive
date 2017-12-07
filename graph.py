from abc import ABCMeta, abstractmethod
from typing import Union
from math import log

# TODO [later] : Format __str__ output algorithum
# TODO [later] : Optimize Graph Calculation - mainly duplication reusing
# TODO : Add More Function

Number = Union[int,float]


class Graph(metaclass=ABCMeta):

    @abstractmethod
    def eval(self, dic) -> Number:
        raise NotImplementedError('users must define eval to use this base class')

    @abstractmethod
    def gradient(self, dic, var):
        raise NotImplementedError('users must define gradient to use this base class')

    @staticmethod
    def constancy(x):
        if isinstance(x, Graph):
            return x
        else:
            return Constance(x)

    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __pow__(self, power, modulo=None):
        return Pow(self, power)



GraphInput = Union[Number, Graph]


class Variable(Graph):

    def __init__(self, name='[default_var_name]'):
        self.name = name

    def eval(self, dic):

        x = dic.get(self)

        if x == None:
            raise ValueError("input dictionary doesn't contain value for {} {}".format(self.name, x))

        return x


    def gradient(self, dic, var):

        # x' = 1, k' = 0
        if self == var:
            return 1
        else:
            return 0

    def __str__(self):
        return str(self.name)


class Constance(Graph):

    def __init__(self, x: Number):
        self.x = x

    def eval(self, dic):
        return self.x

    def gradient(self, dic , var):
        # k' = 0
        return 0

    def __str__(self):
        return str(self.x)


class Add(Graph):

    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) + self.g2.eval(dic)

    def gradient(self, dic , var):
        return self.g1.gradient(dic, var) + self.g2.gradient(dic, var)

    def __str__(self):
        return "{} + {}".format(self.g1, self.g2)


class Sub(Graph):

    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) - self.g2.eval(dic)

    def gradient(self, x : Number, var):
        return self.g1.gradient(x, var) - self.g2.gradient(x, var)

    def __str__(self):
        return "{} - {}".format(self.g1, self.g2)


class Mul(Graph):
    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) * self.g2.eval(dic)

    def gradient(self, dic, var):
        # fg' + f'g
        return self.g1.eval(dic) * self.g2.gradient(dic, var) + self.g1.gradient(dic, var) * self.g2.eval(dic)

    def __str__(self):
        return "({}) * ({})".format(self.g1, self.g2)


class Div(Graph):
    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) / self.g2.eval(dic)

    def gradient(self, dic, var):
        return self.g1.eval

    def __str__(self):
        return "({}) / ({})".format(self.g1, self.g2)


class Pow(Graph):
    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) ** self.g2.eval(dic)

    def gradient(self, dic, var):

        f = self.g1.eval(dic)
        fd = self.g1.gradient(dic, var)
        g = self.g2.eval(dic)
        gd = self.g2.gradient(dic, var)

        # https://www.wolframalpha.com/input/?i=Differential+(f(x))%5Eg(x)
        return (f**(g-1)) * (g * fd + (0 if not isinstance(f, Graph) else (f * log(f) * gd)))

    def __str__(self):
        return "({}) ^ ({})".format(self.g1, self.g2)






