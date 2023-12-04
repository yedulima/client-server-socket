import socket
import PySimpleGUI as sg

WIN_SCALE: tuple = (150, 100)

sg.theme('DarkBlack')

# 150 - 100
main = [
    [sg.Text('Server', justification='center', font=('Hartwell Bold', 35), expand_x=True)],
    [sg.Text('Bind to start connection', justification='center', font=('Hartwell Light', 16), expand_x=True)],
    [sg.Text()],
    [sg.Text('Server status: ', justification='center', font=('Hartwell Light', 14)), sg.Text('Inactive', justification='center', font=('Hartwell Medium', 14), text_color='red')],
    [sg.Column([
        [sg.Button('Bind', size=(15, 1))],
        [sg.Button('History', size=(15, 1))],
        [sg.Button('Monitoring', size=(15, 1))]
    ], element_justification='c', expand_x=True)]
]

main_window = sg.Window('Server', main, margins=WIN_SCALE)

def showBindWindow() -> None:
    # 20 - 10
    bind = [
        [sg.Text('HOST: ', justification='left', font=('Hartwell Light', 10)), sg.InputText('', key='-HOST-'), sg.Button('GET', size=(4, 1))],
        [sg.Text('PORT: ', justification='left', font=('Hartwell Light', 10)), sg.InputText(key='-PORT-')],
        [sg.Column([
            [sg.Button('Bind', size=(10, 1), key='-CONFIRM_BIND-')]
        ], element_justification='c', expand_x=True)]
    ]
    bind_window = sg.Window('Bind window', bind, margins=(20, 10))
    while True:
        event, values = bind_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == '-CONFIRM_BIND-':
            print("Bad Bind!")
            break

        elif event == 'GET':
            bind_window['-HOST-'].update(socket.gethostbyname(socket.gethostname()))

    bind_window.close()

while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Bind':
        showBindWindow()

main_window.close()