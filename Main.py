from AnalizadorLexico import AnalizadorLexico
from AnalizadorSintactico import AnalizadorSintactico
from tkinter import *
import tkinter as t
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

tokens = []
total_rows = 0
total_columns = 0

def menu():
    print("*********************************")
    print("*         Menú Principal        *")
    print("*********************************")
    print("* 1) Cargar archivo             *")
    print("* 2) Analizador Léxico          *")
    print("* 3) Analizador Sintáctico      *")
    print("* 4) -----                      *")
    print("* 5) Salir                      *")
    print("*********************************")

def graphicBrowser():
    win = Tk()
    win.geometry("1x1")
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select a File", filetypes=(("Lfp files", "*.lfp*"), ("All files", "*.*")))
    win.destroy()
    return filename

def read(path):
    try:
        with open(path, 'r') as f:
            format = path.find(".lfp")
            if format:
                alltext = f.readlines()
                print("\n")
                print("Carga de datos realizada correctamente")
                print("\n")
                return alltext

            else:
                print("\n")
                print("Formato de carga no coincide con .lfp, intentalo de nuevo")
                print("\n")
    except:
        print("\n")
        print("Ha ocurrido un error, intentalo de nuevo")
        print("\n")

Ejecucion = True
while Ejecucion:
    
    menu()
    opcion = input("Elige una opción: ")

    if opcion == "1":
        #name = graphicBrowser()
        name = "C:/Users/alexi/Downloads/prueba.lfp"
        returned = read(name)

    elif opcion == "2":
        analized = AnalizadorLexico(returned)
        
    elif opcion == "3":
        tokens = analized.getTokens()
        AnalizadorSintactico(tokens)
    
    elif opcion == "5":
        print("Has salido del programa")
        Ejecucion = False

    else:
        print("Intenta de nuevo")