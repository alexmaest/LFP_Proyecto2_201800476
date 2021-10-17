from AnalizadorLexico import AnalizadorLexico
from AnalizadorSintactico import AnalizadorSintactico
from tokenReport import tokenReport
from failsReport import failsReport
from treeReport import treeReport
from tkinter import *
import tkinter as t
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

tokens = []
erroresSintacticos = []
total_rows = 0
total_columns = 0
editorText = ""
consoleTextGlobal = ""

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

def browserFile():
    path = graphicBrowser()
    returned = read(path)
    global editorText
    editorText = ""
    current = ""
    returned.append("$")
    textLen = len(returned)
    for index in range(textLen):
        columnLen = len(returned[index])
        index2 = 0
        while index2 < columnLen:
            current = returned[index][index2]
            index2 += 1
            if current != "$" and index != textLen - 1:
                editorText += current

    global editorBox
    editorBox.insert(END, editorText)
    messagebox.showinfo("Información","Carga realizada correctamente")

def textConsole():
    global editorBox
    editorTempText = editorBox.get("1.0", "end-1c")
    analized = AnalizadorLexico(editorTempText)
    token = analized.getTokens()
    global tokens
    tokens = token
    analizer = AnalizadorSintactico(token)
    global erroresSintacticos
    erroresSintacticos = analizer.getErrores()
    global consoleTextGlobal
    consoleTextGlobal = analizer.getConsoleText()
    global consoleBox
    consoleBox.insert(END, consoleTextGlobal)

def nameReport():
    name = str(reportName.get())
    lowerName = name.lower()
    global tokens
    global erroresSintacticos
    if lowerName == "tokens":
        tokenReport(tokens)
    elif lowerName == "errores":
        failsReport(tokens, erroresSintacticos)
    elif lowerName == "arbol de derivación":
        treeReport(tokens)

v = t.Tk()
v.geometry("1080x720")
v.resizable(False, False)
v.title("Analizadores")

consoleBox = Text(v, fg="#ffffff", bg ="black", height=36, width=54)
consoleBox.place(x=643, y=120)
editorBox = Text(v, fg="#ffffff", bg ="#010030", height=38, width=80)
editorBox.place(x=0, y=96)
t.Label(v, text="", width=200, height=6, bg = "#162742").place(x=0, y=0)
t.Label(v, text="ANALIZADORES", fg="#fcba03", width=15, height=3, bg = "#162742", font = "Helvetica 18 bold italic").place(x=0, y=5)
t.Button(v, text="▶", width=2, font = "Helvetica 14 bold", bg='#fcba03', command=textConsole).place(x=720, y=27)
t.Button(v, text="Cargar archivo", width=12, font = "Arial 12", command=browserFile).place(x=755, y=30)
t.Label(v, text="Reportes", width=20, fg="#fcba03", bg = "#162742", font = "Helvetica 12").place(x=871, y=17)
reportes = ["Tokens", "Errores", "Arbol de derivación"]
reportName = t.StringVar(v)
ttk.Combobox(v, textvariable=reportName, width=15, values=reportes).place(x=900, y=42)
t.Button(v, width=1, text="⟳", font = "Helvetica 10 bold", bg='#fcba03', command=nameReport).place(x=1015, y=39)
t.Label(v, text="Consola", width=50, fg="black", bg = "dark gray", font = "Helvetica 12").place(x=643, y=95)
t.Label(v, text = "   2021 - Proyecto 2 de Lenguajes formales y de programación", width=255, fg="black", bg = "#fcba03").place(x=0, y=700)

v.mainloop()

"""
Ejecucion = True
while Ejecucion:
    
    menu()
    opcion = input("Elige una opción: ")

    if opcion == "1":
        #name = graphicBrowser()
        name = "C:/Users/alexi/Downloads/entrada.lfp"
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
"""