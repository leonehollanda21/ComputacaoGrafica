import math

from main.objetos.Objeto3D import Objeto3D


class CanoReto(Objeto3D):
    def __init__(self, raio, comprimento, segmentos=20, cor='yellow'):
        vertices = []
        faces = []

        # Gerar os anéis de vértices nas duas extremidades
        for i in range(segmentos):
            angulo = 2 * math.pi * i / segmentos
            x = raio * math.cos(angulo)
            y = raio * math.sin(angulo)
            vertices.append([x, y, 0])
            vertices.append([x, y, comprimento])

        # Gerar as faces laterais (a superfície do cano)
        for i in range(segmentos):
            idx_base_atual = i * 2
            idx_topo_atual = i * 2 + 1
            # O operador '%' garante que o último segmento se conecte ao primeiro
            idx_base_prox = ((i + 1) % segmentos) * 2
            idx_topo_prox = ((i + 1) % segmentos) * 2 + 1

            # Criar a face retangular lateral com dois triângulos
            faces.append([idx_base_atual, idx_base_prox, idx_topo_atual])
            faces.append([idx_base_prox, idx_topo_prox, idx_topo_atual])

        super().__init__(vertices, faces, cor=cor)