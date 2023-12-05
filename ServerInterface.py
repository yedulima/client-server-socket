from Server import Server

import socket
import PySimpleGUI as sg
import threading
import multiprocessing
import os

WIN_SCALE: tuple = (150, 100)
process_pid: int = 0

sg.theme('DarkBlack')

server_status = 'Inactive'

# 150 - 100
main = [
    [sg.Text('Server', justification='center', font=('Hartwell Bold', 35), expand_x=True)],
    [sg.Text('Bind to start connection', justification='center', font=('Hartwell Light', 16), expand_x=True)],
    [sg.Text()],
    [sg.Text('Server status: ', justification='center', font=('Hartwell Light', 14)), sg.Text(server_status, justification='center', font=('Hartwell Medium', 14), key='-SERVER_STATUS-')],
    [sg.Column([
        [sg.Button('Bind', size=(15, 1))],
        [sg.Button('History', size=(15, 1))],
        [sg.Button('Monitoring', size=(15, 1))]
    ], element_justification='c', expand_x=True)]
]

def errorWindow():
    error = [
        [sg.Text('Error', justification='center', font=('Hartwell Medium', 15), expand_x=True)],
        [sg.Column([
            [sg.Button('OK', key='-OK-')]
        ], element_justification='c', expand_x=True)]
    ]
    error_window = sg.Window('', error, margins=(50, 1))
    while True:
        event, _ = error_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-OK-':
            break
    error_window.close()
    
main_window = sg.Window('Server', main, margins=WIN_SCALE)

def showBindWindow() -> bool:

    global process_pid

    # 20 - 10
    bind = [
        [sg.Text('HOST: ', justification='left', font=('Hartwell Light', 10)), sg.InputText('', key='-HOST-'), sg.Button('GET', size=(4, 1))],
        [sg.Text('PORT: ', justification='left', font=('Hartwell Light', 10)), sg.InputText('', key='-PORT-')],
        [sg.Column([
            [sg.Button('Bind', size=(10, 1), key='-CONFIRM_BIND-')]
        ], element_justification='c', expand_x=True)]
    ]
    bind_window = sg.Window('Bind window', bind, margins=(20, 10))
    verify: bool = False
    while True:
        event, values = bind_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == '-CONFIRM_BIND-' and len(values['-PORT-']) and len(values['-HOST-']):
            try:
                int(values['-PORT-'])
            except:
                values['-PORT-'].update('')
                errorWindow()
            else:
                if int(values['-PORT-']) < 1024 or not values['-HOST-']:
                    bind_window['-PORT-'].update('')
                    errorWindow()
                    continue
                
                # Bind connect here
                _ = Server(values['-HOST-'], int(values['-PORT-']))
                verify = True
                break

        elif event == 'GET':
            bind_window['-HOST-'].update(socket.gethostbyname(socket.gethostname()))

        else:
            errorWindow()

    bind_window.close()

    if verify:
        server = multiprocessing.Process(target=_.startServer)
        server.start()
        process_pid = server.pid
        return True
    return False

while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        if server_status == 'Active':
            os.kill(process_pid, 1)
            print("[SERVER] Server closed automatically.")
        break
    if event == 'Bind':
        response = showBindWindow()
        if response:
            server_status = 'Active'
            main_window['-SERVER_STATUS-'].update(server_status)

main_window.close()
