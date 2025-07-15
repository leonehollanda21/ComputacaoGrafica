import math

def criar_matriz_identidade():
    return [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

def criar_matriz_translacao(tx, ty, tz):
    return [
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ]

def multiplicar_matriz_por_vetor(matriz, vetor):
    resultado = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            resultado[i] += matriz[i][j] * vetor[j]
    return resultado

def multiplicar_matrizes(mat_a, mat_b):
    mat_resultado = [[0, 0, 0, 0] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                mat_resultado[i][j] += mat_a[i][k] * mat_b[k][j]
    return mat_resultado

def subtrair_vetores(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]

def produto_vetorial(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

def normalizar_vetor(v):
    magnitude = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if magnitude == 0:
        return [0, 0, 0]
    return [v[0] / magnitude, v[1] / magnitude, v[2] / magnitude]

def escalar_vetor(v, s):
    return [v[0] * s, v[1] * s, v[2] * s]

def adicionar_vetores(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]


def avaliar_bezier_cubica(p0, p1, p2, p3, t):
    um_menos_t = 1 - t
    p_t = adicionar_vetores(
        escalar_vetor(p0, um_menos_t**3),
        adicionar_vetores(
            escalar_vetor(p1, 3 * um_menos_t**2 * t),
            adicionar_vetores(
                escalar_vetor(p2, 3 * um_menos_t * t**2),
                escalar_vetor(p3, t**3)
            )
        )
    )
    return p_t



def criar_matriz_rotacao_y(angulo_rad):

    c = math.cos(angulo_rad)
    s = math.sin(angulo_rad)

    return [
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ]


def produto_escalar(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


def criar_matriz_view(pos_camera, ponto_alvo, vetor_up_mundo):
    z_cam = normalizar_vetor(subtrair_vetores(pos_camera, ponto_alvo))
    x_cam = normalizar_vetor(produto_vetorial(vetor_up_mundo, z_cam))
    y_cam = produto_vetorial(z_cam, x_cam)

    matriz_rotacao_inversa = [
        [x_cam[0], x_cam[1], x_cam[2], 0],
        [y_cam[0], y_cam[1], y_cam[2], 0],
        [z_cam[0], z_cam[1], z_cam[2], 0],
        [0, 0, 0, 1]
    ]

    matriz_translacao_inversa = criar_matriz_translacao(
        -pos_camera[0], -pos_camera[1], -pos_camera[2]
    )

    matriz_view = multiplicar_matrizes(matriz_rotacao_inversa, matriz_translacao_inversa)

    return matriz_view
matriz_rot_90_graus_y = criar_matriz_rotacao_y(math.pi / 2)

