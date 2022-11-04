import PySimpleGUI as sg


layout = [
    [sg.Text("hello there")],
    [sg.Button("OK")]
]

window = sg.Window("Demo", layout)

while True:
    event, values = window.read()

    if event == "OK" or event == sg.WIN_CLOSED:
        break


window.close()
