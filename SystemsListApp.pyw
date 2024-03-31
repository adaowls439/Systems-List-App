import PySimpleGUI as sg
import json
import time
import threading
import os
import subprocess
from interface import create_settings_window, create_main_window
from assistant import chamar_assistente, fechar_assistente

config_file = './data/config.json'

# Check if the configuration file exists and create a new one if it doesn't
if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        default_config = {
            'current_index': 0,
            'current_router': "generico",
            'checkbox_state': {'option1': False, 'option2': False, 'option3': False}
        }
        json.dump(default_config, f)

# Load the configuration file
with open(config_file) as f:
    config = json.load(f)

# Load the list of names from the JSON file
with open('./data/systems.json') as f:
    data = json.load(f)

current_name_index = config['current_index']

event_mapping = {
    'Rota Genérica': 'generica',
    'Rota Federal': 'federal',
    'Rota Imperial': 'imperial',
    'Rota Revolta Civil': 'revolta civil',
    'Rota Militar': 'militar',
    'Rota Surto': 'surto'
}

print(config['current_router'])

hge = config['current_router']
subprocess.call(['python', 'CalcularRotas.py', hge])

# Interface principal
window = create_main_window(config, data, current_name_index, hge)

def enable_copy_button():
    time.sleep(2)  # Wait for 2 seconds
    window['Copiar'].update(disabled=False)

# Atualizar o estado dos checkboxes no arquivo de configuração
def update_checkbox_state(values):
    # Ensure 'checkbox_state' key exists in config
    if 'checkbox_state' not in config:
        config['checkbox_state'] = {}
    
    # Update checkbox states
    config['checkbox_state']['option1'] = values.get('-OPTION1-')
    config['checkbox_state']['option2'] = values.get('-OPTION2-')
    config['checkbox_state']['option3'] = values.get('-OPTION3-')

    # Write updated configuration back to file
    with open(config_file, 'w') as f:
        json.dump(config, f)


# Set the current index based on the value stored in the configuration file
def atualizarDados():
    window['-NAME-'].update(data['system'][current_name_index])
    window['-COUNTER-'].update('{}/{}'.format(current_name_index +
                                              1, len(data['system'])))
    window['-LY-'].update(data['ly'][current_name_index])

chamar_assistente(config)

# Main loop for window events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        fechar_assistente()  # Fechar o assistente antes de fechar a janela principal
        break

    elif event == 'Settings':
        main_window_location = window.CurrentLocation()
        settings_window = create_settings_window(main_window_location, config)

        while True:
            event, values = settings_window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Salvar':
                update_checkbox_state(values)  # Atualizar o estado dos checkboxes no arquivo de configuração
                window['-COLAR-SISTEMA-'].update('Ativado' if config.get('checkbox_state', {}).get('option1', False) else 'Desativado')
                window['-ASSISTENTE-STATUS-'].update('Ativado' if config.get('checkbox_state', {}).get('option1', False) else 'Desativado')
                chamar_assistente(config)
                break
        settings_window.close()

    if event == 'Voltar':
        if current_name_index > 0:
            current_name_index -= 1
            atualizarDados()
    if event == 'Copiar':
        sg.clipboard_set(data['system'][current_name_index])
        window['-CONFIRMAR-'].update(
            value=f'Copiado: ({current_name_index+1})  {data["system"][current_name_index]}  -> {data["ly"][current_name_index]}', visible=True)
        window['Próximo'].click()
        window['Copiar'].update(disabled=True)
        threading.Thread(target=enable_copy_button).start()
        
        if config.get('checkbox_state', {}).get('option1', False):  # Verificar se a opção 'Traçar Automáticas' está marcada como True
            print("## Traçando a rota! ##")
            subprocess.Popen(['python', 'ColarSystema.py'])
        else:
            print("## Traçar rotas desativado! ##")

    if event == 'Próximo':
        if current_name_index < len(data['system']) - 1:
            current_name_index += 1
            atualizarDados()

    # Verificar se o evento está presente no mapeamento
    if event in event_mapping:
        hge = event_mapping[event]  # Atribuir o valor correspondente ao evento
        current_name_index = 0

        # Call the CalcularRotas.py script with the updated 'hge' value
        subprocess.call(['python', 'CalcularRotas.py', hge])

        # Update the data on the screen after running CalcularRotas.py
        with open('./data/systems.json') as f:
            data = json.load(f)

        config['current_router'] = hge

        atualizarDados()

        window['-CONFIRMAR-'].update(
            value=f'Atualizado para {event}', visible=True)

# Update the current index in the configuration file
config['current_index'] = current_name_index
with open(config_file, 'w') as f:
    json.dump(config, f)

# Close the window when exiting the main loop
window.close()
