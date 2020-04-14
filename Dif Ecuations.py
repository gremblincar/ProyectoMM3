from sympy.interactive import printing
printing.init_printing(use_latex = True)
from sympy import*
import sympy as sp
import math
import itertools

def isOperator(char):
    return (char == '+' or 
            char == '-' or 
            char == "*" or
            char == '/')

def define_x_sintaxis(function, index):
    conversion = ""
    
    while(index != len(function)):
        
        if function[index].isdigit() and function[index + 1] == 'x': #Si el valor es 2x, la expresión final la convierte a 2 * ...
            conversion += function[index] + '*'
            index += 1
            continue
            
        elif (function[index] == '^'): #Agrega las potencias
            conversion += '**'
            index +=1
            continue
        
        elif (function[index] == 'e'):
            conversion += " math.e "
            index += 1
            continue
        
        conversion += function[index]
        index += 1
        
    return conversion

def define_y_sintaxis(function):
    conversion = "Eq("
    
    for index, char in zip(itertools.count(), function):
        
        firstTime = True # f.diff a la conversion para ejecutarse más adelante. Sólo agrega este mensaje si es la primera vez
        thereAreDigits = False
        
        if ord(char) == 39 or ord(char) == 32: #Si son apostrofes o espacios los descarta, los apostrofes se checan a parte
            continue
        
        elif char == 'y':
            
            counter = index - 1
            respawn = ""
            
            thereAreDigits = function[counter].isdigit() 
            while thereAreDigits and counter > 0: #Ciclo que revisa los números anteriores a la y
                respawn += function[counter]
                
                counter -= 1
                thereAreDigits = function[counter].isdigit()
                
            if(len(respawn) != 0):
                respawn = ''.join(reversed(respawn)) #Invierte cadena que contiene los números
                conversion += respawn + '*'
                
            counter = index + 1
            
            if ord(function[counter]) == 39: #Si es un apostrofe
                while ord(function[counter]) == 39:

                    if firstTime: #Solo agrega mensaje en primer ocasion
                        conversion += "f.diff("
                        firstTime = False

                    conversion += 'x' #Agrega las equis que van dentro de los parentesis, por ejemplo f.diff(x, x, ..., x)

                    if ord(function[counter + 1]) == 39: #Agrega las comas en f.diff(x, x, ..., x)
                        conversion += ','

                    counter += 1

                conversion += ')' #Cierra el paréntesis en f.diff(x, x, ..., x)
            
            else: #En caso de que sea sólo una y, la agrega a la expresión y con la coma se marca el igual
                conversion += 'f,'
                
                counter = index
                while function[counter] != '=': #Sólo recorre hasta el encontrar el igual en la expresión dada para no recorrerlo nuevamente
                    counter += 1
                return conversion, counter
                 
        elif isOperator(char): #Agrega signos directo a la expresión
            conversion += char
            
        elif char == 'e': #Si se ingresa un euler, lo agrega a la expresión a evaluar
            conversion += " math.e "

def exec_code(conversion): #exec permite utilizar un string como código
    
    LOC = ("""
    \nx = sp.symbols('x')
    \nf = sp.Function('f')(x)
    
    \ndiffeq = """ + conversion + 
    """\ndisplay(diffeq)
    
    \ndisplay(dsolve(diffeq, f))""")
    
    exec(LOC)

def main():
    
    function = "y'' + 2y' + 4y = 5x^4 + 3x^2 - x"
    
    """print("Ingresa la función: ")
    function = str(input())"""
    
    conversion, index = define_y_sintaxis(function)
    conversion += define_x_sintaxis(function, index + 1) + ')'
    
    exec_code(conversion)

main()
