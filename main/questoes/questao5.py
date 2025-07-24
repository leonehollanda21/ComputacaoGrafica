from PIL import Image
import math

from main.utils import (
    criar_matriz_view,
    criar_matriz_projecao_perspectiva,
    multiplicar_matriz_por_vetor,
    calcular_coordenadas_baricentricas,
    desenhar_linha_simples
)

mapa_de_cores = {
    'cyan': (0, 255, 255), 'magenta': (255, 0, 255), 'orange': (255, 165, 0),
    'black': (0, 0, 0), 'indigo': (75, 0, 130)
}


def questao5(objetos_da_cena, resolucoes):
    pos_camera = [8, 6, 12]
    ponto_alvo = [0, 0, 0]
    vetor_up_mundo = [0, 1, 0]
    matriz_view = criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo)

    fov = 40;
    aspect_ratio = 16 / 9;
    near = 0.1;
    far = 100.0
    matriz_projecao = criar_matriz_projecao_perspectiva(fov, aspect_ratio, near, far)

    todos_os_pontos_2d = []
    vertices_projetados_por_objeto = []
    for obj in objetos_da_cena:
        vertices_mundo = obj.obter_vertices_transformados()
        vertices_projetados = []
        for v_mundo in vertices_mundo:
            v_homogeneo = v_mundo + [1]
            v_camera = multiplicar_matriz_por_vetor(matriz_view, v_homogeneo)
            v_projetado = multiplicar_matriz_por_vetor(matriz_projecao, v_camera)
            vertices_projetados.append(v_projetado)

            w = v_projetado[3]
            if w > near:
                todos_os_pontos_2d.append((v_projetado[0] / w, v_projetado[1] / w))
        vertices_projetados_por_objeto.append(vertices_projetados)

    if not todos_os_pontos_2d:
        print("Nenhum objeto para renderizar.")
        return

    x_coords = [p[0] for p in todos_os_pontos_2d]
    y_coords = [p[1] for p in todos_os_pontos_2d]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    for largura, altura in resolucoes:
        delta_x = max_x - min_x
        delta_y = max_y - min_y
        margem = 0.9
        escala_x = (largura * margem) / delta_x if delta_x != 0 else 1
        escala_y = (altura * margem) / delta_y if delta_y != 0 else 1
        escala = min(escala_x, escala_y)

        tx = (largura - escala * (max_x + min_x)) / 2
        ty = (altura - escala * (max_y + min_y)) / 2

        imagem = Image.new('RGB', (largura, altura), (255, 255, 255))
        pixels = imagem.load()
        z_buffer = [[float('inf')] * altura for _ in range(largura)]

        for i, obj in enumerate(objetos_da_cena):
            if not obj.faces: continue
            for face in obj.faces:
                v_proj = [vertices_projetados_por_objeto[i][idx] for idx in face]
                vertices_pixel = [];
                profundidades = []
                for v in v_proj:
                    w = v[3]
                    if w <= near: vertices_pixel = None; break
                    px = (v[0] / w) * escala + tx
                    py = altura - ((v[1] / w) * escala + ty)
                    vertices_pixel.append((px, py));
                    profundidades.append(v[2] / w)
                if not vertices_pixel: continue

                v0, v1, v2 = vertices_pixel
                min_x_tri = max(0, min(v0[0], v1[0], v2[0]));
                max_x_tri = min(largura - 1, max(v0[0], v1[0], v2[0]))
                min_y_tri = max(0, min(v0[1], v1[1], v2[1]));
                max_y_tri = min(altura - 1, max(v0[1], v1[1], v2[1]))
                for y in range(int(min_y_tri), int(max_y_tri) + 1):
                    for x in range(int(min_x_tri), int(max_x_tri) + 1):
                        pesos = calcular_coordenadas_baricentricas((x, y), v0, v1, v2)
                        if pesos and all(0 <= w <= 1 for w in pesos):
                            profundidade_pixel = pesos[0] * profundidades[0] + pesos[1] * profundidades[1] + pesos[2] * \
                                                 profundidades[2]
                            if profundidade_pixel < z_buffer[x][y]:
                                z_buffer[x][y] = profundidade_pixel
                                pixels[x, y] = mapa_de_cores[obj.cor]

        cor_malha = (0, 0, 0)
        for i, obj in enumerate(objetos_da_cena):
            if obj.faces:
                for face in obj.faces:
                    v_proj = [vertices_projetados_por_objeto[i][idx] for idx in face]
                    vertices_pixel = []
                    for v in v_proj:
                        w = v[3]
                        if w <= near: vertices_pixel = None; break
                        px = (v[0] / w) * escala + tx
                        py = altura - ((v[1] / w) * escala + ty)
                        vertices_pixel.append((px, py))
                    if not vertices_pixel: continue
                    v0, v1, v2 = vertices_pixel
                    desenhar_linha_simples(v0, v1, pixels, cor_malha, largura, altura)
                    desenhar_linha_simples(v1, v2, pixels, cor_malha, largura, altura)
                    desenhar_linha_simples(v2, v0, pixels, cor_malha, largura, altura)

            if hasattr(obj, 'edges') and not obj.faces:
                v_proj_linha = vertices_projetados_por_objeto[i]
                for edge in obj.edges:
                    p_pixel = []
                    for v in [v_proj_linha[edge[0]], v_proj_linha[edge[1]]]:
                        w = v[3]
                        if w > near:
                            px = (v[0] / w) * escala + tx
                            py = altura - ((v[1] / w) * escala + ty)
                            p_pixel.append((px, py))
                        else:
                            p_pixel.append(None)
                    if all(p_pixel):
                        desenhar_linha_simples(p_pixel[0], p_pixel[1], pixels, mapa_de_cores[obj.cor], largura, altura)

        nome_arquivo = f"raster_final_com_malha_{largura}x{altura}.png"
        imagem.save(nome_arquivo)
        print(f"Imagem rasterizada salva como: {nome_arquivo}")