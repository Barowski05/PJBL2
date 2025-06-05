# -- coding: latin-1 --
import sys
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra(ini, fin, grafo):  # Grafo como Lista de Adjacência (LA).
    if ini == fin:
        return [ini], 0

    n = len(grafo)
    distancia = [float('inf')] * n
    resolvido = [False] * n
    anterior = [-1] * n

    distancia[ini] = 0
    resolvido[ini] = True

    while not resolvido[fin]:
        menor_distancia = float('inf')
        proximo = -1

        for i in range(n):
            if resolvido[i]:
                for (vizinho, peso) in grafo[i]:
                    if not resolvido[vizinho]:
                        nova_dist = distancia[i] + peso
                        if nova_dist < distancia[vizinho]:
                            distancia[vizinho] = nova_dist
                            anterior[vizinho] = i
                        if distancia[vizinho] < menor_distancia:
                            menor_distancia = distancia[vizinho]
                            proximo = vizinho

        if proximo == -1:
            return None, float('inf')  # Caminho inexistente

        resolvido[proximo] = True

    # Reconstrução do caminho
    caminho = []
    atual = fin
    while atual != ini:
        caminho.insert(0, atual)
        atual = anterior[atual]
        if atual == -1:
            return None, float('inf')  # Caminho quebrado
    caminho.insert(0, ini)

    return caminho, distancia[fin]

def plot_grafos(grafo, caminho, ini, fin, desig, Comp):
    G = nx.Graph()
    G_result = nx.Graph()

    for i in range(len(grafo)):
        for vizinho, peso in grafo[i]:
            G.add_edge(i, vizinho, weight=peso)
            G_result.add_edge(i, vizinho, weight=peso)

    pos = nx.spring_layout(G, seed=24)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    nx.draw(G, pos, with_labels=True, labels={i: desig[i] for i in range(len(desig))},
            node_color='lightgray', node_size=500, font_size=10, font_color='black',
            edge_color='black', linewidths=1, edgecolors='black')
    nx.draw_networkx_nodes(G, pos, nodelist=[ini], node_color='lightgreen', edgecolors='black', linewidths=0)
    nx.draw_networkx_nodes(G, pos, nodelist=[fin], node_color='lightsalmon', edgecolors='black', linewidths=0)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)},
                                 font_color='black', rotate=False)
    plt.title("Grafo Original")

    plt.subplot(1, 2, 2)
    edge_colors = ['lightgray' if not (u in caminho and v in caminho and abs(caminho.index(u) - caminho.index(v)) == 1) else 'black' for u, v in G_result.edges()]
    nx.draw(G_result, pos, with_labels=True, labels={i: desig[i] for i in range(len(desig))},
            node_color='lightgray', node_size=500, font_size=10, font_color='black',
            edge_color=edge_colors, linewidths=1, edgecolors='black')
    nx.draw_networkx_nodes(G_result, pos, nodelist=[ini], node_color='lightgreen', edgecolors='black', linewidths=0)
    nx.draw_networkx_nodes(G_result, pos, nodelist=[fin], node_color='lightsalmon', edgecolors='black', linewidths=0)

    edge_labels_result = {(u, v): d['weight'] for u, v, d in G_result.edges(data=True)}
    for (u, v) in edge_labels_result:
        color = 'black' if (u in caminho and v in caminho and abs(caminho.index(u) - caminho.index(v)) == 1) else 'lightgray'
        nx.draw_networkx_edge_labels(G_result, pos, edge_labels={(u, v): edge_labels_result[(u, v)]},
                                     font_color=color, rotate=False)

    plt.title("Grafo com Caminho Minimo")
    plt.text(0.5, -0.1, f"Comprimento caminho: {Comp}", fontsize=10, ha='center', transform=plt.gca().transAxes)
    plt.show()

# Função principal
cidades = ['Aurora', 'Bonito', 'Carmo', 'Douras', 'Estela', 'Felice', 'Gema', 'Herval', 'Ipiau', 'Jaburu', 'Lindoa', 'Mundau']

LA = [
    [(1, 15), (2, 30), (4, 20)],         # Aurora 0
    [(0, 15), (3, 25), (4, 27),(5, 22)],  # Bonito 1
    [(0, 30), (6, 19), (5, 33)],         # Carmo 2
    [(1, 25), (7, 21), (6, 37)],         # Douras 3
    [(2, 37), (0, 20), (8, 18), (7, 35)], # Estela 4
    [(2, 33), (8, 38), (9, 28),(1, 22)],   # Felice 5
    [(2, 19), (3, 37), (9, 40), (10, 24)],# Gema 6
    [(3, 21), (9, 33), (4, 35), (11, 30),(10, 45)] , # Herval 7
    [(5, 38), (4, 18), (11, 50), (10, 32)],         # Ipiaú 8
    [(5, 28), (7, 33), (6, 40),(11,55)],         # Jaburu 9
    [(6, 24), (7, 45),(8,32)],                  # Lindóa 10
    [(7, 30), (8, 50),(10,55)]                   # Mundaú 11
]

orig = 0  # Bonito
destf = 1 # Herval

print("\nVertice inicial.: " + cidades[orig])
print("Vertice final...: " + cidades[destf])

caminho, Comp = dijkstra(orig, destf, LA)
print("Menor caminho de %s ateh %s: %-13s\nValor: %3d" %
      (cidades[orig], cidades[destf], " > ".join(cidades[v] for v in caminho), Comp))
CompTot = Comp

print("\n--------------------------")
print(" Outros destinos")
print("--------------------------")
print("Dest.   Caminho    Custo")
print("--------------------------")

for dest in range(len(LA)):
    if orig != dest and dest != destf:
        Path, Comp = dijkstra(orig, dest, LA)
        print(" " + cidades[dest], end="     ")
        print("%-13s %3d" % (" > ".join(cidades[v] for v in Path), Comp))

plot_grafos(LA, caminho, orig, destf, cidades, CompTot)
