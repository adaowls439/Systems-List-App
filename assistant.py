import subprocess

assistente_processo = None

# Função para chamar o assistente.py se a opção "Escutar" estiver habilitada
def chamar_assistente(config):
    global assistente_processo  # Declarar assistente_processo como global
    print("* chamar_assistente")
    if config.get('checkbox_state', {}).get('option2', False):  # Verifica se a opção 'Escutar' está habilitada
        print("## Iniciando Assistente ##")
        assistente_processo = subprocess.Popen(['python', 'Voz.py'])
    else:
        fechar_assistente()

# Função para fechar o assistente se estiver em execução
def fechar_assistente():
    global assistente_processo  # Declarar assistente_processo como global
    print("* fechar_assistente")
    if assistente_processo and assistente_processo.poll() is None:  # Verifica se o assistente está em execução
        print("## Desligando Assistente ##")
        assistente_processo.terminate()  # Encerra o processo do assistente
