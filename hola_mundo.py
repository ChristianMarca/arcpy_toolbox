from time import time
from time import sleep
import os
import directorios as dr
funciona=0
def arbol(path):
    #direct.find_folders(path)
    #variable_global="no funciono"
    dir, subdir, archivos = next(os.walk(path))
    #print dir
    #print subdir
    #for i in direct.subfolders:
    for i in subdir:
        f = open("prueba.txt","r")
        if str(f.read()) == str(i):
            variable_global=path+"\\"+i
            print ("salds")
            break
        else:
        #print(path + "\\" + i)
            arbol(path+"\\"+i)
    #return variable_global
    print "as"
            #print(path+"\\"+i)
    #return variable_global\
import os
import sys
from os import listdir
from os.path import isfile, isdir, join

def listdir_recurd(files_list, root, folder, checked_folders,ruta_actual,destino):
    dest=destino
    if (folder != root):
        checked_folders.append(folder)

    for f in listdir(folder):
        d = join(folder, f)
        if isdir(d) and d not in checked_folders:
            if join(folder, f)==join(folder,destino):
                ruta_actual.append(join(folder, f))
                print join(folder, destino)
            listdir_recurd(files_list, root, d, checked_folders,ruta_actual,dest)
    return ruta_actual

if __name__ == '__main__':
    #var = time()

    #f = open("prueba.txt")
    #print (f.readline())
    #f.close()

    f = open("prueba.txt", "w")
    a ="@cvxcnst"
    f.write(a)
    f.close()

    #f = open("prueba.txt")
    #print (f.readline())
    #f.close()
    #sleep(1)
    #print(time() - var)

    direct = dr.Directorio()
    path = "C:\Users\EstChristianRafaelMa\Desktop\Varios\\"
    f = open("prueba.txt")
    #print f.readline()
    #pathom=arbol(path)
    #print (pathom)
    filez = listdir_recurd([], path, path, [],[],f.read())  # esto lista todos los archivos
    print(sorted(filez))
    #C:\Users\EstChristianRafaelMa\Desktop\Varios\\MATLAB\cvx\builtins\@cvxcnst

    #listaarchivos = []
    #for (direci, subdir, archivos) in os.walk(path):
    #    listaarchivos.extend(subdir)
        #if str(f.read()) == str(i):
        #    break
        #print subdir
    #print listaarchivos
    #    print subdir