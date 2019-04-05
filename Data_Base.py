#-*- coding: utf-8 -*-
import arcpy
import os
import pandas  as pd
import numpy as np

conversion = "conversion"
conversion_dbf="conversion.dbf"
salida_dbf="salida.dbf"
datum = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                       PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],\
                       VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                       PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];\
                       -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
                       0.001;0.001;IsHighPrecision"
sr = arcpy.SpatialReference()
sr.loadFromString(datum)
#arcpy.env.qualifiedFiledNames = False

def Iniciar_valor():
    path=os.path.dirname(os.path.abspath(__file__))
    path_temp=path+"\\temp"
    arcpy.env.workspace = path + "/temp"
    arcpy.env.overwriteOutput = True
    #arcpy.env.qualifiedFiledNames=False

    #Datos_xls = "\Archivos Base de Datos\ENLACES.xls"
    arcpy.env.workspace = path+"/temp"

    if arcpy.Exists(path+"\\temp\\conversion.dbf"):
        arcpy.Delete_management(path+"\\tempo\\conversion.dbf")
    if arcpy.Exists(path+"\\temp\\conversion_1.dbf"):
        arcpy.Delete_management(path+"\\tempo\\conversion_1.dbf")
    if arcpy.Exists(path+"\\temp\\conversion_12.dbf"):
        arcpy.Delete_management(path+"\\tempo\\conversion_12.dbf")
    if arcpy.Exists(path+"\\temp\\salida.dbf"):
        arcpy.Delete_management(path+"\\tempo\\salida.dbf")
    if arcpy.Exists(path + "\\temp\\salida_1.dbf"):
        arcpy.Delete_management(path + "\\tempo\\salida_1.dbf")

    arcpy.Field.length=254

    #arcpy.ExcelToTable_conversion(path + Datos_xls, "conversion11")
    arcpy.TableToTable_conversion(path_temp+"\\table.dbf", path + "/temp", conversion)

    arcpy.TableToTable_conversion(path_temp+"\\table.dbf", path + "/temp", "salida")

    arcpy.AddField_management(salida_dbf, "LAT_N", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(salida_dbf, "LONG_N", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(salida_dbf, "LAT_A", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(salida_dbf, "LONG_A", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(salida_dbf, "LAT_B", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(salida_dbf, "LONG_B", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.AddField_management(conversion_dbf, "LAT_N", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(conversion_dbf, "LONG_N", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(conversion_dbf, "LAT_A", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(conversion_dbf, "LONG_A", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(conversion_dbf, "LAT_B", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(conversion_dbf, "LONG_B", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    expression = "parse_dms(!Latitud!)"
    expression1 = "parse_dms(!Longitud!)"
    expression2 = "parse_dms(!LATITUD_A!)"
    expression3 = "parse_dms(!LONGITUD_A!)"
    expression4 = "parse_dms(!LATITUD_B!)"
    expression5 = "parse_dms(!LONGITUD_B!)"
    codeblock = """def parse_dms(dms):
                import re
                try:
                    parts=re.split('[^\d\w\.]+',dms.encode('utf8').replace(",","."))
                    dd=float(parts[0])+float(parts[1])/60.0+float(parts[2])/(3600.0);
                    #print(parts[0]+","+","+parts[1]+","+parts[2]+","+parts[3])
                    if parts[3]=='W' or parts[3]=='S':
                        dd*=-1
                    return dd
                except Exception as e:
                    return 0"""

    arcpy.CalculateField_management(salida_dbf, "LAT_N", expression, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(salida_dbf, "LONG_N", expression1, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(salida_dbf, "LAT_A", expression2, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(salida_dbf, "LONG_A", expression3, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(salida_dbf, "LAT_B", expression4, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(salida_dbf, "LONG_B", expression5, "PYTHON_9.3", codeblock)

    arcpy.CalculateField_management(conversion_dbf, "LAT_N", expression, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(conversion_dbf, "LONG_N", expression1, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(conversion_dbf, "LAT_A", expression2, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(conversion_dbf, "LONG_A", expression3, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(conversion_dbf, "LAT_B", expression4, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management(conversion_dbf, "LONG_B", expression5, "PYTHON_9.3", codeblock)

def leer_excel(path_1):
    path_file=path_1+"\\Archivos Base de Datos"
    path_temp=path_1+"\\temp"

    dfA = pd.read_excel(path_file+'\\REGISTRO SAI OTH-ATH.xlsx', sheetname='REGISTRO SAI', header=None, skiprows=4, )
    dfB = pd.read_excel(path_file+'\\MDBA-SAI.xlsx', sheetname='MDBA', header=None)

    arcpy.env.workspace = path_temp

    dfA.columns = dfA.iloc[0, :]
    dfB.columns = dfB.iloc[0, :]
    dfA_data = dfA.drop(0)
    dfB_data = dfB.drop(0)

    Fiel_SAI = [2, 40, 41, 42, 43, 44, 45, 46]
    Fiel_SAIX = [2, 64, 65, 66, 67, 68]

    ENLACES_AB = ['LATITUD_A', 'LONGITUD_A', 'LATITUD_B', 'LONGITUD_B',
                  'PROVINCIA_A', 'PROVINCIA_B', 'CANTON_A', 'CANTON_B', 'PERMISIONARIO']

    InfoSAI = dfA_data.iloc[:, Fiel_SAI]
    InfoSAIX = dfA_data.iloc[:, Fiel_SAIX]

    CANTON = pd.DataFrame(InfoSAI.loc[:, 'CANTON / CIUDAD'])
    CANTON.index = range(len(CANTON))
    PROVINCIA = pd.DataFrame(InfoSAI.PROVINCIA)
    PROVINCIA.index = range(len(PROVINCIA))

    InfoSAI.index = InfoSAI.PERMISIONARIO
    Grados = dfA_data.G
    Minutos = dfA_data.M
    Segundos = dfA_data.S
    N_S = dfA_data.iloc[:]['N/S']
    E_O = dfA_data.iloc[:]['E/O']

    Grados.columns = ['EstacionA', 'EstacionB']
    Minutos.columns = ['EstacionA', 'EstacionB']
    Segundos.columns = ['EstacionA', 'EstacionB']

    Latitud = []
    Longitud = []

    gsim = '\xb0'
    msim = "'"
    ssim = '"'

    for x in range(len(Grados)):
        x = x + 1
        G = str(Grados.EstacionA[x])
        M = str(Minutos.EstacionA[x])
        S = str(Segundos.EstacionA[x])
        GL = str(Grados.EstacionB[x])
        ML = str(Minutos.EstacionB[x])

        SL = str(Segundos.EstacionB[x])
        P1 = str(N_S[x])
        P2 = str(E_O[x])
        if P2 == 'O':
            P2 = 'W'
        else:
            P2 = 'E'

        Lat = G + gsim + M + msim + S + ssim + P1
        Lon = GL + gsim + ML + msim + SL + ssim + P2
        Lat = Lat.decode('unicode-escape')
        Lon = Lon.decode('unicode-escape')

        if G == 'nan':
            Lat = None
            Lon = None

        Latitud.append(Lat)
        Longitud.append(Lon)

    Latitud = pd.DataFrame(Latitud)
    Longitud = pd.DataFrame(Longitud)
    Latitud.columns = ['Latitud']
    Longitud.columns = ['Longitud']

    Coordenadas = Latitud.join(Longitud)
    InfoSAI.index = range(len(InfoSAI))
    InfoSAI = InfoSAI.join(Coordenadas)
    InfoSAI = InfoSAI.drop('CODIGO', axis=1)
    InfoSAI = InfoSAI.dropna(subset=['Latitud'])
    InfoSAI = InfoSAI.rename(columns={'CANTON / CIUDAD': 'CANTON'})

    Enlaces = dfA_data.CODIGO
    Enlaces.columns = ['Codigo', 'EstacionA', 'EstacionB']
    EnlacesD = Enlaces
    EnlacesD.index = InfoSAIX.PERMISIONARIO
    EnlacesD = Enlaces.dropna(subset=['EstacionA'])

    EnlacesY = Enlaces.drop(['EstacionA', 'EstacionB'], axis=1)
    EnlacesY.index = range(len(EnlacesY))
    EnlacesY = EnlacesY.join(Coordenadas)
    EnlacesY = EnlacesY.join(CANTON)
    EnlacesY = EnlacesY.join(PROVINCIA)
    EnlacesY.index = InfoSAIX.PERMISIONARIO

    EnlacesX = Enlaces.drop(['EstacionA', 'EstacionB'], axis=1)
    EnlacesX = EnlacesX.join(Coordenadas)
    EnlacesX = EnlacesX.join(CANTON)
    EnlacesX = EnlacesX.join(PROVINCIA)
    EnlacesX.index = InfoSAIX.PERMISIONARIO

    List02 = EnlacesD.index
    List02 = List02.drop_duplicates()

    Estacion_A = pd.DataFrame()
    Estacion_B = pd.DataFrame()

    for a in List02:

        Permi = pd.DataFrame(EnlacesD.loc[a])
        Location = EnlacesY.loc[a]
        Location.index = Location.Codigo

        try:
            v = len(Permi.Codigo)
        except Exception as e:
            Permi = Permi.T
            v = 1

        for b in range(v):
            Aux = Permi.iloc[b]
            S_A = Aux['EstacionA']
            S_B = Aux['EstacionB']

            Estacion_A = Estacion_A.append(pd.DataFrame(Location.loc[S_A]).T)
            Estacion_B = Estacion_B.append(pd.DataFrame(Location.loc[S_B]).T)

    Estacion_A = Estacion_A.drop(['Codigo'], axis=1)
    Estacion_A.index = range(len(Estacion_A))
    Estacion_A.columns = ['LATITUD_A', 'LONGITUD_A', 'CANTON_A', 'PROVINCIA_A']

    Estacion_B = Estacion_B.drop(['Codigo'], axis=1)
    Estacion_B.index = range(len(Estacion_B))
    Estacion_B.columns = ['LATITUD_B', 'LONGITUD_B', 'CANTON_B', 'PROVINCIA_B']

    EnlacesD.index = range(len(EnlacesD))

    InfoSAIX.index = range(len(InfoSAIX))
    Aux1 = pd.DataFrame(Enlaces.EstacionA)
    Aux1.index = range(len(Aux1))
    InfoSAIX = InfoSAIX.join(Aux1)
    InfoSAIX = InfoSAIX.dropna(subset=['EstacionA'])
    InfoSAIX = InfoSAIX.drop(['EstacionA'], axis=1)
    InfoSAIX.index = range(len(InfoSAIX))
    ENLACES_SAI = Estacion_A.join(Estacion_B)
    ENLACES_SAI = ENLACES_SAI.join(InfoSAIX)
    ENLACES_SAI.index = ENLACES_SAI.PERMISIONARIO
    Col = ENLACES_SAI.columns

    for i in Col:
        ENLACES_SAI.iloc[:][i] = map(lambda x: unicode(x).upper(), ENLACES_SAI.iloc[:][i])

    dfB_data.index = dfB_data['NOMBRES']
    Link_Data = dfB_data.loc[dfB_data.index.isin(List02)]
    Link_Data = Link_Data.rename(columns={'NOMBRES': 'PERMISIONARIO'})
    List03 = Link_Data.index
    List03 = List03.drop_duplicates()
    EnlacesSAI = pd.DataFrame()

    for i in List03:
        X = ENLACES_SAI.loc[i]
        Y = Link_Data.loc[i]
        En = pd.merge(X, Y, on=ENLACES_AB, how='outer')
        EnlacesSAI = EnlacesSAI.append(En, ignore_index=True, verify_integrity=False)

    EnlacesSAI.index = EnlacesSAI.PERMISIONARIO

    ENLACES_SAI = ENLACES_SAI.drop(List03)

    All_Links = ENLACES_SAI.append(EnlacesSAI)
    All_Links.index = All_Links.PERMISIONARIO

    List03 = All_Links.PERMISIONARIO
    List03 = List03.drop_duplicates()
    Link_Data1 = pd.DataFrame()

    for i in List03:

        Datos = pd.DataFrame(All_Links.loc[i])

        try:
            v = len(Datos.PERMISIONARIO)
        except Exception as e:
            Datos = Datos.T
            v = 1

        for j in range(v):
            Can = pd.DataFrame(Datos.iloc[j])
            Can = Can.T
            A = Can.CANTON_A
            B = Can.CANTON_B
            A1 = Can.PROVINCIA_A
            B1 = Can.PROVINCIA_B
            C = pd.DataFrame(A.append(B))
            C.columns = [u'CANTON']

            C1 = pd.DataFrame(A1.append(B1))
            C1.columns = [u'PROVINCIA']

            Canton = Can.append(Can, ignore_index=False, verify_integrity=False)
            Canton = pd.concat([Canton, C, C1], axis=1, join='inner')
            Canton = Canton.drop_duplicates(subset=['CANTON'])
            Canton = Canton.drop_duplicates(subset=['PROVINCIA'])
            Link_Data1 = Link_Data1.append(Canton)

    Link_Data1 = Link_Data1.drop(['CANTON_A', 'CANTON_B', 'PROVINCIA_A', 'PROVINCIA_B'], axis=1)

    DataTable = InfoSAI.append(Link_Data1, ignore_index=True)
    Col = DataTable.columns

    for i in Col:
        DataTable.iloc[:][i] = map(lambda x: unicode(x).upper(), DataTable.iloc[:][i])

    num = np.array(np.rec.fromrecords(DataTable.values))
    names = DataTable.dtypes.index.tolist()
    names = [x.encode('UTF8') for x in names]
    num.dtype.names = tuple(names)

    #arcpy.env.workspace = r'C:\Users\USUARIO\Desktop\DataBase'
    #path = arcpy.env.workspace

    # arcpy.CreateFileGDB_management(path,'GeoDataBase.gdb')

    #arcpy.da.NumPyArrayToTable(num, 'GeoDataBase.gdb/MyTable8')

    #arcpy.CreateFileGDB_management(path,'GeoDataBase.gdb')
    #arcpy.da.NumPyArrayToTable(num, 'GeoDataBase.gdb/MyTable4')
    if arcpy.Exists("C:\Users\EstChristianRafaelMa\Documents\ArcGIS\Default.gdb\\tabla"):
        arcpy.Delete_management("C:\Users\EstChristianRafaelMa\Documents\ArcGIS\Default.gdb\\tabla")
    arcpy.da.NumPyArrayToTable(num, "C:\Users\EstChristianRafaelMa\Documents\ArcGIS\Default.gdb\\tabla")
    arcpy.TableToTable_conversion("C:\Users\EstChristianRafaelMa\Documents\ArcGIS\Default.gdb\\tabla", path_temp, "table")

def ejecutar(path_1):

    path=path_1+"/temp"
    path_file=path_1+"\\data"
    arcpy.env.workspace = path
    arcpy.env.overwriteOutput=True
    arcpy.MakeXYEventLayer_management(conversion_dbf, "LONG_N", "LAT_N","NODOS", sr)
    arcpy.SaveToLayerFile_management("NODOS", path_file+"\\NODOS")
    arcpy.PackageLayer_management(path_file+"\\NODOS.lyr",path_file+"\\NODOS")

    #arcpy.ErasePoint_edit(path_file+"\\NODOS.lyr",path_1+"\\data\\mapa\\EliminarNaN.lyr",'INSIDE')

    #arcpy.PackageLayer_management(path_file + "\\"+V_ATRIBUTO_NAME+"EB.lyr", path_file + "\\"+V_ATRIBUTO_NAME +"EB")
    arcpy.XYToLine_management(path + "\\conversion.dbf", path_file + "\\Enlaces", "LONG_A", "LAT_A",
                              "LONG_B", "LAT_B", "GEODESIC","PERMISIONA")

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    #ejecutar_MDBA(path)
    leer_excel(path)
    Iniciar_valor()
    ejecutar(path)
    print('Completado')