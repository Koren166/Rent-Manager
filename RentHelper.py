import PySimpleGUI as sg
import matplotlib.pyplot as plt


def average(lst):
    return sum(lst) / len(lst)


def create_subplot(subplt, xdata, ydata, color, title):
    """Creates a subplot with given data
        :param subplt: The subplot name
        :param xdata: The list of values for x axis
        :param ydata: The list of values for y axis
        :param color: The color of the plot line
        :param title: The title of the subplot"""

    subplt.plot(xdata, ydata, marker='o', color=color)
    subplt.title.set_text(title)
    for x, y in zip(xdata, ydata):
        label = "{:.2f}".format(y)
        subplt.annotate(label, (x, y), textcoords="offset points",
                        xytext=(0, 5), ha='center')
    subplt.axhline(average(ydata), color=color, linestyle='dashed', linewidth=1)
    return


def show_plot(filename):
    date_label = []
    water_data = []
    elec_data = []
    total_data = []

    # file handling
    f = open(filename, 'r')
    for row in f:
        line = row.strip().split(',')
        date_label.append(str(line[0]) + '/' + str(line[1]))
        water_data.append(float(line[2]))
        elec_data.append(float(line[3]))
        total_data.append(float(line[4]))
    f.close()

    # create the plot
    fig, (water_fig, elec_fig, total_fig) = plt.subplots(3, sharex=True)
    create_subplot(water_fig, date_label, water_data, 'b', 'Water')
    create_subplot(elec_fig, date_label, elec_data, 'g', 'Electricity')
    create_subplot(total_fig, date_label, total_data, 'r', 'Total rent')
    fig.tight_layout()
    plt.show(block=False)
    return


def add_data(fn, m, y, w, e, t):
    new_row = '\n' + str(m) + ',' + str(y) + ',' + str(w) + ',' + str(e) + ',' + str(t)
    f = open(fn, 'a')
    f.write(new_row)
    f.close()
    return


layout1 = [[sg.Text('Select data file:')],
           [sg.InputText(key='-FILENAME-', default_text='D:/Coding - Python/Projects/Rent Automation/rent_data.csv'),
            sg.FileBrowse(target='-FILENAME-')]]

layout2 = [[sg.Text('Add new month data:')],
           [sg.Input(key='-MONTH-', size=(7, 1)), sg.Input(key='-YEAR-', size=(7, 1)),
            sg.Input(key='-WATER-', size=(7, 1)), sg.Input(key='-ELEC-', size=(7, 1)),
            sg.Input(key='-TOTAL-', size=(7, 1)), sg.Button('Submit', key='-ADD_DATA-')],
           [sg.Text('  Month  '), sg.Text('  Year   '), sg.Text('  Water '),
            sg.Text('Electricity'), sg.Text(' Total')]]

layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-')],
          [sg.Button('Select Data File', key='1'), sg.Button('Add Data', key='2'),
           sg.Button('Display Plot', key='-PLOT-'), sg.Button('Exit')]]

sg.theme('systemdefault')
window = sg.Window('Rent Organizer', layout)
layout = 1  # The currently visible layout
while True:
    event, values = window.read()

    if event in (None, 'Exit', sg.WIN_CLOSED):
        break

    file_name = values['-FILENAME-']
    month = values['-MONTH-']
    year = values['-YEAR-']
    water = values['-WATER-']
    elec = values['-ELEC-']
    total = values['-TOTAL-']

    if event in '12':
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(event)
        window[f'-COL{layout}-'].update(visible=True)

    if event == '-ADD_DATA-':
        add_data(file_name, month, year, water, elec, total)
        window['-MONTH-'].update('')
        window['-YEAR-'].update('')
        window['-WATER-'].update('')
        window['-ELEC-'].update('')
        window['-TOTAL-'].update('')

    if event == '-PLOT-':
        show_plot(file_name)

window.close()
