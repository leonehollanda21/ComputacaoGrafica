from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from main.utils import multiplicar_matriz_por_vetor, criar_matriz_view


def questao3(objetos_da_cena):
    # a. Escolha um ponto como origem para o sistema de coordenadas da câmera.
    pos_camera = [15, 10, 20]
    ponto_alvo = [0, 0, 0]
    vetor_up_mundo = [0, 1, 0]
    # b. Compute a base vetorial e crie a Matriz de Visualização.
    matriz_view = criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo)


    #Requisito 3c)
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    for obj in objetos_da_cena:
        #  Pega os vértices do objeto já na sua posição no mundo.
        vertices_mundo = obj.obter_vertices_transformados()

        #  b. Transforma os vértices do mundo para o sistema de coordenadas da câmera.
        vertices_camera = []
        for v_mundo in vertices_mundo:
            v_homogeneo = v_mundo + [1] # Adiciona w=1 para multiplicação da matriz 4x4
            v_transformado = multiplicar_matriz_por_vetor(matriz_view, v_homogeneo)
            vertices_camera.append(v_transformado[:3]) # Guarda apenas as coordenadas XYZ

        if obj.faces:
            lista_de_poligonos = [[vertices_camera[i] for i in face] for face in obj.faces]
            mesh = Poly3DCollection(lista_de_poligonos, facecolors=obj.cor, edgecolors='k', alpha=0.9)
            ax.add_collection3d(mesh)

        if hasattr(obj, 'edges') and obj.edges:
            for edge in obj.edges:
                p1 = vertices_camera[edge[0]]
                p2 = vertices_camera[edge[1]]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=obj.cor, linewidth=4)

    origem_mundo_homogenea = [0, 0, 0, 1]
    origem_na_visao_camera = multiplicar_matriz_por_vetor(matriz_view, origem_mundo_homogenea)
    ax.scatter(
        origem_na_visao_camera[0], origem_na_visao_camera[1], origem_na_visao_camera[2],
        color='red', s=150, marker='X', label='Origem do Mundo (0,0,0)'
    )

    ax.set_title("Cena Vista pelo Sistema de Coordenadas da Câmera")
    ax.set_xlabel('Eixo X da Câmera')
    ax.set_ylabel('Eixo Y da Câmera')
    ax.set_zlabel('Eixo Z da Câmera')

    limite_visao = 20
    ax.set_xlim([-limite_visao, limite_visao])
    ax.set_ylim([-limite_visao, limite_visao])
    ax.set_zlim([-limite_visao, limite_visao])
    ax.set_aspect('auto')
    ax.legend()

    ax.view_init(elev=0, azim=-90)

    plt.show()
