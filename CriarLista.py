import json

# Abre o arquivo de texto para leitura
with open('listCMDTBOX.txt', 'r') as file:
    # Lê as linhas do arquivo e remove caracteres de nova linha
    lines = [line.strip() for line in file.readlines()]

# Extrai os valores da primeira coluna e salva como uma lista de strings
system = []
ly =[]
for line in lines:
    columns = line.split('\t')
    system.append(columns[0])
    ly.append(columns[3])

# Cria um dicionário com as duas listas
data = {"system": system, "ly": ly}

# Salva o dicionário em um arquivo JSON
with open('./data/systems.json', 'w') as file:
    json.dump(data, file)
