import json

# Abre o arquivo de texto para leitura
with open('listCMDTBOX.txt', 'r') as file:
    # Lê as linhas do arquivo e remove caracteres de nova linha
    lines = [line.strip() for line in file.readlines()]

# Extrai os valores da primeira coluna e salva como uma lista de strings
col1_values = []
for line in lines:
    columns = line.split('\t')
    col1_values.append(columns[0])

# Salva a lista de valores da primeira coluna como um arquivo JSON
with open('./data/systems.json', 'w') as file:
    json.dump(col1_values, file)
