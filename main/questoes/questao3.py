from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from main.utils import multiplicar_matriz_por_vetor, criar_matriz_view


def questao3(objetos_da_cena):
    # --- Câmera e Alvo ---
    # MODIFICADO: Usando os exatos parâmetros de câmera do seu relatório de referência.
    # Posição da câmera (eye)
    pos_camera = [5, -5, 10]
    # Ponto de interesse (at) para onde a câmera aponta
    ponto_alvo = [5, 5, 0]
    # Vetor "up"
    vetor_up_mundo = [0, 1, 0]

    # b. Compute a base vetorial e crie a Matriz de Visualização.
    # A função criar_matriz_view já implementa a lógica descrita no relatório.
    matriz_view = criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo)

    # --- Renderização ---
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    for obj in objetos_da_cena:
        vertices_mundo = obj.obter_vertices_transformados()

        # Transforma os vértices do mundo para o sistema de coordenadas da câmera.
        vertices_camera = []
        for v_mundo in vertices_mundo:
            v_homogeneo = v_mundo + [1]
            v_transformado = multiplicar_matriz_por_vetor(matriz_view, v_homogeneo)
            vertices_camera.append(v_transformado[:3])

        # A lógica de desenho permanece a mesma
        if obj.faces:
            lista_de_poligonos = [[vertices_camera[i] for i in face] for face in obj.faces]
            mesh = Poly3DCollection(lista_de_poligonos, facecolors=obj.cor, edgecolors='k', alpha=0.9)
            ax.add_collection3d(mesh)

        if hasattr(obj, 'edges') and obj.edges:
            for edge in obj.edges:
                p1 = vertices_camera[edge[0]]
                p2 = vertices_camera[edge[1]]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=obj.cor, linewidth=4)

    # Marcador da origem do mundo (a lógica não muda)
    origem_mundo_homogenea = [0, 0, 0, 1]
    origem_na_visao_camera = multiplicar_matriz_por_vetor(matriz_view, origem_mundo_homogenea)
    ax.scatter(
        origem_na_visao_camera[0], origem_na_visao_camera[1], origem_na_visao_camera[2],
        color='red', s=150, marker='X', label='Origem do Mundo (0,0,0)'
    )

    # --- Configurações do Gráfico ---
    ax.set_title("Cena Transformada para o Sistema de Coordenadas da Câmera")
    ax.set_xlabel('Eixo X da Câmera (xc)')
    ax.set_ylabel('Eixo Y da Câmera (yc)')
    ax.set_zlabel('Eixo Z da Câmera (zc)')

    # MODIFICADO: Ajustando os limites para enquadrar melhor a nova visão.
    limite_visao = 15
    ax.set_xlim([-limite_visao, limite_visao])
    ax.set_ylim([-limite_visao, limite_visao])
    ax.set_zlim([-limite_visao, limite_visao])
    ax.set_aspect('auto')
    ax.legend()

    # MODIFICADO: Alterando o ângulo de visualização do gráfico para uma visão isométrica,
    # como na imagem de referência.
    ax.view_init(elev=30, azim=-60)

    plt.show()