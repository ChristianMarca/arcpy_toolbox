#!/usr/bin/env python
import arcpy
import os
#__name__

def Iniciar_valor():
    path=os.path.dirname(os.path.abspath(__file__))
    path_temp=path+"\\temp"
    arcpy.env.overwriteOutput = True
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

    conversion = "conversion_1"
    #arcpy.ExcelToTable_conversion(path+Datos_xls, "conversion11_1")
    arcpy.TableToTable_conversion("table.dbf",path+"/temp",conversion)
    arcpy.TableToTable_conversion("table.dbf", path+"/temp", "salida_1")
    #Datos_xls = "\Archivos Base de Datos\DATA_PRUEBA.xls"
    #Datos_xls1 = "\Archivos Base de Datos\ENLACES.xls"
    arcpy.env.workspace = path + "/temp"
    conversion = "conversion"

    #arcpy.ExcelToTable_conversion(path + Datos_xls, "conversion11")
    arcpy.TableToTable_conversion(path_temp+"\\table.dbf", path + "/temp", conversion)
    arcpy.TableToTable_conversion(path_temp+"\\table.dbf", path + "/temp", "salida")
    arcpy.AddField_management("salida.dbf", "LATITUD_GD", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management("salida.dbf", "LONGITUD_GD", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    expression = "parse_dms(!Latitud!)"
    expression1 = "parse_dms(!Longitud!)"
    codeblock = """def parse_dms(dms):
                import re
                try:
                    parts=re.split('[^\d\w\.]+',dms.encode('utf8'))
                    dd=float(parts[0])+float(parts[1])/60.0+float(parts[2])/(3600.0);
                    #print(parts[0]+","+","+parts[1]+","+parts[2]+","+parts[3])
                    if parts[3]=='W' or parts[3]=='S':
                        dd*=-1
                    return dd
                except Exception as e:
                    return 0"""

    arcpy.CalculateField_management("salida.dbf", "LATITUD_GD", expression, "PYTHON_9.3", codeblock)
    arcpy.CalculateField_management("salida.dbf", "LONGITUD_GD", expression1, "PYTHON_9.3", codeblock)
    #arcpy.ExcelToTable_conversion(path + Datos_xls1, "conversion21","ENLACE_A")
    #arcpy.TableToTable_conversion("conversion21.dbf", path + "/temp", "conversion_12")


if __name__ == '__main__':
    Iniciar_valor()