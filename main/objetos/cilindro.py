import math

from main.objetos.Objeto3D import Objeto3D


class Cilindro(Objeto3D):
    def __init__(self, raio, altura, segmentos=20, cor='green'):
        vertices = []
        faces = []

        # vertices das bases usando
        for i in range(segmentos):
            angulo = 2 * math.pi * i / segmentos
            x, y = raio * math.cos(angulo), raio * math.sin(angulo)
            vertices.append([x, y, 0])
            vertices.append([x, y, altura])

        vertices.append([0, 0, 0])  # Centro da base
        vertices.append([0, 0, altura])  # Centro do topo

        # gerar faces permanece a mesma
        centro_base_idx = len(vertices) - 2
        centro_topo_idx = len(vertices) - 1

        for i in range(segmentos):
            idx_base_atual = i * 2
            idx_topo_atual = i * 2 + 1
            idx_base_prox = ((i + 1) % segmentos) * 2
            idx_topo_prox = ((i + 1) % segmentos) * 2 + 1

            faces.append([idx_base_atual, idx_base_prox, idx_topo_atual])
            faces.append([idx_base_prox, idx_topo_prox, idx_topo_atual])
            faces.append([idx_base_atual, centro_base_idx, idx_base_prox])
            faces.append([idx_topo_atual, idx_topo_prox, centro_topo_idx])

        super().__init__(vertices, faces, cor=cor)