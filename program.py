from datastructures.avltree import AVLTree
from tests.car import Car, Color, Make, Model

def main():
    # print('Hello world!')

    # car = Car(vin='123456789', color=Color.RED, make=Make.TOYOTA, model=Model.COROLLA)
    # print(car)
    
    tree = AVLTree[int, int]([(1,1)])

if __name__ == '__main__':
    main()
