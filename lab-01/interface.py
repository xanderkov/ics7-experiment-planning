import matplotlib.pyplot as plt
import math
import pylab
from tkinter import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from distributions import *
from queuing_system import *

root = Tk()
root.title("Lab 1")
root.geometry("1000x800")


labRes = Label(text="")


def getModelingData(params_generator, params_handler, time):
    source_generator1 = Generator(gauss_t, params_generator)
    source_generator2 = Generator(gauss_t, params_generator)
    handler_generator1 = Handler(gauss_t, params_handler)
    gov = ModelingGoverner(
        time, [source_generator1], [handler_generator1], 0
    )
    s = gov.event()

    reqs = s.getRequests()

    n = 0

    last_creation = 0
    t_creation = 0

    t_in = 0

    t_handling = 0
    n_handled = 0
    time = s.getMaxTime()
    for r in reqs:

        if r.getHandlingTime() > 0:
            t_creation += r.getCreationTime() - last_creation
            n += 1
            t_in += r.getStartHandlingTime() + r.getHandlingTime() - r.getCreationTime()

            # if r.getStartHandlingTime() + r.getHandlingTime() < time:
            n_handled += 1
            t_handling += r.getHandlingTime()
        ##        else:
        ##            t_in += time - r.getCreationTime()
        last_creation = r.getCreationTime()

    # print(n, n_handled)
    if n_handled > 0:
        t_in /= n_handled
    if n > 0:
        t_creation /= n
    if n_handled > 0:
        t_handling /= n_handled

    return [t_in, t_creation, t_handling]


def draw():
    fig = pylab.figure(1)
    fig.clf()

    plot1 = [[], []]
    plot_theory1 = [[], []]
    i = 0.1
    while i < 0.203:
        data = getModelingData( [1 / i, 0.05], [1 / 0.1, 0.05], 1000)
        if data[1] > 0:
            plot1[0].append(1 / data[1])
        else:
            plot1[0].append(1000000)
        plot1[1].append(data[0])

        plot_theory1[0].append(i)
        plot_theory1[1].append(data[0])

        if i < 0.09:
            i += 0.01
        else:
            i += 0.001

    pylab.subplot(2, 2, 1)
    # pylab.plot(plot_theory1[0], plot_theory1[1], color='red', label = 'теория')
    pylab.plot(plot1[0], plot1[1], color='green', label="Tпреб(Iпост)")
    pylab.legend()

    plot2 = [[], []]
    plot_theory2 = [[], []]
    i = 0.2
    while i < 1:
        data = getModelingData([1 / 0.1, 0.5], [1 / i, 0.05], 1000)
        #print("mx = {:10.3f}, int = {:6.6f}, t_hand = {:6.3f}, t_cr = {:6.3f}, z = {:6.3f}, tin = {:6.3f}".format(1 / i, i , data[2], data[1], data[2]/data[1], data[0]))

        plot2[0].append(1 / data[2])
        plot2[1].append(data[0])

        plot_theory2[0].append(i)
        plot_theory2[1].append(data[0])

        if i < 0.2:
            i += 0.0005
        elif i < 1:
            i += 0.01
        else:
            i += 1

    pylab.subplot(2, 2, 2)
    # pylab.plot(plot_theory2[0], plot_theory2[1], color='red', label = 'теория')
    pylab.plot(plot2[0], plot2[1], color='green', label="Tпреб(Iобр)")
    pylab.legend()
    
    plot3 = [[], []]
    plot_theory3 = [[], []]

    # print()
    i = 0.1
    while i < 10:
        data = getModelingData([1 / 0.1, 1], [1 / i, 1], 1000)
        if data[1] > 0:
            plot3[0].append(data[2] / data[1])
            plot3[1].append(data[0])
        # else:
        #     plot3[0].append(100000)        

        # plot_theory3[0].append(0.2 / i)
        # plot_theory3[1].append(data[0])
        if i < 0.1:
            i += 0.0005
        elif i < 0.2:
            i += 0.001
        elif i < 1:
            i += 0.01
        else:
            i += 1
    plot3[0].append(0)
    plot3[1].append(0)
    pylab.subplot(2, 1, 2)
    # pylab.plot(plot_theory3[0], plot_theory3[1], color="red", label="теория")
    pylab.plot(plot3[0], plot3[1], color="green", label="T преб(загрузки)")
    pylab.legend()


    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    canvas.get_tk_widget().grid(row=5, column=0, rowspan=6, columnspan=6)


def read():
    params_generator = []
    params_handler = []
    time = 0
    try:
        params_generator = [1 / float(entry_mx_1.get()), float(entry_dx_1.get())]
        params_handler = [1 / float(entry_mx_2.get()), float(entry_dx_2.get())]

        time = float(entry_time.get())
    except Exception:
        print("error read")
    data = getModelingData(params_generator, params_handler, time)
    global labRes
    labRes.config(
        text="Загрузка системы: {:.3f} (теория) {:.3f} (факт)".format(
            params_handler[0] / params_generator[0], data[2] / data[1]
        )
    )


Label(text="интенсивность поступления заявок: ").grid(row=0, column=0)
entry_mx_1 = Entry(root)
entry_mx_1.insert(0, 0.1) 
entry_mx_1.grid(row=0, column=1)

Label(text="разброс поступления заявок: ").grid(row=0, column=2)
entry_dx_1 = Entry(root)
entry_dx_1.insert(0, 0.5) 
entry_dx_1.grid(row=0, column=3)

Label(text="интенсивность обслуживания заявок: ").grid(row=1, column=0)
entry_mx_2 = Entry(root)
entry_mx_2.insert(0, 0.1)
entry_mx_2.grid(row=1, column=1)

Label(text="разброс обслуживания заявок: ").grid(row=1, column=2)
entry_dx_2 = Entry(root)
entry_dx_2.insert(0, 0.5)
entry_dx_2.grid(row=1, column=3)


Label(text="время моделирования: ").grid(row=2, column=0)
entry_time = Entry(root)
entry_time.insert(0, 1000)
entry_time.grid(row=2, column=1)


btn = Button(root, text="результат", command=read)
btn.grid(row=3, column=0)

btnDraw = Button(root, text="показать графики", command=draw)
btnDraw.grid(row=3, column=2)

labRes.grid(row=4, column=0, columnspan=4)


root.mainloop()
