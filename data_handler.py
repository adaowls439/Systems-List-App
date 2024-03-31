import json
import os

def load_config(config_file):
    # Carregar configuração do arquivo JSON
    print("* load_config")
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

    return config

def load_system_data(data_systems):
    # Carregar dados do sistema do arquivo JSON
    print("* load_system_data")
    # Load the list of names from the JSON file
    with open('./data/systems.json') as f:
        data = json.load(f)

    return data


def save_config(config, config_file):
    # Salvar configuração no arquivo JSON
    print("* save_config")
    with open(config_file, 'w') as f:
        json.dump(config, f)

def update_checkbox_state(config, config_file, values):
    # Atualizar o estado dos checkboxes no arquivo de configuração
    print("* update_checkbox_state")
    # Ensure 'checkbox_state' key exists in config
    if 'checkbox_state' not in config:
        config['checkbox_state'] = {}
    
    # Update checkbox states
    config['checkbox_state']['option1'] = values.get('-OPTION1-')
    config['checkbox_state']['option2'] = values.get('-OPTION2-')
    config['checkbox_state']['option3'] = values.get('-OPTION3-')

    # Write updated configuration back to file
    save_config(config,config_file)

def read_log_file():
    try:
        with open('log.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""