from PIL import Image
import math

from main.utils import (
    criar_matriz_view,
    criar_matriz_projecao_perspectiva,
    multiplicar_matriz_por_vetor,
    calcular_coordenadas_baricentricas,
)

mapa_de_cores = {
    'cyan': (0, 255, 255), 'magenta': (255, 0, 255), 'orange': (255, 165, 0),
    'black': (0, 0, 0), 'indigo': (75, 0, 130)
}


#  Algoritmo de Bresenham
def desenhar_linha_bresenham(p1, p2, pixels, cor, largura, altura):
    x1, y1 = int(p1[0]), int(p1[1])
    x2, y2 = int(p2[0]), int(p2[1])

    dx = abs(x2 - x1)
    sx = 1 if x1 < x2 else -1
    dy = -abs(y2 - y1)
    sy = 1 if y1 < y2 else -1
    err = dx + dy

    while True:
        if 0 <= x1 < largura and 0 <= y1 < altura:
            pixels[x1, y1] = cor
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x1 += sx
        if e2 <= dx:
            err += dx
            y1 += sy


def questao5(objetos_da_cena, resolucoes):
    # Câmera significativamente mais próxima para dar "zoom"
    pos_camera = [20, 19, 24]
    ponto_alvo = [0, 0, 0]
    vetor_up_mundo = [0, 1, 0]
    matriz_view = criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo)

    fov = 40;
    aspect_ratio = 16 / 9;
    near = 0.1;
    far = 100.0
    matriz_projecao = criar_matriz_projecao_perspectiva(fov, aspect_ratio, near, far)

    # Pré-calcula todos os vértices projetados
    vertices_projetados_por_objeto = []
    for obj in objetos_da_cena:
        vertices_mundo = obj.obter_vertices_transformados()
        vertices_projetados = [
            multiplicar_matriz_por_vetor(matriz_projecao, multiplicar_matriz_por_vetor(matriz_view, v_mundo + [1])) for
            v_mundo in vertices_mundo]
        vertices_projetados_por_objeto.append(vertices_projetados)

    for largura, altura in resolucoes:
        imagem = Image.new('RGB', (largura, altura), (255, 255, 255))  # Fundo branco
        pixels = imagem.load()
        z_buffer = [[float('inf')] * altura for _ in range(largura)]

        # --- Preenche os polígonos ---
        for i, obj in enumerate(objetos_da_cena):
            if not obj.faces: continue
            for face in obj.faces:
                v_proj = [vertices_projetados_por_objeto[i][idx] for idx in face]
                vertices_pixel = [];
                profundidades = []
                for v in v_proj:
                    w = v[3]
                    if w <= near: vertices_pixel = None; break
                    px = (v[0] / w + 1) * 0.5 * largura
                    py = (1 - v[1] / w) * 0.5 * altura
                    vertices_pixel.append((px, py));
                    profundidades.append(v[2] / w)
                if not vertices_pixel: continue
                v0, v1, v2 = vertices_pixel
                min_x = max(0, min(v0[0], v1[0], v2[0]));
                max_x = min(largura - 1, max(v0[0], v1[0], v2[0]))
                min_y = max(0, min(v0[1], v1[1], v2[1]));
                max_y = min(altura - 1, max(v0[1], v1[1], v2[1]))
                for y in range(int(min_y), int(max_y) + 1):
                    for x in range(int(min_x), int(max_x) + 1):
                        pesos = calcular_coordenadas_baricentricas((x, y), v0, v1, v2)
                        if pesos and all(0 <= w <= 1 for w in pesos):
                            profundidade_pixel = pesos[0] * profundidades[0] + pesos[1] * profundidades[1] + pesos[2] * \
                                                 profundidades[2]
                            if profundidade_pixel < z_buffer[x][y]:
                                z_buffer[x][y] = profundidade_pixel
                                pixels[x, y] = mapa_de_cores[obj.cor]

        # ---  Desenha a malha (wireframe) por cima ---
        cor_malha = (0, 0, 0)  # Cor preta para as arestas
        for i, obj in enumerate(objetos_da_cena):
            if not obj.faces: continue
            for face in obj.faces:
                # Reutiliza os vértices já calculados
                v_proj = [vertices_projetados_por_objeto[i][idx] for idx in face]
                vertices_pixel = []
                for v in v_proj:
                    w = v[3]
                    if w <= near: vertices_pixel = None; break
                    px = (v[0] / w + 1) * 0.5 * largura
                    py = (1 - v[1] / w) * 0.5 * altura
                    vertices_pixel.append((px, py))
                if not vertices_pixel: continue
                v0, v1, v2 = vertices_pixel
                # Desenha as 3 arestas do triângulo usando Bresenham
                desenhar_linha_bresenham(v0, v1, pixels, cor_malha, largura, altura)
                desenhar_linha_bresenham(v1, v2, pixels, cor_malha, largura, altura)
                desenhar_linha_bresenham(v2, v0, pixels, cor_malha, largura, altura)

        # Salva a imagem final
        nome_arquivo = f"raster_final_com_malha_{largura}x{altura}.png"
        imagem.save(nome_arquivo)
        print(f"Imagem rasterizada salva como: {nome_arquivo}")