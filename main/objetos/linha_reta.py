from main.objetos.Objeto3D import Objeto3D


class LinhaReta(Objeto3D):
    def __init__(self, tamanho=4, cor='black'):
        vertices = [
            [0, 0, 0],
            [tamanho, 0, 0]
        ]

        faces = []

        super().__init__(vertices, faces, cor=cor)

        self.edges = [[0, 1]]