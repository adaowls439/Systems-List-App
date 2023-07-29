from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed and button == button.left:
        print(f"Mouse position: ({x}, {y})")

with Listener(on_click=on_click) as listener:
    listener.join()