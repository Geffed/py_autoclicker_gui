import time
import threading
import PySimpleGUI as sg

from pynput.mouse import Button, Controller

#global variables for autoclicker
delay = 1.0
button = Button.left
# instance of mouse controller is created
mouse = Controller()

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.do_click = False

    def start_clicking(self):
        self.do_click = True
  
    def stop_clicking(self):
        self.do_click = False

    def press(self):
        if self.do_click == True:
            mouse.click(self.button)
            time.sleep(self.delay)

#PySimpleGUI Window Variables
sg.theme('DarkAmber')
layout = [  [sg.Text('Default delay is set to 1')],
            [sg.Text('Set delay: '), sg.InputText(key='delayinput'), sg.Button('Save')],
            [sg.Button('Start'), sg.Button('Stop'), sg.Button('Exit')]
        ]

window = sg.Window('Auto Clicker', layout)

click_thread = ClickMouse(delay, button)
click_thread.start()

# Event Loop to process "events" and get the "values" of the inputs
while True:   
    if click_thread.do_click == True:
         click_thread.press()
    
    event, values = window.read(timeout = delay)

    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    elif event == 'Save':
        delay = float(values['delayinput'])
        click_thread.delay = delay
    elif event == 'Start':        
        click_thread.start_clicking()
    elif event == 'Stop':
        click_thread.stop_clicking()
        
window.close()