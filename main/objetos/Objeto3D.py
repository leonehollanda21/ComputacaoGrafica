from main.utils import criar_matriz_identidade, multiplicar_matrizes, multiplicar_matriz_por_vetor


class Objeto3D:
    def __init__(self, vertices, faces, cor='blue'):
        self.vertices = [v + [1] for v in vertices]
        self.faces = faces
        self.cor = cor

        self.matriz_transformacao = criar_matriz_identidade()

    def aplicar_transformacao(self, matriz):
        self.matriz_transformacao = multiplicar_matrizes(matriz, self.matriz_transformacao)

    def obter_vertices_transformados(self):
        vertices_transformados = []
        for v in self.vertices:
            v_transformado = multiplicar_matriz_por_vetor(self.matriz_transformacao, v)
            vertices_transformados.append(v_transformado)

        return [v[:3] for v in vertices_transformados]