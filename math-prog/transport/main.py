from data import a, d, C
from model import TransportModel


if __name__ == '__main__':
    tm = TransportModel(a, d, C)
    tm.solve()
    tm.print_result()
