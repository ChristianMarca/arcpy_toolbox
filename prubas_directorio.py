import directorios as dr
import os
dire=dr.Directorio()
dire.find_folders(os.path.dirname(os.path.abspath(__file__))+"\\data")
print(dire.existing)
print (dire.folders)
for folder in dire.folders:
    dire.extract_data(os.path.dirname(os.path.abspath(__file__))+"\\data\\"+folder)
    print (dire.files)
