from abc import ABCMeta, abstractmethod
from typing import Union, List
from math import log
from functools import reduce

# TODO [later][Hard] : Optimize Graph Calculation - mainly duplication reusing
# TODO [later] : Optimize Graph Calculation - coefficient combining
# TODO [main] : auto derivative graph -> construct new derivative graph using current graph
# TODO : Add More Function

Number = Union[int, float]


class Graph(metaclass=ABCMeta):

    @abstractmethod
    def eval(self, dic) -> Number:
        raise NotImplementedError('users must define eval to use this base class')

    @abstractmethod
    def gradient(self, dic, var):
        raise NotImplementedError('users must define gradient to use this base class')

    @abstractmethod
    def childs(self):
        raise NotImplementedError('users must define childs to use this base class')

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

tree_sep = '|-- '
def draw_tree(graph : Graph, layer = 1):

    print(f"{tree_sep:>{len(tree_sep)*layer}}{repr(graph)}")

    if graph.childs() is not None:
        for g in graph.childs():
            draw_tree(g, layer + 1)


GraphInput = Union[Number, Graph]


class Variable(Graph):

    def __init__(self, name='[default_var_name]'):
        self.name = name

    def eval(self, dic):

        x = dic.get(self)

        if x is None:
            raise ValueError("input dictionary doesn't contain value for {} {}".format(self.name, x))

        return x

    def gradient(self, dic, var):

        # x' = 1, k' = 0
        if self == var:
            return 1
        else:
            return 0

    def childs(self):
        return None

    def __repr__(self):
        return "Variable {}".format(self.name)

    def __str__(self):
        return str(self.name)


class Constance(Graph):

    def __init__(self, x: Number):
        self.x = x

    def eval(self, dic):
        return self.x

    def gradient(self, dic, var):
        # k' = 0
        return 0

    def childs(self):
        return None

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)


def brace(x):
    return ("{}" if isinstance(x, Variable) or isinstance(x, Constance) else "({})").format(x)


class Add(Graph):

    def __init__(self, *args):
        self.g = []

        for i in args:
            if isinstance(i, Add):
                self.g += i.g
            else:
                self.g.append(self.constancy(i))

    def eval(self, dic) -> Number:
        return sum(map(lambda x: x.eval(dic), self.g))

    def gradient(self, dic, var):
        return sum(map(lambda x: x.gradient(dic, var), self.g))

    def childs(self):
        return self.g

    def __repr__(self):
        return "Add"

    def __str__(self):
        return " + ".join(map(lambda x : str(x), self.g))


class Sub(Graph):

    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) - self.g2.eval(dic)

    def gradient(self, x : Number, var):
        return self.g1.gradient(x, var) - self.g2.gradient(x, var)

    def childs(self):
        return self.g1, self.g2

    def __repr__(self):
        return "Sub"

    def __str__(self):
        return "{} - {}".format(self.g1, brace(self.g2))


class Mul(Graph):
    def __init__(self, g1: Graph , g2: Graph, *args):
        self.g : List[Graph] = []

        self.add(g1)
        self.add(g2)
        for i in args:
            self.add(i)

    def add(self, x):
            if isinstance(x, Mul):
                self.g += x.g
            else:
                self.g.append(self.constancy(x))

    def eval(self, dic) -> Number:
        return reduce(lambda x, y : x * y, map(lambda x : x.eval(dic), self.g))

    def gradient(self, dic, var):

        all_mult = self.eval(dic)  # = fgh

        # fgh      fgh      fgh
        # --- f' + --- g' + --- h'
        #  f        g        h
        return sum(map(lambda x : x.gradient(dic, var) * all_mult / x.eval(dic), self.g))

    def childs(self):
        return self.g

    def __repr__(self):
        return "Mul"

    def __str__(self):
        return " * ".join(map(lambda x: ("{}" if isinstance(x, Variable) or isinstance(x, Constance)
                                         else "({})").format(x), self.g))


class Div(Graph):
    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) / self.g2.eval(dic)

    def gradient(self, dic, var):
        b = self.g2.eval(dic)
        return (b * self.g1.gradient(dic, var) - self.g1.eval(dic) * self.g2.gradient(dic,var)) / b**2

    def childs(self):
        return self.g1, self.g2

    def __repr__(self):
        return "Div"

    def __str__(self):
        return "{} / {}".format(brace(self.g1), brace(self.g2))


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

    def childs(self):
        return self.g1, self.g2

    def __repr__(self):
        return "Pow"

    def __str__(self):
        return "{} ^ {}".format(brace(self.g1), brace(self.g2))

