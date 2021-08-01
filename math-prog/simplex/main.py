import numpy as np

from simplex_a import SimplexA
from simplex_ad import SimplexAD
from simplex_2phase import Simplex2P
from instances import instances


if __name__ == '__main__':
    ins = instances[0]  # Normal
    SimplexA(ins['c'], ins['A'], ins['b'], ins['v0']).solve()
    ins = instances[5]  # Degenerate
    SimplexAD(ins['c'], ins['A'], ins['b'], ins['v0']).solve()
    ins = instances[6]  # Degenerate
    #Simplex2P(ins['c'], ins['A'], ins['b']).solve()

