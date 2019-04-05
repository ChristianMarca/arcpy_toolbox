import compare as cp
import Hash_function as HF
import numpy as np
import scipy as sp
a=sp.ceil(1000*sp.rand(100))
b=sp.ceil(1000*sp.rand(10000))
comp=cp.Comparar()
comp.hashing(a,b)
print(comp.datos_hashing)
print len(comp.datos_hashing)


datos=[]
d=HF.TablaHash()
for i in range(len(a)):
    d.agregar(hash(a[i]), a[i])
for i in range(len(b)):
    if d.existe(hash(b[i])):
        datos.append(b[i])
self.datos_hashing = datos
