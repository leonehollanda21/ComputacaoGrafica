from main.objetos.Objeto3D import Objeto3D


class Paralelepipedo(Objeto3D):
    def __init__(self, base, altura, comprimento, cor='cyan'):
        b, a, c = base, altura, comprimento
        # Vértices:
        vertices = [
            [0, 0, 0], [b, 0, 0], [b, a, 0], [0, a, 0],
            [0, 0, c], [b, 0, c], [b, a, c], [0, a, c]
        ]

        faces = [
            # Face Frontal (virada para -Z)
            [0, 2, 1], [0, 3, 2],

            # Face Traseira (virada para +Z)
            [4, 5, 6], [4, 6, 7],

            # Face Esquerda (virada para -X)
            [4, 3, 0], [4, 7, 3],

            # Face Direita (virada para +X)
            [1, 2, 6], [1, 6, 5],

            # Face Inferior (virada para -Y)
            [0, 5, 1], [0, 4, 5],

            # Face Superior (virada para +Y)
            [3, 6, 2], [3, 7, 6]
        ]

        super().__init__(vertices, faces, cor=cor)