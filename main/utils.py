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