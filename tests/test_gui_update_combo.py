import PySimpleGUI as sg

layout = [[sg.Text('Your typed chars appear here:'), sg.InputCombo(values=['1','2','3'],size=(5,1),key='OUTPUT')],
            [sg.Input(do_not_clear=True, key='IN')],
            [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Window Title').Layout(layout)

while True: # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Show':
        # change the "output" element to be the value of "input" element
        window.FindElement('OUTPUT').Update(values=values['IN'].split(','))
window.Close()