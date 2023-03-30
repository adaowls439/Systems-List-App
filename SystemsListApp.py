import PySimpleGUI as sg
import json


# carrega a lista de nomes do arquivo JSON
with open('./data/systems.json') as f:
    names = json.load(f)

# define a cor da fonte
font_color = '#f87532'
button_cores = ('#f87532', 'black', '#f87532')


# define o layout da janela
layout = [
    [sg.Text('System', size=(20,1), font=('Arial', 12), justification='right', text_color=font_color, background_color='black'),
     sg.Text('1/{}'.format(len(names)), size=(20,1), font=('Arial', 12), justification='left', text_color=font_color, background_color='black', key='-COUNTER-')],
    [sg.Text(names[0], size=(50,1), font=('Arial', 18, 'bold'), background_color='black', justification='center', key='-NAME-')],
    [sg.Button('Voltar', button_color=button_cores), sg.Button('Copiar', button_color=button_cores), sg.Button('Próximo', button_color=button_cores)]
]

sg.set_options(icon='./icon/logo.ico')

# cria a janela
window = sg.Window('Lista de Sistemas. by: adaowls439', layout, element_justification='center', size=(400, 110), background_color='black')



# loop principal para eventos da janela
current_name_index = 0
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Voltar':
        if current_name_index > 0:
            current_name_index -= 1
            window['-NAME-'].update(names[current_name_index])
            window['-COUNTER-'].update('{}/{}'.format(current_name_index+1, len(names)))
    if event == 'Copiar':
        sg.clipboard_set(names[current_name_index])
    if event == 'Próximo':
        if current_name_index < len(names) - 1:
            current_name_index += 1
            window['-NAME-'].update(names[current_name_index])
            window['-COUNTER-'].update('{}/{}'.format(current_name_index+1, len(names)))

# fecha a janela ao sair do loop principal
window.close()
