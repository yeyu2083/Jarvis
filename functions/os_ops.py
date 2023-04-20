import os
import subprocess as sp

paths = {

    'notepad': "C://Program Files//Notepad++//notepad++.exe",
    'discord': "C:/Users/g-jk/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Discord Inc",
    'calculator': "C://Windows//System32//calc.exe"
}
#funcion para camara
def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)
#funcion para block de notas
def open_notepad():
    os.startfile(paths['notepad'])

#funcion para discord
def open_discord():
    os.startfile(paths['discord'])
#funcion para comandos
def open_cmd():
    os.system('start cmd')

#funcion para calculadora
def open_calculator():
    sp.Popen(paths['calculator'])