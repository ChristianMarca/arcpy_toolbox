import arcpy
import os
from Aranque_cod import *
import prubeas as pr
import shutil

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Registro SAI"
        self.alias = "Registro SAI"

        # List of tool classes associated with this toolbox
        self.tools = [Tool,Filtros]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        #params = None

        try:
            path=os.path.dirname(os.path.abspath(__file__))+"/conversion.dbf"
        except Exception as e:
            messages.addMessage("Ejecucion Inicial")
            #Iniciar_valor()
            path=os.path.dirname(os.path.abspath(__file__))
            path=os.path.dirname(os.path.abspath(__file__))+"/conversion.dbf"

        fields = arcpy.ListFields(path)

        CAMPO=[]
        V_CAMPO=[]

        for field in fields:
            CAMPO.append(field.name)

        param0=arcpy.Parameter()
        param0.name="ATRIBUTO"
        param0.displayName="CAMPO"
        param0.parameterType="Required"
        param0.datatype="String"
        param0.value="PROVINCIA"
        param0.filter.list=CAMPO

        cursor = arcpy.da.SearchCursor(path, param0.value)
        for row in cursor:
            V_CAMPO.append(format(row[0]))


        param1=arcpy.Parameter()
        param1.name="V_ATRIBUTO"
        param1.displayName="VALOR DEL CAMPO"
        param1.parameterType="Required"
        param1.datatype="String"
        #param1.value="Azuay"
        value=sorted(set(V_CAMPO))
        param1.filter.list=value

        #return params
        return [param0,param1]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        path=os.path.dirname(os.path.abspath(__file__))+"\conversion.dbf"

        cursor = arcpy.da.SearchCursor(path, parameters[0].valueAsText)
        V_CAMPO=[]
        for row in cursor:
            V_CAMPO.append(format(row[0]))
        value=sorted(set(V_CAMPO))

        parameters[1].filter.list=value
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        #-*- conding: utf-8 -*-
        """The source code of the tool."""

        ATRIBUTO=parameters[0].valueAsText
        V_ATRIBUTO=parameters[1].valueAsText

        values=pr.prueba()

        messages.addMessage("Campo: " +ATRIBUTO)
        messages.addMessage("Valor de Campo: " +V_ATRIBUTO)
        messages.addMessage("{0} probando ".format(values))

        # Local variables:
        path=os.path.dirname(os.path.abspath(__file__))
        Datos_xls = "DATA_PRUEBA.xls"
        conversion = "conversion"
        conversion_dbf="conversion.dbf"
        #Scripts = "C:\\Users\\EstChristianRafaelMa\\Desktop\\ARGIS_PASANTIA\\Datos"

        SaveToLayerFile_lyr = path+"SaveToLayerFile.lyr"

        #Lugar de trabajo
        arcpy.env.workspace = path
        arcpy.env.overwriteOutput=True

        # Process: Excel To Table
        arcpy.ExcelToTable_conversion(Datos_xls, "conversion1")
        arcpy.TableToTable_conversion("conversion1.dbf",path,conversion)

        # Process: Add Field
        arcpy.AddField_management(conversion_dbf, "Latitud", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.AddField_management(conversion_dbf, "Longitud", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        # Calculate Parameters for New Fields
        expression = "getClass(!G!,!M!,!S!,!N_S!)"
        codeblock = """def getClass(G,M,S,N_S):
            if N_S == "S":
                return -1*(float(G)+float(float(M)/60.0)+float(float(S)/3600.0))
            else:
                return 1*(float(G)+float(float(M)/60.0)+float(float(S)/3600.0))"""

        expression1 = "getClass1(!G_1!,!M_1!,!S_1!,!E_O!)"
        codeblock1 = """def getClass1(G_1,M_1,S_1,E_O):
            if E_O == "O":
                return -1*(float(G_1)+float(float(M_1)/60.0)+float(float(S_1)/3600.0))
            else:
                return 1*(float(G_1)+float(float(M_1)/60.0)+float(float(S_1)/3600.0))"""

        arcpy.CalculateField_management("conversion.dbf","Latitud",expression, "PYTHON_9.3",codeblock)
        arcpy.CalculateField_management("conversion.dbf","Longitud",expression1, "PYTHON_9.3",codeblock1)

        #Paquete original de salida
        datum = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                           PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],\
                           VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                           PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];\
                           -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
                           0.001;0.001;IsHighPrecision"

        sr = arcpy.SpatialReference()
        sr.loadFromString(datum)
        arcpy.MakeXYEventLayer_management("conversion.dbf", "Longitud", "Latitud","original", sr)

        arcpy.SaveToLayerFile_management("original", "salida_original")
        arcpy.PackageLayer_management("salida_original.lyr","paquete_capa_original")

        # Process: Table to Table
        expresion = arcpy.AddFieldDelimiters(arcpy.env.workspace, ATRIBUTO) + "=" + "'"+V_ATRIBUTO +"'"
        arcpy.TableToTable_conversion(conversion_dbf, path, "salida",expresion)

        salida_Layer = "salida_Layer"
        #salida_Layer=V_ATRIBUTO
        #salida_Layer="TOOL"

        arcpy.MakeXYEventLayer_management("salida.dbf", "Longitud", "Latitud", salida_Layer, sr)
        saved_Layer="salidalyr"
        #saved_Layer=V_ATRIBUTO
        #saved_Layer="TOOL"

        # Process: Save To Layer File
        arcpy.SaveToLayerFile_management(salida_Layer, saved_Layer)
        #arcpy.PackageLayer_management("salidalyr.lyr","paquete_capa")

        #arcpy.RefreshActiveView()
        #arcpy.RefreshTOC()
        #arcpy.RefreshCatalog("SaveToLayerFile_lyr.lyr")
        return

