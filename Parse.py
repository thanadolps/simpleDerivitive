from graph import *
import re
from re import sub

# TODO [main] : Variable linking


def check_matching(express : str):

    depth = 0
    for i,j in enumerate(express):
        if j == '(':
            depth += 1
        elif j == ')':
            depth -= 1

        if depth == 0 and i < len(express) - 1:
            return False

    return depth == 0


def find_in_layer(express : str, chars : str,  relative_layer = 0, start = 0):

    depth = 0
    for i, j in enumerate(express):

        if i < start:
            continue

        if j == '(':
            depth += 1
        elif j == ')':
            depth -= 1
        elif j in chars and depth == relative_layer:
            return i
    return -1



def braclet_parse(express : str):
    pass


def pre_parse(express: str):

    # whitespace remove
    express = express.replace(" ","")

    # near-braclet multiplication
    express = express.replace(")(",")*(")

    # coefficient system
    def add_start(m):
        return m.group(1) + "*" + m.group(2)

    express = sub(r"(\d)([a-zA-z])", add_start, express)

    return express


def parse(express : str):

    pre = pre_parse(express)
    return __parse(pre[::-1])


def __parse(express : str):

    if express.isdecimal():
        return float(express[::-1])

    if express.isalpha():
        return reduce(lambda x,y : x * y, (Variable(i) for i in express))

    if express.startswith(')') and check_matching(express):
        return __parse(express[1:-1])

    layer = 0

    for i,j in enumerate(express):

        if j == '(':
            layer += 1
        elif j == ')':
            layer -= 1

        if layer == 0:
            if find_in_layer(express, '+') == -1 and find_in_layer(express, '-') == -1:
                if j == '*':
                    return Mul(__parse(express[i+1:]), __parse(express[:i]))
            else:
                if j == '+':
                    return Add(__parse(express[i+1:]), __parse(express[:i]))
                elif j == '-':
                    return Sub(__parse(express[i+1:]), __parse(express[:i]))
