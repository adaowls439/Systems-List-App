import sys
import numpy as np
from scipy.spatial import distance_matrix
import requests
import json

# Dicionário de mapeamento de strings para URLs
url_mapping = {
    'generica': 'http://localhost:3001/api/gene',
    'federal': 'http://localhost:3001/api/fed',
    'imperial': 'http://localhost:3001/api/ipl',
    'revolta civil': 'http://localhost:3001/api/imp',
    'militar': 'http://localhost:3001/api/mil',
    'surto': 'http://localhost:3001/api/pha'
}

hge = sys.argv[1]

# Verificar se a chave está presente no mapeamento
if hge in url_mapping:
    url = url_mapping[hge]  # Atribuir a URL correspondente à chave
else:
    print("HGE não reconhecido")

response = requests.get(url)
data = response.json()

# Definindo a lista de pontos
pontos = []
nomes = []
for item in data:
    ponto = np.array([item['x'], item['y'], item['z']])
    pontos.append(ponto)
    nomes.append(item['name'])

# Criando um grafo vazio
grafo = {}

# Calculando a distância entre todos os pares de pontos
distancias = distance_matrix(pontos, pontos)

# Adicionando arestas entre os pontos que estão próximos o suficiente
for i in range(len(pontos)):
    for j in range(i+1, len(pontos)):
        nome_i = nomes[i]
        nome_j = nomes[j]
        if nome_i not in grafo:
            grafo[nome_i] = {}
        if nome_j not in grafo:
            grafo[nome_j] = {}
        grafo[nome_i][nome_j] = distancias[i][j]
        grafo[nome_j][nome_i] = distancias[i][j]


# Algoritmo Nearest Neighbor para o problema do caixeiro-viajante
print("\n\nAlgoritmo Nearest Neighbor para o problema do caixeiro-viajante\n")


def nearest_neighbor(grafo, inicio):
    visitados = [inicio]  # Armazena a lista de sistemas estelares visitados
    distancias = []  # Armazena a lista de distâncias percorridas
    nao_visitados = list(grafo.keys())
    nao_visitados.remove(inicio)

    # Visita sempre o sistema mais próximo que ainda não foi visitado
    while nao_visitados:
        atual = visitados[-1]
        distancia_minima = float('inf')
        proximo = None
        for vizinho, distancia in grafo[atual].items():
            if vizinho in nao_visitados and distancia < distancia_minima:
                distancia_minima = distancia
                proximo = vizinho
        if proximo:
            visitados.append(proximo)
            nao_visitados.remove(proximo)
            distancias.append(distancia_minima)

    # Retorna a lista de sistemas visitados e a lista de distâncias percorridas
    return visitados, distancias


# Testa diferentes pontos de partida e salva a combinação com a menor distância total
melhor_rota = None
melhor_distancia = float('inf')
for inicio in grafo.keys():
    rota, distancias = nearest_neighbor(grafo, inicio)
    distancia_total = sum(distancias)
    if distancia_total < melhor_distancia:
        melhor_rota = rota
        melhor_distancia = distancia_total

# Imprime a melhor rota e a distância total
print('Melhor rota:')
for i in range(len(melhor_rota)-1):
    distancia_atual = distancias[i]
    sistema_atual = melhor_rota[i]
    sistema_proximo = melhor_rota[i+1]
    print(f"{sistema_atual} -> ({distancia_atual:.2f} Ly) -> {sistema_proximo}")
print(f"Distância total: {melhor_distancia:.2f} Ly")

# Cria um dicionário vazio com as chaves "system" e "ly"
data = {"system": [], "ly": []}

# Percorre a melhor rota encontrada (invertida) e adiciona o nome do sistema à lista "system"
for sistema in reversed(melhor_rota):
    data["system"].append(sistema)

    # Para cada sistema na rota, obtém a distância percorrida até o sistema atual
    if sistema != melhor_rota[-1]:
        distancia = f"{grafo[sistema][melhor_rota[melhor_rota.index(sistema) + 1]]:.2f} Ly"
        data["ly"].append(distancia)
    else:
        data["ly"].append("0 Ly")

# Salva o dicionário como um arquivo JSON
with open("./data/systems.json", "w") as f:
    json.dump(data, f)
