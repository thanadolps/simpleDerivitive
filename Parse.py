# TODO Parse.py
# Convert String Expression Into Graph
# Mainly Unpacking

from graph import *


def matching(express : str):
    depth = 0
    for i,j in enumerate(express):
        if j == '(':
            depth += 1
        elif j == ')':
            depth -= 1
            if depth == 0:
                return i

    raise ValueError("braclet error : {}".format(express))


def braclet_parse(express : str):
    pass


def parse(express : str):

    # preformat
    express.replace(" ","")

    return __parse(express)


def __parse(express : str):

    if express.isdecimal():
        return float(express)

    for i,j in enumerate(express):

        if j == '+':
            return Add(__parse(express[:i]), __parse(express[i+1:]))
        elif j == '-':
            return Sub(__parse(express[:i]), __parse(express[i+1:]))