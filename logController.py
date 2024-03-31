import datetime

log_file = 'log.txt'

def read_log_file():
    #print("* read_log_file")
    try:
        with open(log_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def log(msg):
    # Escreve algo no arquivo de log
    print("* log")
    timestamp = datetime.datetime.now().strftime("[%d/%m %H:%M:%S]")
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - {msg}\n")

def logClear():
    # Limpa o arquivo de logs
    print("* logClear")
    open(log_file, 'w').close()
