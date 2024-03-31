import PySimpleGUI as sg
import time
import threading
import subprocess
from interface import create_settings_window, create_main_window
from assistant import chamar_assistente, fechar_assistente
from data_handler import load_config, load_system_data, save_config, update_checkbox_state
from logController import log, logClear, read_log_file


config_file = './data/config.json'
data_systems = './data/systems.json'
config = load_config(config_file)
data = load_system_data(data_systems)

chamar_assistente(config)

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

# Set the current index based on the value stored in the configuration file
def atualizarDados():
    window['-NAME-'].update(data['system'][current_name_index])
    window['-COUNTER-'].update('{}/{}'.format(current_name_index +
                                              1, len(data['system'])))
    window['-LY-'].update(data['ly'][current_name_index])


def closeAppSafe():
    fechar_assistente()  # Fechar o assistente antes de fechar a janela principal
    logClear() # Limpa o log temporario

def update_log_field(window):
    while True:
        log_text = read_log_file()
        window.write_event_value('-UPDATE-LOG-', log_text)
        time.sleep(1)

log_update_thread = threading.Thread(target=update_log_field, args=(window,), daemon=True)
log_update_thread.start()

# Main loop for window events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        closeAppSafe()
        break

    elif event == 'Settings':
        main_window_location = window.CurrentLocation()
        settings_window = create_settings_window(main_window_location, config)

        while True:
            event, values = settings_window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Salvar':
                update_checkbox_state(config, config_file,values)  # Atualizar o estado dos checkboxes no arquivo de configuração
                window['-COLAR-SISTEMA-'].update('Ativado' if config.get('checkbox_state', {}).get('option1', False) else 'Desativado')
                window['-ASSISTENTE-STATUS-'].update('Ativado' if config.get('checkbox_state', {}).get('option2', False) else 'Desativado')  # Aqui atualizamos com base na opção 2
                chamar_assistente(config)
                break
        settings_window.close()

    if event == 'Voltar':
        if current_name_index > 0:
            current_name_index -= 1
            atualizarDados()

    if event == 'Copiar':
        sg.clipboard_set(data['system'][current_name_index])
        msg = f'Copiado: ({current_name_index+1})  {data["system"][current_name_index]}  -> {data["ly"][current_name_index]}'
        window['-CONFIRMAR-'].update(value=msg, visible=True)
        log(msg)
        window['Próximo'].click()
        window['Copiar'].update(disabled=True)
        threading.Thread(target=enable_copy_button, daemon=True).start()
        
        if config.get('checkbox_state', {}).get('option1', False):  # Verificar se a opção 'Traçar Automáticas' está marcada como True
            print("## Traçando a rota! ##")
            subprocess.Popen(['python', 'ColarSystema.py'])
        else:
            print("## Traçar rotas desativado! ##")

    if event == 'Próximo':
        if current_name_index < len(data['system']) - 1:
            current_name_index += 1
            atualizarDados()
    
    elif event == '-UPDATE-LOG-':
        window['-LOG-'].update(value=values['-UPDATE-LOG-'])

    # Verificar se o evento está presente no mapeamento
    if event in event_mapping:
        hge = event_mapping[event]  # Atribuir o valor correspondente ao evento
        current_name_index = 0

        # Call the CalcularRotas.py script with the updated 'hge' value
        subprocess.call(['python', 'CalcularRotas.py', hge])

        # Update the data on the screen after running CalcularRotas.py
        data = load_system_data('./data/systems.json')

        config['current_router'] = hge

        atualizarDados()

        msg = f'Atualizado para {event}'
        window['-CONFIRMAR-'].update(value=msg, visible=True)
        log(msg)

# Update the current index in the configuration file
config['current_index'] = current_name_index
save_config(config, config_file)

# Close the window when exiting the main loop
window.close()
