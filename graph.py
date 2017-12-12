from abc import ABCMeta, abstractmethod
from typing import Union, List
from math import log
from functools import reduce

# TODO [later][Hard] : Optimize Graph Calculation - mainly duplication reusing
# TODO [later] : Optimize Graph Calculation - coefficient combining
# TODO [main] : auto derivative graph -> construct new derivative graph using current graph
# TODO : Add More Function
# TODO : Better output formatting
# TODO : Value State Protocol [zero, one]

Number = Union[int, float]


def isNumber(x):
    return isinstance(x, (float,int))

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

    @abstractmethod
    def gradient_graph(self, var):
        """

        :rtype: Graph
        """
        raise NotImplementedError('users must define gradient_graph to use this base class')

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

    if not isinstance(graph, (int,float)) and graph.childs() is not None:
        for g in graph.childs():
            draw_tree(g, layer + 1)
    elif isinstance(graph, (int,float)):
        print("IF Warning")


GraphInput = Union[Number, Graph]


class Variable(Graph):

    def __init__(self, name='[default_var_name]'):
        self.name = name

    def eval(self, dic):

        x = dic.get(self)

        if x is None:

            x = dic.get(self.name)

            if x is None:
                raise ValueError("input dictionary doesn't contain value for {} {}".format(self.name, x))

        return x

    def gradient(self, dic, var):

        # x' = 1, k' = 0
        if self == var or self.name == var:
            return 1
        else:
            return 0

    def gradient_graph(self, var):

        if self == var or self.name == var:
            return Constance(1)
        else:
            return DerivitiveVariable(self, var)

    def childs(self):
        return None

    def __repr__(self):
        return "Variable {}".format(self.name)

    def __str__(self):
        return str(self.name)


class DerivitiveVariable(Graph):

    def __init__(self, variable, respect : Union[str, Variable]='x'):
        self.var = variable
        self.respect = respect

    def eval(self, dic):

        return self.var.gradient(dic, self.respect)

    def gradient(self, dic, var):

        return self.var.gradient(dic, var)

    def gradient_graph(self, var):

        return DerivitiveVariable(self, var)

    def childs(self):
        return self.var,

    def __repr__(self):
        return "Deri"

    def __str__(self):
        return str(self.var) + "'"



class Constance(Graph):

    def __init__(self, x: Number):
        self.x = x

    def eval(self, dic):
        return self.x

    def gradient(self, dic, var):
        # k' = 0
        return 0

    def gradient_graph(self, var) -> Graph:
        return Constance(0)

    def childs(self):
        return None

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)

    def __eq__(self, other):
        if isinstance(other, Constance):
            return self.x == other.x
        elif isinstance(other, (int,float)):
            return self.x == other
        else:
            return False

    def __float__(self):
        return self.x

zero = Constance(0)
one = Constance(1)


def brace(x):
    if isinstance(x, Variable) or isinstance(x, Constance) or isinstance(x, DerivitiveVariable):
        return "{}".format(x)
    elif not None:
        return "({})".format(x)
    else :
        return ''


class Add(Graph):

    def __init__(self, *args):
        self.g = []
        self.const : int = 0

        for i in args:
            if not bool(i): # Denying
                continue
            elif isinstance(i, Constance): # Constance
                self.const += i.x
            elif isinstance(i, Add): # Add
                self.g += i.g
                self.const += i.const
            elif isinstance(i, (int, float)): # Number
                self.const += i
            else: # Other
                self.g.append(self.constancy(i))

    def eval(self, dic) -> Number:
        return self.const + sum(map(lambda x: x.eval(dic), self.g))

    def gradient(self, dic, var):
        return sum(map(lambda x: x.gradient(dic, var), self.g))

    def gradient_graph(self, var):
        return Add(*map(lambda x : x.gradient_graph(var), self.g))

    def childs(self):
        return self.g + [self.const]

    def __repr__(self):
        return "Add"

    def __str__(self):
        return (f"{self.const}{' + ' if self.g else ''}" if self.const else '') + \
               " + ".join(map(lambda x : str(x), self.g))


