import Hash_function as HF

class Comparar:
    def __init__(self):
        self.datos_classico=[]
        self.datos_hashing=[]
    def clasico(self, a, b):
        datos = []
        for i in range(len(a)):
            for j in range(len(b)):
                if a[i] == b[j]:
                    datos.append(b[j])
        self.datos_classico = datos
    def hashing(self,a,b):
        datos=[]
        d=HF.TablaHash()
        for i in range(len(a)):
            d.agregar(hash(a[i]), a[i])
        for i in range(len(b)):
            if d.existe(hash(b[i])):
                datos.append(b[i])
        self.datos_hashing = datos