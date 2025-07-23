import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from main.objetos.cano_curvado import CanoCurvado
from main.objetos.cano_reto import CanoReto
from main.objetos.cilindro import Cilindro
from main.objetos.linha_reta import LinhaReta
from main.objetos.paralelepípedo import Paralelepipedo
from main.questoes.questao3 import questao3
from main.questoes.questao4 import questao4
from main.questoes.questao5 import questao5
from main.questoes.questao4_visualizacao import questao4_visualizacao
from main.utils import criar_matriz_translacao, criar_matriz_rotacao_y, criar_matriz_view, multiplicar_matriz_por_vetor

meu_paralelepipedo = Paralelepipedo(base=2, altura=2, comprimento=2, cor='cyan')
meu_cilindro = Cilindro(raio=1, altura=4, cor='magenta')
meu_cano_reto = CanoReto(raio=0.8, comprimento=5, cor='orange')
minha_linha = LinhaReta(tamanho=8, cor='black')
#curva do cano curvado
pontos_bezier = [[0, 0, 0], [0, 4, 0], [4, 4, 0], [4, 0, 0]]
meu_cano_curvado = CanoCurvado(raio=0.5, pontos_de_controle=pontos_bezier, cor='indigo')
# Paralelepípedo vai para o canto X positivo, Y positivo
trans_p = criar_matriz_translacao(5, 5, 0)
meu_paralelepipedo.aplicar_transformacao(trans_p)
# Cilindro vai para o canto X negativo, Y positivo
trans_c = criar_matriz_translacao(-5, 5, 0)
meu_cilindro.aplicar_transformacao(trans_c)
# Cano Reto será rotacionado para ficar deitado e movido para Y negativo
rot_cr = criar_matriz_rotacao_y(math.pi / 2)  # Rotaciona 90 graus
trans_cr = criar_matriz_translacao(0, -6, 0)
meu_cano_reto.aplicar_transformacao(rot_cr)
meu_cano_reto.aplicar_transformacao(trans_cr)
# Linha Reta é movida para a frente no eixo Z
trans_l = criar_matriz_translacao(0, 0, 5)
minha_linha.aplicar_transformacao(trans_l)
# Cano Curvado é movido para baixo, no centro
trans_cc = criar_matriz_translacao(-2, -5, -2)
meu_cano_curvado.aplicar_transformacao(trans_cc)
objetos_da_cena = [
    meu_paralelepipedo,
    meu_cilindro,
    meu_cano_reto,
    minha_linha,
    meu_cano_curvado
]
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
for obj in objetos_da_cena:
    vertices_mundo = obj.obter_vertices_transformados()
    if obj.faces:
        lista_de_poligonos = [[vertices_mundo[i] for i in face] for face in obj.faces]
        mesh = Poly3DCollection(lista_de_poligonos, facecolors=obj.cor, edgecolors='k', alpha=0.9)
        ax.add_collection3d(mesh)
    if hasattr(obj, 'edges') and obj.edges:
        for edge in obj.edges:
            ponto_inicio = vertices_mundo[edge[0]]
            ponto_fim = vertices_mundo[edge[1]]
            ax.plot(
                [ponto_inicio[0], ponto_fim[0]],
                [ponto_inicio[1], ponto_fim[1]],
                [ponto_inicio[2], ponto_fim[2]],
                color=obj.cor, linewidth=4
            )
ax.set_title("Cena 3D com Todos os Sólidos Modelados")
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_zlabel('Eixo Z')
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])

ax.set_aspect('auto')

ax.view_init(elev=25., azim=-50)

plt.show()

questao3(objetos_da_cena)
questao4(objetos_da_cena)
# Mostra a visualização 3D que explica o processo de projeção
print("Executando Questão 4.2: Visualização do Frustum...")
questao4_visualizacao(objetos_da_cena)

resolucoes_desejadas = [(320, 180), (640, 360), (960, 540), (1280, 720)]

questao5(objetos_da_cena, resolucoes_desejadas)