class Sub(Graph):

    def __init__(self, g1: GraphInput, g2: GraphInput):

        if isinstance(g1, (Constance,int,float)) and isinstance(g2, (Constance,int,float)):
            self.g1 = self.constancy(self.constancy(g1).x - self.constancy(g2).x)
            self.g2 = zero
        else:
            self.g1: Graph = self.constancy(g1)
            self.g2: Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) - self.g2.eval(dic)

    def gradient(self, x : Number, var):
        return self.g1.gradient(x, var) - self.g2.gradient(x, var)

    def gradient_graph(self, var):
        return Sub(self.g1.gradient_graph(var), self.g2.gradient_graph(var))

    def childs(self):
        return self.g1, self.g2

    def __repr__(self):
        return "Sub"

    def __str__(self):
        return "{} {}".format('' if isinstance(self.g1, Constance) and self.g1.x == 0 else self.g1,
                              '' if isinstance(self.g2, (Constance)) and self.g2.x == 0 else "- " + brace(self.g2))


class Mul(Graph):
    def __init__(self, g1: Graph, *args):
        self.g : List[Graph] = []
        self.const = 1

        self.add(g1)
        for i in args:
            self.add(i)

    def add(self, i):

        if self.const == 0: # Zero = nothing
            return

        if not bool(i): # Denying
            return
        elif isinstance(i, Constance): # Constance
            self.const *= i.x
        elif isinstance(i, Mul): # Mul
            self.g += i.g
            self.const *= i.const
        elif isinstance(i, (int, float)): # Number
            self.const *= i
        else: # Other
            self.g.append(self.constancy(i))

    def eval(self, dic) -> Number:
        return reduce(lambda x, y : x * y, map(lambda x : x.eval(dic), self.g))

    def gradient(self, dic, var):

        all_mult = self.eval(dic)  # = fgh

        # fgh      fgh      fgh
        # --- f' + --- g' + --- h'
        #  f        g        h
        return sum(map(lambda x : x.gradient(dic, var) * all_mult / x.eval(dic), self.g))

    def gradient_graph(self, var):

        sum = Add()

        for i in self.g:
            sum += Mul(*(j if j != i else i.gradient_graph(var) for j in self.g))

        return sum

    def childs(self):
        return self.g + [self.const]

    def __repr__(self):
        return "Mul"

    def __str__(self):
        return (f"{self.const} * " if self.const != 1 else '') + " * ".join(map(brace, self.g)) if self.const else '0'

    def __bool__(self):
        return bool(self.g)


class Div(Graph):
    def __init__(self, g1: GraphInput, g2: GraphInput):
        self.g1 : Graph = self.constancy(g1)
        self.g2 : Graph = self.constancy(g2)

    def eval(self, dic) -> Number:
        return self.g1.eval(dic) / self.g2.eval(dic)

    def gradient(self, dic, var):
        b = self.g2.eval(dic)
        return (b * self.g1.gradient(dic, var) - self.g1.eval(dic) * self.g2.gradient(dic,var)) / b**2

    def gradient_graph(self, var):
        return (self.g2 * self.g1.gradient_graph(var) - self.g1 * self.g2.gradient_graph(var)) / Pow(self.g2, 2)

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

    def gradient_graph(self, var):
        # TODO
        f = self.g1
        fd = self.g1.gradient_graph(var)
        g = self.g2
        return Pow(f, g-one) * g * fd

    def childs(self):
        return self.g1, self.g2

    def __repr__(self):
        return "Pow"

    def __str__(self):
        return "{} ^ {}".format(brace(self.g1), '' if isinstance(self.g2, (int,float,Constance))
                                                                  and self.g2 == 1 else brace(self.g2))

