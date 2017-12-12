from graph import *
from Parse import parse

G,_ = parse(input('Expression : '))

print(G)
draw_tree(G)
print("\nGradient!\n")

gra = G.gradient_graph('x')

print(gra)
draw_tree(gra)
