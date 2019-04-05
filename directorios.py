import os
class Directorio:
    def __init__(self):
        self.folders=[]
        self.existing=[]
        self.files=[]
        self.subfolders=[]
    def find_folders(self,address=os.getcwd()):
        dir,subdir,archivos=next(os.walk(address))
        data = []
        for folder in subdir:
            # if os.path.splitext(file)[1]=='.lyr' and file!='World Topographic Map.lyr' and file!='NODOS.lyr':
            if folder != 'mapa':
                data.append(folder)
        self.existing=subdir
        self.folders = data
        self.subfolders=dir
    def extract_data(self,address_):
        #for address_ in self.floders:
        #os.path.dirname(os.path.abspath(__file__)) +
        dir, subdir, archivos = next(os.walk(address_))
        self.files=archivos