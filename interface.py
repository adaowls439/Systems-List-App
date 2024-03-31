import PySimpleGUI as sg

# Set the font color
font_color = '#f87532'
button_colors = ('#f87532', 'black', '#f87532')
background = '#000000'
checkbox_background_color = 'black'  # Cor de fundo do checkbox
checkbox_text_color = '#f87532'  # Cor do texto do checkbox

def create_main_window(config, data, current_name_index, hge):
    print("* create_main_window")
    # Definição da janela principal
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
        [sg.Text('Assistente Mudo, Assistente Desativar Mudo.', size=(400, 1), font=('Arial', 9), justification='left', text_color=font_color, background_color='black',visible=True, key='-CMDS-')],
        [sg.Text('Colar Sistema:', size=(15, 1), font=('Arial', 9), justification='left', text_color=font_color, background_color='black'),
        sg.Text('Ativado' if config.get('checkbox_state', {}).get('option1', False) else 'Desativado', size=(10, 1), font=('Arial', 9), justification='left', text_color='#00FF00' if config.get('checkbox_state', {}).get('option1', False) else '#FF0000', background_color='black', key='-COLAR-SISTEMA-')],
        [sg.Text('Assistente:', size=(15, 1), font=('Arial', 9), justification='left', text_color=font_color, background_color='black'),
        sg.Text('Ativado' if config.get('checkbox_state', {}).get('option2', False) else 'Desativado', size=(10, 1), font=('Arial', 9), justification='left', text_color='#00FF00' if config.get('checkbox_state', {}).get('option2', False) else '#FF0000', background_color='black', key='-ASSISTENTE-STATUS-')]
    ]

    sg.set_options(icon='./icon/logo.ico')

    return sg.Window('Lista de Sistemas. by: adaowls439', layout,
                    element_justification='center', size=(525, 400), background_color=background, keep_on_top=True, finalize=True)

def create_settings_window(main_window_location, config):
    print("* create_settings_window")
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
