import math

from main.objetos.Objeto3D import Objeto3D
from main.utils import avaliar_bezier_cubica, adicionar_vetores, escalar_vetor, normalizar_vetor, produto_vetorial, \
    subtrair_vetores


class CanoCurvado(Objeto3D):
    def __init__(self, raio, pontos_de_controle, segs_espinha=20, segs_cano=12, cor='purple'):
        vertices = []
        faces = []

        ponto_anterior = None
        vetor_up_global = [0, 1, 0]  # Vetor "para cima" de referência

        for i in range(segs_espinha + 1):
            t = i / segs_espinha

            # 1. Encontrar o ponto e a tangente na curva
            ponto_atual = avaliar_bezier_cubica(pontos_de_controle[0], pontos_de_controle[1], pontos_de_controle[2],
                                                pontos_de_controle[3], t)

            # Aproximar a tangente
            if t < 1.0:
                ponto_seguinte = avaliar_bezier_cubica(pontos_de_controle[0], pontos_de_controle[1],
                                                       pontos_de_controle[2], pontos_de_controle[3], t + 0.001)
                tangente = normalizar_vetor(subtrair_vetores(ponto_seguinte, ponto_atual))
            else:
                tangente = tangente

            if abs(tangente[1]) > 0.99:
                vetor_up_global = [1, 0, 0]

            eixo_x = normalizar_vetor(produto_vetorial(tangente, vetor_up_global))
            eixo_y = normalizar_vetor(produto_vetorial(tangente, eixo_x))

            offset_atual = len(vertices)
            for j in range(segs_cano):
                angulo = 2 * math.pi * j / segs_cano
                v_anel = adicionar_vetores(
                    escalar_vetor(eixo_x, raio * math.cos(angulo)),
                    escalar_vetor(eixo_y, raio * math.sin(angulo))
                )
                vertices.append(adicionar_vetores(ponto_atual, v_anel))

            if i > 0:
                offset_anterior = offset_atual - segs_cano
                for j in range(segs_cano):
                    idx0 = offset_anterior + j
                    idx1 = offset_anterior + ((j + 1) % segs_cano)
                    idx2 = offset_atual + j
                    idx3 = offset_atual + ((j + 1) % segs_cano)
                    faces.append([idx0, idx1, idx2])
                    faces.append([idx1, idx3, idx2])

        super().__init__(vertices, faces, cor=cor)