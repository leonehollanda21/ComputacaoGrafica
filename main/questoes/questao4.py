from matplotlib import pyplot as plt

from main.utils import (
    criar_matriz_view,
    criar_matriz_projecao_perspectiva,
    multiplicar_matriz_por_vetor,
    subtrair_vetores,
    produto_vetorial,
    produto_escalar
)


def questao4(objetos_da_cena):

    pos_camera = [12, 9, 14]
    ponto_alvo = [0, 0, 0]
    vetor_up_mundo = [0, 1, 0]
    matriz_view = criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo)

    fov = 50
    aspect_ratio = 16 / 9
    near = 0.1
    far = 100.0
    matriz_projecao = criar_matriz_projecao_perspectiva(fov, aspect_ratio, near, far)

    fig, ax = plt.subplots(figsize=(12.8, 7.2))

    for obj in objetos_da_cena:
        vertices_mundo = obj.obter_vertices_transformados()

        vertices_2d_finais = []
        for v_mundo in vertices_mundo:
            v_homogeneo = v_mundo + [1]
            v_camera = multiplicar_matriz_por_vetor(matriz_view, v_homogeneo)
            v_projetado = multiplicar_matriz_por_vetor(matriz_projecao, v_camera[:3] + [1])

            w = v_projetado[3]
            if w > near:
                x_2d = v_projetado[0] / w
                y_2d = v_projetado[1] / w
                vertices_2d_finais.append((x_2d, y_2d))
            else:
                vertices_2d_finais.append(None)

        if obj.faces:
            for face in obj.faces:
                p1_idx, p2_idx, p3_idx = face
                p1 = vertices_2d_finais[p1_idx] if p1_idx < len(vertices_2d_finais) else None
                p2 = vertices_2d_finais[p2_idx] if p2_idx < len(vertices_2d_finais) else None
                p3 = vertices_2d_finais[p3_idx] if p3_idx < len(vertices_2d_finais) else None

                if p1 and p2: ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=obj.cor, solid_capstyle='round', lw=1)
                if p2 and p3: ax.plot([p2[0], p3[0]], [p2[1], p3[1]], color=obj.cor, solid_capstyle='round', lw=1)
                if p3 and p1: ax.plot([p3[0], p1[0]], [p3[1], p1[1]], color=obj.cor, solid_capstyle='round', lw=1)

        if hasattr(obj, 'edges') and obj.edges:
            for edge in obj.edges:
                p1, p2 = [vertices_2d_finais[idx] if idx < len(vertices_2d_finais) else None for idx in edge]
                if p1 and p2:
                    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=obj.cor, linewidth=2)

    ax.set_title("Projeção 2D com Malha Completa (Sem Culling - Questão 4)")
    ax.set_xlabel("Eixo X da Tela (Normalizado)")
    ax.set_ylabel("Eixo Y da Tela (Normalizado)")
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    plt.show()