import sys
import time
import pydirectinput

# mouse posi
local = {"Game": {"x": 200, "y": 200}}

## utills
def tecla(btn):
    pydirectinput.keyDown(btn)
    time.sleep(0.3)
    pydirectinput.keyUp(btn)

def teclaTime(btn, tempo):
    pydirectinput.keyDown(str(btn))
    time.sleep(tempo)
    pydirectinput.keyUp(str(btn))

def tempo(t):
    time.sleep(t)

def clicks(nome, btn):
    x = local[nome]['x']
    y = local[nome]['y']

    pydirectinput.moveTo(x=x, y=y)
    pydirectinput.mouseDown(button=btn)
    time.sleep(0.2) # ajuste o tempo de acordo com a necessidade
    pydirectinput.mouseUp(button=btn)



## comandos
def coletarHGE():
    print("1")
    clicks("Game","left")
    tecla("insert")
    tecla("delete")
    teclaTime("w", 6.5)
    tecla("p")
    clicks("Game","right")
    tempo(3)
    clicks("Game","right")
    tempo(3)
    clicks("Game","right")
    tecla("home")

def proximoHGE():
    print("2")
    clicks("Game","left")
    tecla("u")
    tecla("home")
    tecla("k")
    tecla("shiftleft")
    tecla("insert")
    tecla("delete")

def proximoSistema():
    print("3")

# case
def executar(cmd):
    switcher = {
        "coletar hge": coletarHGE,
        "proximo hge": proximoHGE,
        "proximo sistema": proximoSistema
    }
    func = switcher.get(cmd)
    func()

# init
if __name__ == '__main__':
    cmd = sys.argv[1]
    #cmd = "proximo hge"
    print(cmd)
    executar(cmd)
