from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from main.objetos.cilindro import Cilindro
from main.objetos.paralelepípedo import Paralelepipedo
from main.utils import criar_matriz_translacao

meu_paralelepipedo = Paralelepipedo(base=2, altura=3, comprimento=4, cor='cyan')
meu_cilindro = Cilindro(raio=1, altura=5, cor='magenta')

# 2. Aplicar transformações
# Usamos nossa função que retorna listas de listas
matriz_translacao_p = criar_matriz_translacao(5, 0, 0)
meu_paralelepipedo.aplicar_transformacao(matriz_translacao_p)

matriz_translacao_c = criar_matriz_translacao(-5, 0, 0)
meu_cilindro.aplicar_transformacao(matriz_translacao_c)

# 3. Criar a lista de objetos da cena
objetos_da_cena = [meu_paralelepipedo, meu_cilindro]

# 4. Loop de Renderização
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for obj in objetos_da_cena:
    vertices_mundo = obj.obter_vertices_transformados()

    # Matplotlib funciona melhor com numpy, mas frequentemente converte
    # listas automaticamente. Para garantir, podemos fazer a conversão aqui.
    # Ou, podemos extrair as faces diretamente.
    lista_de_poligonos = []
    for face in obj.faces:
        poligono = [vertices_mundo[i] for i in face]
        lista_de_poligonos.append(poligono)

    mesh = Poly3DCollection(lista_de_poligonos, facecolors=obj.cor, edgecolors='k', alpha=0.8)
    ax.add_collection3d(mesh)

# Configurações do plot
ax.set_xlabel('X');
ax.set_ylabel('Y');
ax.set_zlabel('Z')
ax.set_xlim([-10, 10]);
ax.set_ylim([-10, 10]);
ax.set_zlim([-10, 10])
ax.view_init(elev=20., azim=-35)
plt.show()