#!/usr/bin/env python
#-*- coding: utf-8 -*-
import arcpy
import os
import directorios as DR

salida_Layer = "salida_Layer"
datum = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                       PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],\
                       VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                       PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];\
                       -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
                       0.001;0.001;IsHighPrecision"

sr = arcpy.SpatialReference()
sr.loadFromString(datum)
#arcpy.env.qualifiedFiledNames = False

def ejecutar(path_1,ATRIBUTO,V_ATRIBUTO,Data_set):
    path = path_1 + "/temp"
    conversion_dbf = path + "\\temporal.dbf"
    arcpy.env.workspace = path
    arcpy.env.overwriteOutput = True



    V_ATRIBUTO_NAME=""
    for letra in V_ATRIBUTO:
        if letra=="." or letra=="." or letra=="-" or letra==" " or letra=="&" or letra=="/" or letra==";" or letra=="\xc2\xbf" or letra=="," :
            print("NO ASCII")
        else:
            V_ATRIBUTO_NAME=V_ATRIBUTO_NAME+letra

    def robust_decode(bs):
        '''Takes a byte string as param and convert it into a unicode one.
    First tries UTF8, and fallback to Latin1 if it fails'''
        cr = None
        try:
            cr = bs.decode('utf8')
        except UnicodeDecodeError:
            cr = bs.decode('latin1')
        return cr
    #f = open(path+"\\address.txt", "w")
    #f.write(V_ATRIBUTO.encode('utf8'))
    #f.close()

    def listdir_recurd(files_list, root, folder, checked_folders, ruta_actual, destino):
        dest = destino
        if (folder != root):
            checked_folders.append(folder)
        for f in os.listdir(folder):
            d = os.path.join(folder, f)
            if os.path.isdir(d) and d not in checked_folders:
                if os.path.join(folder, f) == os.path.join(folder, dest):
                    ruta_actual.append(os.path.join(folder, f))
                    #print os.path.join(folder, dest)
                listdir_recurd(files_list, root, d, checked_folders, ruta_actual, dest)
        return ruta_actual
    direct = DR.Directorio()
    #path = path_1+"\\data"
    #f = open(path+"\\address.txt")

    if Data_set=="Filtrada":
        try:
            #path_file = path_1 + "\\data\\" + V_ATRIBUTO_NAME
            f=open(path+"\\address.txt")
            address = listdir_recurd([], path_1+"\\data", path_1+"\\data", [], [], f.read())
            adds=sorted(address)
            #address = listdir_recurd([], path + "\\data", path + "\\data", [], [], f.read().encode('utf8'))
            #adds = sorted(address)
            f.close()
            concatenar = open(path + "\\name.txt")
            concatenar.close()
            #print(adds)
            path_file = adds[0] + "\\" + V_ATRIBUTO_NAME
            f = open(path + "\\address.txt", "w")
            f.write(V_ATRIBUTO_NAME)
            f.close()

            f = open(path + "\\name.txt", "r")
            acutales=f.read()
            f.close()
            f = open(path + "\\name.txt", "w")
            f.write(acutales+"_"+V_ATRIBUTO_NAME)
            f.close()

            gds="no problem 1"
        except Exception as e:
            gds=e
            path_file = path_1 + "\\data\\" + robust_decode(V_ATRIBUTO_NAME)
            f = open(path + "\\address.txt", "w")
            f.write(V_ATRIBUTO_NAME.encode('utf8'))
            f.close()
            f = open(path + "\\name.txt", "w")
            f.write(V_ATRIBUTO_NAME.encode('utf8'))
            f.close()
    else:
        print(V_ATRIBUTO_NAME)
        path_file=path_1 + "\\data\\" + V_ATRIBUTO_NAME
        #print V_ATRIBUTO_NAME
        f = open(path + "\\address.txt", "w")
        f.write(V_ATRIBUTO_NAME.encode('utf8'))
        f.close()
        f = open(path + "\\name.txt", "w")
        f.write(V_ATRIBUTO_NAME.encode('utf8'))
        f.close()
        gds="no problem 2"

    try:
        if Data_set=="Filtrada":

            try:
                arcpy.TableToTable_conversion(path+"\\salida.dbf", path, "temporal")
            except Exception as e:
                arcpy.TableToTable_conversion(path + "\\conversion.dbf", path, "temporal")
        else:
            arcpy.TableToTable_conversion(path+"\\conversion.dbf", path, "temporal")
    except Exception as e:
        if arcpy.Exists(path + "\\temporal.dbf"):
           arcpy.Delete_management(path + "\\temporal.dbf")
           if Data_set == "Filtrada":
               try:
                   arcpy.TableToTable_conversion(path + "\\salida.dbf", path, "temporal")
               except Exception as e:
                   arcpy.TableToTable_conversion(path + "\\conversion.dbf", path, "temporal")
           else:
               arcpy.TableToTable_conversion(path + "\\conversion.dbf", path, "temporal")
        else:
            raise e

    try:
        #shutil.rmtree(path_file,True)
        os.mkdir(path_file, 0755)
        print(path_file)
    except Exception as e:
        print("No data")
        #os.mkdir(path_file, 0755)



    expresion = arcpy.AddFieldDelimiters(arcpy.env.workspace, ATRIBUTO) + "=" + "'"+V_ATRIBUTO+"'"
    arcpy.TableToTable_conversion(conversion_dbf, path, "salida",expresion)
    arcpy.MakeXYEventLayer_management("salida.dbf", "LAT_N", "LONG_N", salida_Layer, sr)


    arcpy.env.workspace = path_file
    arcpy.env.overwriteOutput=True

    f = open(path + "\\name.txt", "r")
    V_ATRIBUTO_NAME_CONCAT = f.read()
    f.close()


    expresion = arcpy.AddFieldDelimiters(arcpy.env.workspace, ATRIBUTO) + "=" + "'"+V_ATRIBUTO +"'"
    arcpy.TableToTable_conversion(conversion_dbf, path_file, V_ATRIBUTO_NAME_CONCAT,expresion)
    arcpy.TableToTable_conversion(path+"/salida.dbf", path_file, V_ATRIBUTO_NAME_CONCAT)

    TABLE = V_ATRIBUTO_NAME_CONCAT + ".dbf"

    arcpy.MakeXYEventLayer_management(TABLE, "LONG_N", "LAT_N", V_ATRIBUTO_NAME_CONCAT+"_CAPA DE NODOS_", sr)
    arcpy.SaveToLayerFile_management(V_ATRIBUTO_NAME_CONCAT+"_CAPA DE NODOS_", V_ATRIBUTO_NAME_CONCAT+"_CAPA DE NODOS_")


    arcpy.XYToLine_management(TABLE,"Enlaces", "LONG_A", "LAT_A", "LONG_B",
                              "LAT_B", "GEODESIC")

    arcpy.MakeFeatureLayer_management("Enlaces.shp",
                                      V_ATRIBUTO_NAME_CONCAT + "_ENLACES")
    arcpy.SaveToLayerFile_management(V_ATRIBUTO_NAME_CONCAT + "_ENLACES",
                                     V_ATRIBUTO_NAME_CONCAT + "_ENLACES")
    arcpy.AddJoin_management(V_ATRIBUTO_NAME_CONCAT + "_ENLACES.lyr", "FID",TABLE, "OID")

    arcpy.MakeXYEventLayer_management(TABLE, "LONG_A", "LAT_A",
                                      V_ATRIBUTO_NAME_CONCAT + "_NODOS ESTACION A", sr)
    arcpy.MakeXYEventLayer_management(TABLE, "LONG_B", "LAT_B",
                                      V_ATRIBUTO_NAME_CONCAT + "_NODOS ESTACION B", sr)
    arcpy.SaveToLayerFile_management(V_ATRIBUTO_NAME_CONCAT + "_NODOS ESTACION A",
                                     V_ATRIBUTO_NAME_CONCAT + "_NODOS ESTACION A")
    arcpy.SaveToLayerFile_management(V_ATRIBUTO_NAME_CONCAT + "_NODOS ESTACION B",
                                      V_ATRIBUTO_NAME_CONCAT + "_NODOS ESTACION B")

    return gds
