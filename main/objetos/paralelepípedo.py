from main.objetos.Objeto3D import Objeto3D


class Paralelepipedo(Objeto3D):
    def __init__(self, base, altura, comprimento, cor='red'):
        vertices = [
            [0, 0, 0],
            [base, 0, 0],
            [base, altura, 0],
            [0, altura, 0],
            [0, 0, comprimento],
            [base, 0, comprimento],
            [base, altura, comprimento],
            [0, altura, comprimento]
        ]
        faces = [
            [0, 1, 2], [0, 2, 3],
            [1, 5, 6], [1, 6, 2],
            [5, 4, 7], [5, 7, 6],
            [4, 0, 3], [4, 3, 7],
            [3, 2, 6], [3, 6, 7],
            [4, 5, 1], [4, 1, 0]
        ]
        super().__init__(vertices, faces, cor=cor)