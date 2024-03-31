import time
import pydirectinput

local = {"Game": {"x": 200, "y": 200}, "Pesquisar": {"x": 882, "y": 120}, "Pesquisar_Proximo": {"x": 1216, "y": 119}, "tracar": {"x": 1830,"y":600}}

def executar():
    clicks("Game")
    pydirectinput.keyDown("/")
    time.sleep(0.3)
    pydirectinput.keyUp("/")
    time.sleep(2) 
    clicks("Pesquisar")
    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('v')
    time.sleep(0.3)
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('v')
    time.sleep(0.3)
    clicks("Pesquisar_Proximo")
    time.sleep(1)
    pydirectinput.moveTo(x=500, y=500)
    clicks("tracar")
    time.sleep(0.3)
    pydirectinput.press('/')

def clicks(nome):
    x = local[nome]['x']
    y = local[nome]['y']

    pydirectinput.moveTo(x=x, y=y)
    pydirectinput.mouseDown()
    time.sleep(0.2) # ajuste o tempo de acordo com a necessidade
    pydirectinput.mouseUp()
    time.sleep(0.2) 

if __name__ == '__main__':
    executar()
