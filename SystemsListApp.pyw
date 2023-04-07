import PySimpleGUI as sg
import json
import time
import threading
import os
import subprocess
import json

# Chama o script listCMDTBOX.py
subprocess.call(['python', 'CalcularRotas.py'])

config_file = './data/config.json'
# Verifica se o arquivo de configuração existe e cria um novo se não existir
if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        json.dump({'current_index': 0}, f)

# Carrega o arquivo de configuração
with open(config_file) as f:
    config = json.load(f)

# carrega a lista de nomes do arquivo JSON
with open('./data/systems.json') as f:
    data = json.load(f)

# define a cor da fonte
font_color = '#f87532'
button_cores = ('#f87532', 'black', '#f87532')

current_name_index = config['current_index']

# define o layout da janela
layout = [
    [sg.Text('System', size=(20,1), font=('Arial', 12), justification='right', text_color=font_color, background_color='black'),
     sg.Text('{}/{}'.format(current_name_index+1, len(data['system'])), size=(20,1), font=('Arial', 12), justification='left', text_color=font_color, background_color='black', key='-COUNTER-')],
    [sg.Text(data['system'][current_name_index], size=(18,1), font=('Arial', 18, 'bold'), background_color='black', justification='center', key='-NAME-'),
     sg.Text(data['ly'][current_name_index], size=(7,1),font=('Arial', 18, 'bold'), background_color='black', justification='left', key='-LY-')],
    [sg.Button('Voltar', button_color=button_cores), sg.Button('Copiar', button_color=button_cores), sg.Button('Próximo', button_color=button_cores)],
    [sg.Text('Copiado', size=(400,1), font=('Arial', 9), justification='left', text_color='#00FF00', background_color='black', visible=False, key='-CONFIRMAR-')]
]

sg.set_options(icon='./icon/logo.ico')

# cria a janela
window = sg.Window('Lista de Sistemas. by: adaowls439', layout, element_justification='center', size=(425, 135), background_color='black')

def enable_copy_button():
    time.sleep(2)  # espera 5 segundos
    window['Copiar'].update(disabled=False)


# Define o índice atual com base no valor armazenado no arquivo de configuração

# loop principal para eventos da janela
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Voltar':
        if current_name_index > 0:
            current_name_index -= 1
            window['-NAME-'].update(data['system'][current_name_index])
            window['-COUNTER-'].update('{}/{}'.format(current_name_index+1, len(data['system'])))
            window['-LY-'].update(data['ly'][current_name_index])
    if event == 'Copiar':
        sg.clipboard_set(data['system'][current_name_index])
        window['-CONFIRMAR-'].update(value=f'Copiado: ({current_name_index+1})  {data["system"][current_name_index]}  -> {data["ly"][current_name_index]}', visible=True)
        window['Próximo'].click()
        window['Copiar'].update(disabled=True)
        threading.Thread(target=enable_copy_button).start()

    if event == 'Próximo':
        if current_name_index < len(data['system']) - 1:
            current_name_index += 1
            window['-NAME-'].update(data['system'][current_name_index])
            window['-COUNTER-'].update('{}/{}'.format(current_name_index+1, len(data['system'])))
            window['-LY-'].update(data['ly'][current_name_index])


# Atualiza o índice atual no arquivo de configuração
        config['current_index'] = current_name_index
        with open(config_file, 'w') as f:
            json.dump(config, f)

# fecha a janela ao sair do loop principal
window.close()
