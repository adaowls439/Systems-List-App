import time
import pydirectinput

local = {"Game": {"x": 200, "y": 200}, "Pesquisar": {"x": 882, "y": 120}, "Pesquisar_Proximo": {"x": 1216, "y": 119}}

def executar():
    clicks("Game")
    pydirectinput.press('ctrlright')
    time.sleep(2) 
    clicks("Pesquisar")
    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('v')
    time.sleep(0.3)
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('v')
    time.sleep(0.3)
    clicks("Pesquisar_Proximo")
    pydirectinput.moveTo(x=500, y=500)
    pydirectinput.keyDown('space')
    time.sleep(1)
    pydirectinput.keyUp('space')
    time.sleep(0.3)
    pydirectinput.press('ctrlright')

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
