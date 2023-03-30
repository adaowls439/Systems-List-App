with open('listEDDB.txt', 'r') as file:
    # Lê as linhas do arquivo e remove caracteres de nova linha
    lines = [line.strip() for line in file.readlines()]

# Extrai os nomes dos sistemas (primeira coluna) e salva em uma lista
system_names = []
for line in lines:
    columns = line.split('\t')
    system_name = columns[0]
    system_names.append(system_name)

# Grava a lista de nomes de sistemas em um arquivo de texto
with open('listEDDB.txt', 'w') as file:
    for name in system_names:
        file.write(name + '\n')
