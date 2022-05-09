from asyncio.subprocess import PIPE
from operator import length_hint
from pickle import TRUE
from re import S, T
import re
import subprocess
import sys
import csv
from textwrap import indent

def lister():
    sortie = subprocess.run("ls eleves_bis/", text=True, shell=TRUE, capture_output=TRUE).stdout.splitlines()
    return sortie

def compiler(nom_fichier):
    nom_executable = nom_fichier[0:len(nom_fichier)-2]
    compilation = subprocess.run("gcc -Wall -ansi eleves_bis/" + nom_fichier + " -o " + nom_executable, text=True,
                            capture_output=True, shell=True).stderr
    return compilation, nom_executable

def executer(nom_executable, a, b):
    a1 = str(a)
    b1 = str(b)
    ex = subprocess.run("./eleves_bis/"+ nom_executable + " " + a1 + " " + b1 , text=True, shell=TRUE, capture_output=TRUE).stdout
    return ex

def nombre_avertissements(sortie_compilation):
    nb = sortie_compilation.count("warning")
    return nb

def nombre_erreurs (sortie_compilation):
    nb = sortie_compilation.count("error")
    return nb

def compilation_ok (sortie_compilation):
    res = nombre_erreurs(sortie_compilation)
    if res == 0:
        return 1
    return 0

def test(a, b):
    test = f"La somme de {a} et {b} vaut {a + b}\n"
    return test

def nombre_tests_ok(nom_executable):
    compteur = 0
    lst = [(0,0), (1,0), (0,1), (1,1), (12,12), (12,-43), (-1,-52)]
    for x,y in lst:
        if test(x, y) == executer(nom_executable, x, y):
            compteur += 1
    return compteur

def nombre_commentaires(nom_fichier):
    sortie = subprocess.run("cat eleves_bis/" + nom_fichier, text=True, shell=TRUE, capture_output=TRUE).stdout
    nb = sortie.count("/*")
    return nb

def informations_dans_liste():
    liste = lister()
    data = []
    for elem in liste:
        if elem[-2:] == ".c":
            etudiant = []
            nom_prenom = elem[:-2].split('_')
            compilation, nom_executable = compiler(elem)
            etudiant.append(nom_prenom[0])
            etudiant.append(nom_prenom[1])
            etudiant.append(compilation_ok(compilation))
            etudiant.append(nombre_avertissements(compilation))
            etudiant.append(nombre_tests_ok(nom_executable))
            etudiant.append(nombre_commentaires(elem))
            data.append(etudiant)
    return data

def liste_dans_csv():
    data = informations_dans_liste()
    fichier = open('fichier.csv', 'w')
    objet = csv.writer(fichier)
    for elem in data:
        objet.writerow(elem)
    fichier.close()

liste_dans_csv()
