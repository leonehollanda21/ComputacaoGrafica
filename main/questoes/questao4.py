import math
from matplotlib import pyplot as plt

# Importa as funções de utilidades necessárias
from main.utils import (
    criar_matriz_view,
    criar_matriz_projecao_perspectiva,
    multiplicar_matriz_por_vetor
)


def questao4(objetos_da_cena):


    pos_camera = [15, 10, 20]
    ponto_alvo = [0, 0, 0]
    vetor_up_mundo = [0, 1, 0]
    matriz_view = criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo)

    fov = 60
    aspect_ratio = 16 / 9
    near = 0.1
    far = 100.0
    matriz_projecao = criar_matriz_projecao_perspectiva(fov, aspect_ratio, near, far)

    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    for obj in objetos_da_cena:
        # Pega os vértices na posição do mundo
        vertices_mundo = obj.obter_vertices_transformados()

        vertices_2d_finais = []
        # Para cada vértice, aplica a pipeline completa
        for v_mundo in vertices_mundo:
            # Transforma para o espaço da câmera
            v_homogeneo = v_mundo + [1]
            v_camera = multiplicar_matriz_por_vetor(matriz_view, v_homogeneo)

            # Transforma para o espaço de projeção (Clip Space)
            v_projetado = multiplicar_matriz_por_vetor(matriz_projecao, v_camera)

            # Executa a Divisão por Perspectiva para obter as coordenadas 2D finais
            w = v_projetado[3]
            if w > near:  # Só desenha vértices que estão na frente da câmera
                x_2d = v_projetado[0] / w
                y_2d = v_projetado[1] / w
                vertices_2d_finais.append((x_2d, y_2d))
            else:  # Se o vértice estiver atrás da câmera, marca-o como inválido
                vertices_2d_finais.append(None)

        # a. Apresente tais objetos em 2D [cite: 29]
        # Cada sólido tem arestas da mesma cor, mas sólidos diferentes têm cores diferentes [cite: 28]
        if obj.faces:
            for face in obj.faces:
                p1_idx, p2_idx, p3_idx = face
                p1 = vertices_2d_finais[p1_idx]
                p2 = vertices_2d_finais[p2_idx]
                p3 = vertices_2d_finais[p3_idx]

                # Desenha as 3 arestas do triângulo, verificando se os pontos são válidos
                if p1 and p2: ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=obj.cor)
                if p2 and p3: ax.plot([p2[0], p3[0]], [p2[1], p3[1]], color=obj.cor)
                if p3 and p1: ax.plot([p3[0], p1[0]], [p3[1], p1[1]], color=obj.cor)

        if hasattr(obj, 'edges') and obj.edges:
            for edge in obj.edges:
                p1 = vertices_2d_finais[edge[0]]
                p2 = vertices_2d_finais[edge[1]]
                if p1 and p2:  # Apenas desenha se ambos os pontos forem válidos
                    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=obj.cor, linewidth=2)

    # --- Configurações Finais do Plot 2D ---
    ax.set_title("Projeção em Perspectiva 2D da Cena (Questão 4)")
    ax.set_xlabel("Eixo X da Tela (Normalizado)")
    ax.set_ylabel("Eixo Y da Tela (Normalizado)")
    ax.set_aspect('equal', adjustable='box')  # Garante que círculos não pareçam elipses
    ax.grid(True)
    # As coordenadas após a projeção estão normalizadas, geralmente entre -1 e 1.
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    plt.show()