class Filtros(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Filtros"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        #params = None
        path=path=os.path.dirname(os.path.abspath(__file__))+"\salida.dbf"

        fields = arcpy.ListFields(path)
        CAMPO=[]
        V_CAMPO=[]
        for field in fields:
            CAMPO.append(field.name)

        param0=arcpy.Parameter()
        param0.name="ATRIBUTO"
        param0.displayName="CAMPO"
        param0.parameterType="Required"
        param0.datatype="String"
        param0.value="PROVINCIA"
        param0.filter.list=CAMPO

        cursor = arcpy.da.SearchCursor(path, param0.value)
        for row in cursor:
            V_CAMPO.append(format(row[0]))


        param1=arcpy.Parameter()
        param1.name="V_ATRIBUTO"
        param1.displayName="VALOR DEL CAMPO"
        param1.parameterType="Required"
        param1.datatype="String"
        value=sorted(set(V_CAMPO))
        param1.filter.list=value

        param2=arcpy.Parameter()
        param2.name="Create_Shapefile"
        param2.displayName="Desea Crear ShapeFile"
        param2.parameterType="Required"
        param2.datatype="String"
        param2.value="NO"
        param2.filter.list=["NO","SI"]

        param3=arcpy.Parameter()
        param3.name="Direccion de salida"
        param3.displayName="Direccion"
        param3.parameterType="Optional"
        param3.datatype="Address Locator"
        param3.value=path

        #return params
        return [param0,param1,param2,param3]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        path=path=os.path.dirname(os.path.abspath(__file__))+"\salida.dbf"
        cursor = arcpy.da.SearchCursor(path, parameters[0].valueAsText)
        V_CAMPO=[]
        for row in cursor:
            V_CAMPO.append(format(row[0]))
        value=sorted(set(V_CAMPO))

        parameters[1].filter.list=value
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        #-*- conding: utf-8 -*-
        """The source code of the tool."""

        ATRIBUTO=parameters[0].valueAsText
        V_ATRIBUTO=parameters[1].valueAsText
        Create_Shapefile=parameters[2].valueAsText
        Address_Shapefile=parameters[3].valueAsText

        V_ATRIBUTO_NAME1=""
        for letra in V_ATRIBUTO:
            if letra==".":
                print("NO ASCII")
            else:
                V_ATRIBUTO_NAME1=V_ATRIBUTO_NAME1+letra

        V_ATRIBUTO_NAME=""
        for letra in V_ATRIBUTO_NAME1:
            if letra=="&":
                print("NO ASCII")
            else:
                V_ATRIBUTO_NAME=V_ATRIBUTO_NAME+letra


        messages.addMessage("Campo: " +ATRIBUTO)
        messages.addMessage("Valor de Campo: " +V_ATRIBUTO)

        # Local variables:
        path=os.path.dirname(os.path.abspath(__file__))
        path_file=path+"/data"

        try:
            shutil.rmtree(path_file,ignore_errors=True)
            os.mkdir(path_file,0755)
        except Exception as e:
            print("No data")
            os.mkdir(path_file,0755)

        salida_Layer = "salida_Layer"
        SaveToLayerFile_lyr = path+"\SaveToLayerFile.lyr"
        #..........
        arcpy.TableToTable_conversion("salida.dbf", path, "temporal")
        conversion_dbf="temporal.dbf"

        #.............................

        #Lugar de trabajo
        arcpy.env.workspace = path
        arcpy.env.overwriteOutput=True

        # Process: Table to Table
        expresion = arcpy.AddFieldDelimiters(arcpy.env.workspace, ATRIBUTO) + "=" + "'"+V_ATRIBUTO +"'"
        arcpy.TableToTable_conversion(conversion_dbf, path, "salida",expresion)

        # Process: Make XY Event Layer
        datum = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                           PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],\
                           VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
                           PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];\
                           -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
                           0.001;0.001;IsHighPrecision"

        sr = arcpy.SpatialReference()
        sr.loadFromString(datum)
        arcpy.MakeXYEventLayer_management("salida.dbf", "Longitud", "Latitud", salida_Layer, sr)

        saved_Layer="salidalyr"
        # Process: Save To Layer File
        arcpy.SaveToLayerFile_management(salida_Layer, saved_Layer)
        arcpy.PackageLayer_management("salidalyr.lyr","paquete_capa")

        #....................................

        #Lugar de trabajo
        arcpy.env.workspace = path_file
        arcpy.env.overwriteOutput=True

        # Process: Table to Table
        expresion = arcpy.AddFieldDelimiters(arcpy.env.workspace, ATRIBUTO) + "=" + "'"+V_ATRIBUTO +"'"
        arcpy.TableToTable_conversion(conversion_dbf, path_file, V_ATRIBUTO_NAME ,expresion)

        # Process: Make XY Event Layer

        arcpy.MakeXYEventLayer_management(path+"/salida.dbf", "Longitud", "Latitud", V_ATRIBUTO_NAME, sr)


        # Process: Save To Layer File
        arcpy.SaveToLayerFile_management(V_ATRIBUTO_NAME, V_ATRIBUTO_NAME)

        arcpy.PackageLayer_management(V_ATRIBUTO_NAME+".lyr",V_ATRIBUTO_NAME)
        #arcpy.PackageLayer_management(HNOMBRE+".lyr","V_ATRIBUTO")

        #....................................

        #arcpy.RefreshActiveView()
        #arcpy.RefreshTOC()

        #arcpy.RefreshCatalog("SaveToLayerFile_lyr_filtrada.lyr")
        if Create_Shapefile.upper()=="SI":
            arcpy.FeatureClassToShapefile_conversion([salida_Layer,"salida_original.lyr"],Address_Shapefile)
        return