def selection(ATRIBUTO,V_ATRIBUTO,Data_set):
    V_ATRIBUTO_NAME1 = ""
    for letra in V_ATRIBUTO:
        if letra == ".":
            print("NO ASCII")
        else:
            V_ATRIBUTO_NAME1 = V_ATRIBUTO_NAME1 + letra

    V_ATRIBUTO_NAMEk = ""
    for letra in V_ATRIBUTO_NAME1:
        if letra == "-":
            print("NO ASCII")
        else:
            V_ATRIBUTO_NAMEk = V_ATRIBUTO_NAMEk + letra

    V_ATRIBUTO_NAME = ""
    for letra in V_ATRIBUTO_NAMEk:
        if letra == "&":
            print("NO ASCII")
        else:
            V_ATRIBUTO_NAME = V_ATRIBUTO_NAME + letra
    path=os.path.dirname(os.path.abspath(__file__)) + "\\temp"
    path_file = os.path.dirname(os.path.abspath(__file__)) + "\\data"

    arcpy.env.workspace = path
    arcpy.env.overwriteOutput = True

    arcpy.XYToLine_management(path_file + "\\" + V_ATRIBUTO_NAME + "\\" + "C.dbf",
                              path_file + "\\" + V_ATRIBUTO_NAME + "\\Enlaces_1", "LongitudA", "LatitudA", "LongitudB",
                              "LatitudB", "GEODESIC")

    arcpy.MakeFeatureLayer_management(path_file + "\\" + V_ATRIBUTO_NAME + "\\Enlaces_1.shp",
                                     path_file + "\\" + V_ATRIBUTO_NAME + "\\" + V_ATRIBUTO_NAME + "E")

    #arcpy.MakeFeatureLayer_management(path_file + "\\Enlaces_1.shp",V_ATRIBUTO_NAME+"E")
    arcpy.SaveToLayerFile_management(path_file + "\\" +V_ATRIBUTO_NAME + "\\" +V_ATRIBUTO_NAME+"E", path_file+"\\"+V_ATRIBUTO_NAME + "\\"+V_ATRIBUTO_NAME+"E")
    #arcpy.AddJoin_management(path_file+"\\"+V_ATRIBUTO_NAME + "\\"+V_ATRIBUTO_NAME+"E.lyr", "FID", path + "\\salida_1.dbf", "OID")
    arcpy.AddJoin_management(path_file + "\\" + V_ATRIBUTO_NAME + "\\" + V_ATRIBUTO_NAME + "E.lyr", "FID",
                             path_file + "\\" + V_ATRIBUTO_NAME + "C.dbf", "OID")
    #arcpy.PackageLayer_management(path_file +"\\"+V_ATRIBUTO_NAME+ "\\"+V_ATRIBUTO_NAME+"E.lyr", path_file+ "\\"+V_ATRIBUTO_NAME+"\\"+V_ATRIBUTO_NAME +"E" )


    datum = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                           PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],\
                           VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                           PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];\
                           -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
                           0.001;0.001;IsHighPrecision"

    sr = arcpy.SpatialReference()
    sr.loadFromString(datum)
    TABLE=path_file + "\\" + V_ATRIBUTO_NAME + "\\" + "C.dbf"
    arcpy.MakeXYEventLayer_management(TABLE, "LongitudA", "LatitudA", path_file+"\\"+V_ATRIBUTO_NAME+"\\"+V_ATRIBUTO_NAME + "EA", sr)
    arcpy.MakeXYEventLayer_management(TABLE, "LongitudB", "LatitudB", path_file+"\\"+V_ATRIBUTO_NAME+"\\"+V_ATRIBUTO_NAME+"EB", sr)
    arcpy.SaveToLayerFile_management(path_file + "\\" + V_ATRIBUTO_NAME + "\\" +V_ATRIBUTO_NAME+"EA", path_file+"\\"+V_ATRIBUTO_NAME+"\\"+V_ATRIBUTO_NAME+"EA")
    arcpy.SaveToLayerFile_management(path_file + "\\" + V_ATRIBUTO_NAME + "\\" +V_ATRIBUTO_NAME+"EB", path_file+"\\"+V_ATRIBUTO_NAME+"\\"+V_ATRIBUTO_NAME+"EB")

if __name__ == '__main__':
    #selection()
    path = os.path.dirname(os.path.abspath(__file__))
    ejecutar(path,"BANDA_OPER","5250 MHZ ¿ 5350 MHZ","Original")

    print('ejecutado')