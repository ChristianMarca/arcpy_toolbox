import arcpy
import os
import shutil
import pandas as pd
import numpy as np
import xlrd
import xlwt
import Data_Base as DB
import Filtrar_Campos as FC
import Generar_Excel as GE

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Registro SAI"
        self.alias = "Registro SAI"

        # List of tool classes associated with this toolbox
        self.tools = [Generate_data,Filters,Generate_Data_Compatible]


class Generate_data(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate_data"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        path=os.path.dirname(os.path.abspath(__file__))+"\\temp"
        #................................................................................................................
        fields = arcpy.ListFields(path+"/conversion.dbf")
        CAMPO=[]
        V_CAMPO=[]

        for field in fields:
            CAMPO.append(field.name)

        CAMPO_C=arcpy.Parameter(name="ATRIBUTO",displayName="CAMPO",datatype="String",parameterType="Required")
        CAMPO_C.value="PROVINCIA"
        CAMPO_C.filter.list=CAMPO

        cursor = arcpy.da.SearchCursor(path+"\conversion.dbf", CAMPO_C.value)
        for row in cursor:
            V_CAMPO.append(format(row[0]))

        CAMPO_V=arcpy.Parameter(name="V_ATRIBUTO",displayName="VALOR DEL CAMPO",datatype="String",parameterType="Required")
        value=sorted(set(V_CAMPO))
        CAMPO_V.filter.list=value

        SAVE_S=arcpy.Parameter(name="Create_Shapefile",displayName="Desea Crear ShapeFile",datatype="String",parameterType="Required")
        SAVE_S.value="NO"
        SAVE_S.filter.list=["NO","SI"]

        ADDRESS=arcpy.Parameter(name="Direccion de salida",displayName="Direccion",datatype="Address Locator",parameterType="Optional")
        ADDRESS.value=path
        #..............................................................................

        fields_1 = arcpy.ListFields(path + "/conversion_1.dbf")
        CAMPO_1 = []
        V_CAMPO_1 = []

        for field in fields_1:
            CAMPO_1.append(field.name)

        CAMPO_C_1 = arcpy.Parameter(name="ATRIBUTO", displayName="CAMPO", datatype="String", parameterType="Required")
        CAMPO_C_1.value = "PROVINCIA_"
        CAMPO_C_1.filter.list = CAMPO

        cursor = arcpy.da.SearchCursor(path + "\conversion.dbf", CAMPO_C_1.value)
        for row in cursor:
            V_CAMPO_1.append(format(row[0]))

        CAMPO_V_1 = arcpy.Parameter(name="V_ATRIBUTO", displayName="VALOR DEL CAMPO", datatype="String",
                                  parameterType="Required")
        value = sorted(set(V_CAMPO_1))
        CAMPO_V_1.filter.list = value

        SAVE_S_1 = arcpy.Parameter(name="Create_Shapefile", displayName="Desea Crear ShapeFile", datatype="String",
                                 parameterType="Required")
        SAVE_S_1.value = "NO"
        SAVE_S_1.filter.list = ["NO", "SI"]

        ADDRESS_1 = arcpy.Parameter(name="Direccion de salida", displayName="Direccion", datatype="Address Locator",
                                  parameterType="Optional")
        ADDRESS_1.value = path

        #..............................................................................
        return [CAMPO_C,CAMPO_V,SAVE_S,ADDRESS,CAMPO_C_1,CAMPO_V_1,SAVE_S_1,ADDRESS_1]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        path=os.path.dirname(os.path.abspath(__file__))+"/temp"+"\conversion.dbf"

        cursor = arcpy.da.SearchCursor(path, parameters[0].valueAsText)
        V_CAMPO=[]
        for row in cursor:
            V_CAMPO.append(format(row[0]))
        value=sorted(set(V_CAMPO))

        parameters[1].filter.list=value
        path = os.path.dirname(os.path.abspath(__file__)) + "/temp" + "\conversion_1.dbf"

        cursor_1 = arcpy.da.SearchCursor(path, parameters[4].valueAsText)
        V_CAMPO_1 = []
        for row in cursor_1:
            V_CAMPO_1.append(format(row[0]))
        value_1 = sorted(set(V_CAMPO_1))

        parameters[5].filter.list = value_1
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
        messages.addMessage("Campo: " +ATRIBUTO)
        messages.addMessage("Valor de Campo: " +V_ATRIBUTO)
        path=os.path.dirname(os.path.abspath(__file__))
        DB.ejecutar(path,ATRIBUTO,V_ATRIBUTO,Create_Shapefile,Address_Shapefile)

        return

class Filters(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Filters"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        path=os.path.dirname(os.path.abspath(__file__))+"/temp"+"\salida.dbf"

        fields = arcpy.ListFields(path)
        CAMPO=[]
        V_CAMPO=[]
        for field in fields:
            CAMPO.append(field.name)

        CAMPO_C = arcpy.Parameter(name="ATRIBUTO", displayName="CAMPO", datatype="String", parameterType="Required")
        CAMPO_C.value = "PROVINCIA"
        CAMPO_C.filter.list = CAMPO

        cursor = arcpy.da.SearchCursor(path, CAMPO_C.value)
        for row in cursor:
            V_CAMPO.append(format(row[0]))

        CAMPO_V = arcpy.Parameter(name="V_ATRIBUTO", displayName="VALOR DEL CAMPO", datatype="String",
                                  parameterType="Required")
        value = sorted(set(V_CAMPO))
        CAMPO_V.filter.list = value

        SAVE_S = arcpy.Parameter(name="Create_Shapefile", displayName="Desea Crear ShapeFile", datatype="String",
                                 parameterType="Required")
        SAVE_S.value = "NO"
        SAVE_S.filter.list = ["NO", "SI"]

        ADDRESS = arcpy.Parameter(name="Direccion de salida", displayName="Direccion", datatype="Address Locator",
                                  parameterType="Optional")
        ADDRESS.value = path

        return [CAMPO_C, CAMPO_V, SAVE_S, ADDRESS]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        path=os.path.dirname(os.path.abspath(__file__))+"/temp"+"\salida.dbf"
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
        path=os.path.dirname(os.path.abspath(__file__))
        FC.ejecutar(path,ATRIBUTO,V_ATRIBUTO,Create_Shapefile,Address_Shapefile)
        messages.addMessage("Campo: " +ATRIBUTO)
        messages.addMessage("Valor de Campo: " +V_ATRIBUTO)
        return

class Generate_Data_Compatible(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate_Data_Compatible"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        CAMPO=arcpy.Parameter(name="ITEMS",displayName="CAMPOS",datatype="GPString",parameterType="Optional")
        CAMPO.multiValue=True
        CAMPO.filter.type="ValueList"

        return [CAMPO]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        path=os.path.dirname(os.path.abspath(__file__))
        df=pd.read_excel(path+"\\Archivos Base de Datos"+'\REGISTRO SAI OTH-ATH.xlsx',sheetname='REGISTRO SAI',header=None,skiprows=4,)

        datos=df.iloc[[0],:]
        da=[]
        cabecera=[]
        for index in datos[:].values.tolist():
            da=index

        for index in da:
            cabecera.append(index.encode('utf8'))

        #parameters[0].filter.list=sorted(set(cabecera))
        parameters[0].filter.list=cabecera
        #parameters[0].value=["PERMISIONARIO","PROVINCIA"]

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        invalues=parameters[0].valueAsText
        path=os.path.dirname(os.path.abspath(__file__))
        GE.ejecutar(path,invalues)
        return