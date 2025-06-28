from main.objetos.Objeto3D import Objeto3D


class LinhaReta(Objeto3D):
    def __init__(self, tamanho=4, cor='black'):
        # Uma linha reta é definida por um ponto inicial e final
        vertices = [
            [0, 0, 0],
            [tamanho, 0, 0]
        ]

        # Não há faces, apenas uma aresta
        faces = []

        super().__init__(vertices, faces, cor=cor)

        # Podemos guardar a aresta para facilitar a plotagem
        self.edges = [[0, 1]]