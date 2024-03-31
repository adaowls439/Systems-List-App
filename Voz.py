import speech_recognition as sr
from unidecode import unidecode
from logController import log as logtemp
import pydirectinput
import time
import pyttsx3
import pyperclip
import winsound  # Importa a biblioteca winsound para reprodução de sons
import subprocess

__NAME__ = "[ASSISTENTE] "
mudo = False
engine = pyttsx3.init()

comand_mapping = {
    "coletar hge",
    "proximo hge",
    "proximo sistema"
}

class ComandosPorVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.pause = False
        self.continuar_execucao = True

    def ouvir_comando(self):
        while self.continuar_execucao:
            with sr.Microphone() as source:
                log("Aguardando comando...")
                self.recognizer.adjust_for_ambient_noise(source)  # Ajusta para o ruído ambiente
                try:
                    audio = self.recognizer.listen(source, timeout=5)  # Limita a espera para 5 segundos
                    comando = self.recognizer.recognize_google(audio, language='pt-BR')
                    msg("Você disse: " + comando)
                    self.executar_acao(comando)
                except sr.UnknownValueError:
                    log("Não entendi.")
                except sr.RequestError as e:
                    print(f"Erro na requisição ao Google Speech Recognition service; {e}")
                except sr.WaitTimeoutError:
                    log("Nenhum som detectado. Continuando...")

    def executar_acao(self, comando):
        global mudo  # Informa que a variável global 'mudo' será modificada
        na = False
        com = remover_acentos(comando.lower())

        if self.pause:
            log("Aguardando...")
        else: 
            if "parar" == com:
                msg("Parando o reconhecimento de voz.")
                na = False
                self.continuar_execucao = False

            if "assistente aguarde" == com:
                msg("Aguardando ser chamada.")
                self.pause = True
                na = False

            if "assistente mudo" == com:
                mudo = True
                msg("Mudo ativado!")
                na = False
            
            if "assistente desativar mudo" == com:
                mudo = False
                msg("Mudo desativado!")
                na = False

            if "teste" == com:
                msg("Testando!")
                na = False

            ## COMANDOS IN GAME
            if com in comand_mapping:
                subprocess.call(['python', 'ComandosAssistente.py', com])
                na = False
                              
            ## CASO NÃO ENCONTRE SAÍDA
            if na:
                msg("Repita")

        if "assistente continue" == com:
            self.pause = False
            msg("Continuando!")

# macros keys
def tecla(btn):
    pydirectinput.keyDown(btn)
    time.sleep(0.000001)
    pydirectinput.keyUp(btn)


def atalho(btn, letra):
    pydirectinput.keyDown(btn)
    pydirectinput.keyDown(letra)
    time.sleep(0.1)
    pydirectinput.keyUp(btn)
    pydirectinput.keyUp(letra)

#clicks
def clicks(nome):
    x = btn[nome]['x']
    y = btn[nome]['y']

    pydirectinput.moveTo(x=x, y=y)
    pydirectinput.mouseDown()
    time.sleep(0.2) # ajuste o tempo de acordo com a necessidade
    pydirectinput.mouseUp()

# utils
def remover_acentos(texto):
    return unidecode(texto)

# Comunicação
def falar(frase):
    engine.say(f"{frase}")
    engine.runAndWait()

def bip():
    # Reproduz um som de bip com frequência de 1000 Hz e duração de 200 ms
    winsound.Beep(200, 50)

def msg(m):
    log(m)
    if not mudo:  # Se 'mudo' for False
        falar(m)
    else:
        log("bip")
        bip()  # Chama a função para reproduzir o som de bip

def log(m):
    txt = __NAME__ + m
    print(txt)
    logtemp(txt)

comandos_por_voz = ComandosPorVoz()
comandos_por_voz.ouvir_comando()
