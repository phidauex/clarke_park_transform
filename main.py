#! /usr/bin/python3

# Tkinter test
print('Tkinter tests\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

from tkinter import *
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
import transforms as trs

### Function that transforms and
### plots the results
def ex_transform(*args):
    if phaseA.get()=="" or phaseB.get()=="" or phaseC.get()=="" or freq.get()=="" or unit.get()=="" or delta.get()=="":
        return 0
    
    end_time = 10/float(freq.get())
    step_size = end_time/(1000)
    t = np.arange(0,end_time,step_size)
    wt = 2*np.pi*float(freq.get()) * t
    # t = np.arange(0,6*np.pi/float(freq.get()),0.01/float(freq.get()))
    # wt = float(freq.get())*t
    if mag_val.get()=="peak":
        A = float(phaseA.get())*np.sin(wt)
        B = float(phaseB.get())*np.sin(wt-(2*np.pi/3))
        C = float(phaseC.get())*np.sin(wt+(2*np.pi/3))
    else:
        if mag_val.get()=="rms":
            A = (np.sqrt(2)*float(phaseA.get()))*np.sin(wt)
            B = (np.sqrt(2)*float(phaseB.get()))*np.sin(wt-(2*np.pi/3))
            C = (np.sqrt(2)*float(phaseC.get()))*np.sin(wt+(2*np.pi/3))
        else:
            return 0

    # apply the fault
    if fault.get() == 'Monophasic A':
        for ii in range(int(len(t)/4), int(3*len(t)/4)):
            A[ii]=0
    elif fault.get() == 'Monophasic B':
        for ii in range(int(len(t)/4), int(3*len(t)/4)):
            B[ii]=0
    elif fault.get() == 'Monophasic C':
        for ii in range(int(len(t)/4), int(3*len(t)/4)):
            C[ii]=0
    elif fault.get() == 'Biphasic A-B':
        for ii in range(int(len(t)/4), int(3*len(t)/4)):
            A[ii]=0
            B[ii]=0
    elif fault.get() == 'Biphasic B-C':
        for ii in range(int(len(t)/4), int(3*len(t)/4)):
            B[ii]=0
            C[ii]=0
    elif fault.get() == 'Biphasic C-A':
        for ii in range(int(len(t)/4), int(3*len(t)/4)):
            C[ii]=0
            A[ii]=0


    delta_rad = float(delta.get())*np.pi/180 # convert delta to radians
    # calling transformation functions
    alpha, beta, zero1 = trs.abc_to_alphaBeta0(A,B,C)
    d, q, zero2 = trs.alphaBeta0_to_dq0(alpha, beta, zero1, wt, delta_rad)
    a,b,c = trs.dq0_to_abc(d, q, zero2, wt, delta_rad)

    plt.clf() # clear any previous plots
    # Plot the 3-phase system
    plt.subplot(411)
    plt.plot(t, A, label="A")
    plt.plot(t, B, label="B")
    plt.plot(t, C, label="C")
    plt.ylabel(unit.get())
    plt.legend(ncol=3,loc=4)
    # Plot the alphaBeta0 system
    plt.subplot(412)
    plt.plot(t, alpha, label="\u03B1")
    plt.plot(t, beta, label="\u03B2")
    plt.plot(t, zero1, label="zero")
    plt.ylabel(unit.get())
    plt.legend(ncol=3,loc=4)
    # Plot the dq0 system
    plt.subplot(413)
    plt.plot(t, d, label="d")
    plt.plot(t, q, label="q")
    plt.plot(t, zero2, '-', label="zero")
    plt.xlabel('Time [s]')
    plt.ylabel(unit.get())
    plt.legend(ncol=3,loc=4)
    # Plot the abc transformed from dq0
    plt.subplot(414)
    plt.plot(t, a, label="A")
    plt.plot(t, b, label="B")
    plt.plot(t, c, label="C")
    plt.ylabel(unit.get())
    plt.legend(ncol=3,loc=4)
    plt.show()
########################################
#### Function to validate user input
def validate_val(char):
    return  char=="." or char.isdigit()
########################################

root = Tk()
root.title("Clark's and Park's Transformations")
mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

validation = mainframe.register(validate_val)

### Creating variables to store user input
phaseA = StringVar() # stores magnitude of phase A
phaseB = StringVar() # stores magnitude of phase B
phaseC = StringVar() # stores magnitude of phase C
freq = StringVar() # stores the system frequency os oscilation
unit = StringVar() # stores the system unit
fault = StringVar() # stores the system fault type
mag_val = StringVar() # stores the type of magnitude used
delta = StringVar() # stores the angle in degrees between the A and d axis in clarke trans.
########################################

# Creates label and Combobox for system unit
ttk.Label(mainframe, text="Unit:").grid(column=1, row=1, sticky=E)
unit_combobox = ttk.Combobox(mainframe, state="readonly", textvariable=unit, width=15)
unit_combobox.grid(column=2,row=1, sticky=(W,E))
unit_combobox['values'] = ('Voltage [V]', 'Voltage [kV]')
unit_combobox.bind('<FocusOut>', lambda e: unit_combobox.selection_clear())
########################################

# Creates label and radio buttons for magnitude selection
ttk.Label(mainframe, text="Magnitude:"). grid(column=1, row=2, sticky=E)
## creates frame to hold radio buttons nicely
radio_frame=ttk.Frame(mainframe, padding=("10 0 0 0"))
radio_frame.grid(column=2, row=2, sticky=(W, E))
peak_val = ttk.Radiobutton(radio_frame, text="Peak", variable=mag_val, value="peak")
peak_val.grid(column=1, row=1, sticky=(W, E))
rms_val = ttk.Radiobutton(radio_frame, text="RMS", variable=mag_val, value="rms")
rms_val.grid(column=2,row=1, sticky=(W, E))
########################################

# Creates label and text entry for frequency
ttk.Label(mainframe, text="Frequency [Hz]:").grid(column=1, row=3, sticky=W)
freq_entry = ttk.Entry(mainframe, validate="key", validatecommand=(validation, '%S'), width=7, textvariable=freq)
freq_entry.grid(column=2, row=3, sticky=W)
########################################

# Creates label and Combobox for fault type
ttk.Label(mainframe, text="Fault:").grid(column=1, row=4, sticky=E)
fault_combobox = ttk.Combobox(mainframe, state="readonly", textvariable=fault, width=15)
fault_combobox.grid(column=2,row=4, sticky=(W,E))
fault_combobox['values'] = ('None','Monophasic A', 'Monophasic B', 'Monophasic C', 'Biphasic A-B','Biphasic B-C','Biphasic C-A')
fault_combobox.bind('<FocusOut>', lambda e: fault_combobox.selection_clear())
########################################

# Creates label and text entry for phase A
ttk.Label(mainframe, text="Phase A:", padding=("10 0 0 0")).grid(column=3, row=1, sticky=E)
phaseA_entry = ttk.Entry(mainframe, validate="key", validatecommand=(validation, '%S'), width=7, textvariable=phaseA)
phaseA_entry.grid(column=4, row=1, sticky=(W, E), pady=3)
########################################

# Creates label and text entry for phase B
ttk.Label(mainframe, text="Phase B:",padding=("10 0 0 0")).grid(column=3, row=2, sticky=E)
phaseB_entry = ttk.Entry(mainframe, validate="key", validatecommand=(validation, '%S'), width=7, textvariable=phaseB)
phaseB_entry.grid(column=4, row=2, sticky=(W, E), pady=3)
########################################

# Creates label and text entry for phase C
ttk.Label(mainframe, text="Phase C:", padding=("10 0 0 0")).grid(column=3, row=3, sticky=E)
phaseC_entry = ttk.Entry(mainframe, validate="key", validatecommand=(validation, '%S'), width=7, textvariable=phaseC)
phaseC_entry.grid(column=4, row=3, sticky=(W, E), pady=3)
########################################

# Creates label and text entry for delta
ttk.Label(mainframe, text="delta [degrees]:", padding=("10 0 0 0")).grid(column=3, row=4, sticky=E)
delta_entry = ttk.Entry(mainframe, validate="key", validatecommand=(validation, '%S'), width=7, textvariable=delta)
delta_entry.grid(column=4, row=4, sticky=(W,E), pady=3)
########################################


# Creates button to call transformation function
trans_button = ttk.Button(mainframe, text="Calculte", command=ex_transform,padding=("3 3 3 3"))
trans_button.grid(column=4, row=5, pady= 10,sticky=E)
########################################

root.mainloop() # Starts Tkinter loop