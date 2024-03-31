import PySimpleGUI as sg
import json
import time
import threading
import os
import subprocess
import json

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

# Set the font color
font_color = '#f87532'
button_colors = ('#f87532', 'black', '#f87532')
background = '#000000'
checkbox_background_color = 'black'  # Cor de fundo do checkbox
checkbox_text_color = '#f87532'  # Cor do texto do checkbox

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

assistente_processo = None
hge = config['current_router']
subprocess.call(['python', 'CalcularRotas.py', hge])

def create_settings_window(main_window_location):
    # Definir o estado inicial dos checkboxes
    option1_state = config.get('checkbox_state', {}).get('option1', False)
    option2_state = config.get('checkbox_state', {}).get('option2', False)
    option3_state = config.get('checkbox_state', {}).get('option3', False)

    layout = [
        [sg.Checkbox('Traçar Automáticas', text_color=checkbox_text_color, background_color=checkbox_background_color, key='-OPTION1-', default=option1_state)],
        [sg.Checkbox('Reconhecimento de Voz', text_color=checkbox_text_color, background_color=checkbox_background_color, key='-OPTION2-', default=option2_state)],
        [sg.Button('Salvar', button_color=button_colors)]
    ]

    location = (main_window_location[0] + 30, main_window_location[1] + 30)

    return sg.Window('Configurações', layout, background_color=background, location=location, keep_on_top=True)


# Define the window layout
layout = [
    [sg.Menu([['&Menu', ['&About', '&Settings', '&Exit']], ['&HGE', ['Rota Genérica','Rota Federal', 'Rota Imperial','Rota Revolta Civil', 'Rota Militar', 'Rota Surto']]], key='-MENU-')],
    [sg.Text('System', size=(20, 1), font=('Arial', 12), justification='right', text_color=font_color, background_color='black'),
     sg.Text('{}/{}'.format(current_name_index+1, len(data['system'])), size=(20, 1), font=('Arial', 12), justification='left', text_color=font_color, background_color='black', key='-COUNTER-')],
    [sg.Text(data['system'][current_name_index], size=(22, 1), font=('Arial', 18, 'bold'), background_color='black', justification='center', key='-NAME-'),
     sg.Text(data['ly'][current_name_index], size=(7, 1), font=('Arial', 18, 'bold'), background_color='black', justification='left', key='-LY-')],
    [sg.Button('Voltar', button_color=button_colors), sg.Button(
        'Copiar', button_color=button_colors), sg.Button('Próximo', button_color=button_colors)],
    [sg.Text(f'Iniciado com rota {hge}', size=(400, 1), font=('Arial', 9), justification='left',
             text_color='#00FF00', background_color='black', visible=True, key='-CONFIRMAR-')],
    [sg.Text('Assistente comandos: Coletar HGE, Próximo HGE, Assistente Aguarde', size=(400, 1), font=('Arial', 9), justification='left', text_color=font_color, background_color='black',visible=True, key='-ASSISTENTE-')],
    [sg.Text('Assistente Mudo, Assistente Desativar Mudo.', size=(400, 1), font=('Arial', 9), justification='left', text_color=font_color, background_color='black',visible=True, key='-CMDS-')]
]

sg.set_options(icon='./icon/logo.ico')

# Create the window
window = sg.Window('Lista de Sistemas. by: adaowls439', layout,
                   element_justification='center', size=(525, 180), background_color=background, keep_on_top=True, finalize=True)

# Função para chamar o assistente.py se a opção "Escutar" estiver habilitada
def chamar_assistente():
    global assistente_processo
    if config.get('checkbox_state', {}).get('option2', False):  # Verifica se a opção 'Escutar' está habilitada
        print("## Iniciando Assistente ##")
        assistente_processo = subprocess.Popen(['python', 'Assistente.py'])
    else:
        fechar_assistente()
# Função para fechar o assistente se estiver em execução
def fechar_assistente():
    global assistente_processo
    if assistente_processo and assistente_processo.poll() is None:  # Verifica se o assistente está em execução
        print("## Desligando Assistente ##")
        assistente_processo.terminate()  # Encerra o processo do assistente

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

chamar_assistente()

# Main loop for window events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        window['-ASSISTENTE-'].update(visible=False)
        fechar_assistente()
        break

    elif event == 'Settings':
        main_window_location = window.CurrentLocation()
        settings_window = create_settings_window(main_window_location)

        while True:
            event, values = settings_window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Salvar':
                update_checkbox_state(values)  # Atualizar o estado dos checkboxes no arquivo de configuração
                chamar_assistente()
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
fechar_assistente()
window.close()

