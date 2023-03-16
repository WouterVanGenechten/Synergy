#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:43:35 2023

@author: u0107886 : Wouter Van Genechten
"""

def Calculatesynergy():
    from synergy.combination import MuSyC # or BRAID, Zimmer
    import pandas as pd
    from csv_synergy import Checkerboardwriter
    from csv_synergy import Synergyplotter
    import webbrowser

    Checkerboardwriter(Doxycycline_conc_max = 400, Dox_number = 6,\ #drug 1 max conc and amount of dilutions
                   Fluconazole_conc_max = 64, Fluc_number = 10,\ #drug 2 max conc and amount of dilutions
                   importfile = "import.csv",\   #This should be a 6row, 10 column csv file with 1 being full growth and 0 being no growth
                   exportfile = "export.csv" )   #this will become a file which can be read by the synergycalculator
    
    model = MuSyC(E0_bounds=(0,1), E1_bounds=(0,1), E2_bounds=(0,1), E3_bounds=(0,1))
    model.fit(df['drug1.conc'], df['drug2.conc'], df['effect'], bootstrap_iterations=100)
    print(model.summary())
        
    df = pd.read_csv("export.csv")

def Checkerboardwriter(Doxycycline_conc_max = 400, Dox_number = 6, Fluconazole_conc_max = 64,\
                   Fluc_number = 10, importfile = "import.csv",\
                       exportfile = 'export.csv'):
    import csv
    doxycycline_concentrations = []
    fluconazole_concentrations = []
    dilution = 1
    for i in range(1, Dox_number):
        doxycycline_concentrations.append(Doxycycline_conc_max/dilution)
        dilution = dilution*2
    dilution = 1
    for i in range(1, Fluc_number):
        fluconazole_concentrations.append(Fluconazole_conc_max/dilution)
        dilution = dilution*2
    doxycycline_concentrations.append(0)
    fluconazole_concentrations.append(0)
    fluconazole_concentrations.reverse()
    
    
    with open(importfile, 'r') as inp, open(exportfile, 'w', newline='') as outp:
        csvreader = csv.reader(inp)
        writer = csv.writer(outp)
        first_row = ["drug1.conc","drug2.conc","effect"]
        writer.writerow(first_row)
        i = 0
        for row in csvreader: 
            j = 0
            for effect in row:            
                curr_dox = doxycycline_concentrations[i]
                curr_fluc = fluconazole_concentrations[j]
                temp_row = [curr_dox, curr_fluc, effect]
                writer.writerow(temp_row)
                j += 1
            i +=1

            
def Synergyplotter(importfile = "import.csv"): #plotter uses your original importfile
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import csv
    # Create a dataset
    a = pd.read_csv(importfile, header=None, keep_default_na=False)
    df = a.astype(float)


    # figsize=(6, 6) control width and height
    # dpi = 600, I 
    plt.figure(figsize=(12, 6), 
               dpi = 600) 
    
    x_axis_labels = ["0","0,25",'0,5',"1","2",'4','8','16','32','64']
    y_axis_labels = rows=['400','200','100','50','25','0']


    
    p1 = sns.heatmap(df, yticklabels = y_axis_labels, xticklabels = x_axis_labels, cmap="Blues", annot=True, annot_kws={"size": 7})
    p1.set_xlabel("Drug1 (µg/mL)")
    p1.set_ylabel("Drug2(µg/mL)")
