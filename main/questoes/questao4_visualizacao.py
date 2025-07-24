import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from main.utils import (
    criar_matriz_view,
    criar_matriz_projecao_perspectiva,
    multiplicar_matriz_por_vetor
)


def questao4_visualizacao(objetos_da_cena):

    pos_camera = [12, 9, 14]
    ponto_alvo = [0, 0, 0]
    vetor_up_mundo = [0, 1, 0]
    fov = 50;
    aspect_ratio = 16 / 9;
    near = 1.0;
    far = 20.0

    matriz_view = criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo)
    matriz_projecao = criar_matriz_projecao_perspectiva(fov, aspect_ratio, near, far)

    vertices_camera_3d_por_obj = []
    vertices_2d_finais_por_obj = []
    for obj in objetos_da_cena:
        vertices_mundo = obj.obter_vertices_transformados()
        v_cam_3d_obj = []
        v_2d_final_obj = []
        for v_mundo in vertices_mundo:
            v_homogeneo = v_mundo + [1]
            v_camera = multiplicar_matriz_por_vetor(matriz_view, v_homogeneo)
            v_cam_3d_obj.append(v_camera[:3])

            v_projetado = multiplicar_matriz_por_vetor(matriz_projecao, v_camera)
            w = v_projetado[3]
            if w > near:
                v_2d_final_obj.append((v_projetado[0] / w, v_projetado[1] / w))
            else:
                v_2d_final_obj.append(None)
        vertices_camera_3d_por_obj.append(v_cam_3d_obj)
        vertices_2d_finais_por_obj.append(v_2d_final_obj)

    fig = plt.figure(figsize=(18, 9))
    fig.suptitle("Questão 4: Processo de Projeção e Resultado Final", fontsize=16)

    ax_3d = fig.add_subplot(1, 2, 1, projection='3d')
    ax_3d.set_title("Visualização do Processo (Espaço da Câmera)")

    ax_2d = fig.add_subplot(1, 2, 2)
    ax_2d.set_title("Resultado da Projeção (Plano 2D)")

    for i, obj in enumerate(objetos_da_cena):
        vertices_camera = vertices_camera_3d_por_obj[i]
        if obj.faces:
            mesh = Poly3DCollection([[vertices_camera[idx] for idx in face] for face in obj.faces],
                                    facecolors=obj.cor, edgecolors='k', alpha=0.5)
            ax_3d.add_collection3d(mesh)
        if hasattr(obj, 'edges') and obj.edges:
            for edge in obj.edges:
                p1, p2 = [vertices_camera[idx] for idx in edge]
                ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=obj.cor, linewidth=3)

    altura_far = 2 * far * math.tan(math.radians(fov / 2));
    largura_far = altura_far * aspect_ratio
    fc = [0, 0, -far];
    fbl = [fc[0] - largura_far / 2, fc[1] - altura_far / 2, fc[2]];
    fbr = [fc[0] + largura_far / 2, fc[1] - altura_far / 2, fc[2]]
    ftl = [fc[0] - largura_far / 2, fc[1] + altura_far / 2, fc[2]];
    ftr = [fc[0] + largura_far / 2, fc[1] + altura_far / 2, fc[2]]
    cam_pos = [0, 0, 0]
    ax_3d.plot([cam_pos[0], fbl[0]], [cam_pos[1], fbl[1]], [cam_pos[2], fbl[2]], color='red', lw=1);
    ax_3d.plot([cam_pos[0], fbr[0]], [cam_pos[1], fbr[1]], [cam_pos[2], fbr[2]], color='red', lw=1)
    ax_3d.plot([cam_pos[0], ftl[0]], [cam_pos[1], ftl[1]], [cam_pos[2], ftl[2]], color='red', lw=1);
    ax_3d.plot([cam_pos[0], ftr[0]], [cam_pos[1], ftr[1]], [cam_pos[2], ftr[2]], color='red', lw=1)
    ax_3d.plot([fbl[0], fbr[0]], [fbl[1], fbr[1]], [fbl[2], fbr[2]], color='red', lw=1);
    ax_3d.plot([fbr[0], ftr[0]], [fbr[1], ftr[1]], [fbr[2], ftr[2]], color='red', lw=1)
    ax_3d.plot([ftr[0], ftl[0]], [ftr[1], ftl[1]], [ftr[2], ftl[2]], color='red', lw=1);
    ax_3d.plot([ftl[0], fbl[0]], [ftl[1], fbl[1]], [ftl[2], fbl[2]], color='red', lw=1)

    origem_na_visao_camera = multiplicar_matriz_por_vetor(matriz_view, [0, 0, 0, 1])
    ax_3d.scatter(origem_na_visao_camera[0], origem_na_visao_camera[1], origem_na_visao_camera[2], color='yellow',
                  s=100, ec='black', label='Origem do Mundo')
    ax_3d.scatter(0, 0, 0, color='red', s=100, ec='black', label='Câmera (Olho)')
    ax_3d.set_xlabel('Xc');
    ax_3d.set_ylabel('Yc');
    ax_3d.set_zlabel('Zc');
    ax_3d.legend()
    ax_3d.view_init(elev=25, azim=-80)

    for i, obj in enumerate(objetos_da_cena):
        vertices_2d_finais = vertices_2d_finais_por_obj[i]
        if obj.faces:
            for face in obj.faces:
                p1, p2, p3 = [vertices_2d_finais[idx] for idx in face]
                if p1 and p2: ax_2d.plot([p1[0], p2[0]], [p1[1], p2[1]], color=obj.cor, lw=1)
                if p2 and p3: ax_2d.plot([p2[0], p3[0]], [p2[1], p3[1]], color=obj.cor, lw=1)
                if p3 and p1: ax_2d.plot([p3[0], p1[0]], [p3[1], p1[1]], color=obj.cor, lw=1)
        if hasattr(obj, 'edges') and obj.edges:
            for edge in obj.edges:
                p1, p2 = [vertices_2d_finais[idx] for idx in edge]
                if p1 and p2: ax_2d.plot([p1[0], p2[0]], [p1[1], p2[1]], color=obj.cor, linewidth=2)

    ax_2d.set_xlabel("Eixo X Normalizado");
    ax_2d.set_ylabel("Eixo Y Normalizado")
    ax_2d.set_aspect('equal', 'box');
    ax_2d.grid(True)
    ax_2d.set_xlim(-1.2, 1.2);
    ax_2d.set_ylim(-1.2, 1.2)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

