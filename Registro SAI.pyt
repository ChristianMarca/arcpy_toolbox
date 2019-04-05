#!/usr/bin/env python
#-*- coding: utf-8 -*-
import arcpy
import os
import Data_Base as DB
import Filtrar_Campos as FC
import directorios as dr
import codecs

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Registro SAI"
        self.alias = "Registro SAI"

        # List of tool classes associated with this toolbox
        self.tools = [Generate_data, Filters, Generate_Data_Compatible]


class Generate_data(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate_data"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        path = os.path.dirname(os.path.abspath(__file__))
        DB.leer_excel(path)
        DB.Iniciar_valor()
        DB.ejecutar(path)

        return


class Filters(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Filters"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        pathk="C:\Users\EstChristianRafaelMa\Documents\ArcGIS\Default.gdb\\tabla"
        path = os.path.dirname(os.path.abspath(__file__)) + "/temp" + "\\salida.dbf"
        fields = arcpy.ListFields(path)
        fields_=arcpy.ListFields(pathk)
        CAMPO = []
        V_CAMPO = []
        for field in fields:
            CAMPO.append(field.name)

        CAMPO_ = []
        for field in fields_:
            CAMPO_.append(field.name)

        CAMPO_C = arcpy.Parameter(name="ATRIBUTO", displayName="CAMPO", datatype="String", parameterType="Required")
        CAMPO_C.value = "PROVINCIA"
        CAMPO_.pop(0)
        CAMPO_.remove('ESTACION_A')
        CAMPO_.remove('ESTACION_B')
        CAMPO_.remove('LATITUD_A')
        CAMPO_.remove('LATITUD_B')
        CAMPO_.remove('LONGITUD_A')
        CAMPO_.remove('LONGITUD_B')
        CAMPO_.remove('Latitud')
        CAMPO_.remove('Longitud')

        CAMPO_C.filter.list = CAMPO_
        cursor = arcpy.da.SearchCursor(path, CAMPO)
        for row in cursor:
            V_CAMPO.append(format(row[0]))

        CAMPO_V = arcpy.Parameter(name="V_ATRIBUTO", displayName="VALOR DEL CAMPO", datatype="String",
                                  parameterType="Required")
        value = sorted(set(V_CAMPO))
        CAMPO_V.filter.list = value

        SAVE_S = arcpy.Parameter(name="Data de Origen", displayName="Data a Filtrar", datatype="String",
                                 parameterType="Required")
        SAVE_S.value = "Filtrada"
        SAVE_S.filter.list = ["Filtrada", "Original"]

        return [CAMPO_C, CAMPO_V, SAVE_S]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[2].valueAsText == "Filtrada":
            try:
                path = os.path.dirname(os.path.abspath(__file__)) + "/temp" + "\\salida.dbf"
            except Exception as e:
                path = os.path.dirname(os.path.abspath(__file__)) + "/temp" + "\conversion.dbf"
        else:
            path = os.path.dirname(os.path.abspath(__file__)) + "/temp" + "\conversion.dbf"

        # ...............................................................
        pathk="C:\Users\EstChristianRafaelMa\Documents\ArcGIS\Default.gdb\\tabla"
        fields = arcpy.ListFields(path)
        fields_ = arcpy.ListFields(pathk)
        CAMPO = []
        for field in fields:
            CAMPO.append(field.name)

        CAMPO_ = []
        for field in fields_:
            CAMPO_.append(field.name)

        CAMPO_C = arcpy.Parameter(name="ATRIBUTO", displayName="CAMPO", datatype="String", parameterType="Required")
        CAMPO_C.value = "PROVINCIA"
        CAMPO_C.filter.list = CAMPO
        CAMPO_.pop(0)
        CAMPO_.remove('ESTACION_A')
        CAMPO_.remove('ESTACION_B')
        CAMPO_.remove('LATITUD_A')
        CAMPO_.remove('LATITUD_B')
        CAMPO_.remove('LONGITUD_A')
        CAMPO_.remove('LONGITUD_B')
        CAMPO_.remove('Latitud')
        CAMPO_.remove('Longitud')
        parameters[0].filter.list = CAMPO_
        # ...............................................................

        try:
            cursor = arcpy.da.SearchCursor(path, parameters[0].valueAsText[:10])
            V_CAMPO = []
            for row in cursor:
                V_CAMPO.append(format(row[0]))
        except Exception as e:
            cursor = arcpy.da.SearchCursor(path, parameters[0].valueAsText[:9])
            V_CAMPO = []
            for row in cursor:
                V_CAMPO.append(format(row[0]))
        # value=sorted(set(V_CAMPO))
        parameters[1].filter.list = sorted(set(V_CAMPO))

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):

        """The source code of the tool.
        Obtencion de parametros dados por el usuarios
        Los parametros son /Campo del cual se requiere la informacion/Valor del campo del cual se requiere la informacion/Base de datos de la cual se realizara la busqueda
        Ejecucion del modulo de filtrado que  dos funciones en la fecha 9/3/2018 son independientes las funciones en dinde estas permiten
        ejecutar(path_1,ATRIBUTO,V_ATRIBUTO,Data_set)
           Recibe la base de datos elegida y crea una nueva base de datos (guaradando la base de datos actual) con el cual se generan campos propios de la ejecucion del filtro
        selection(ATRIBUTO,V_ATRIBUTO,Data_set)
            Recibe la base de datos de del filtro ejecutado y crea las capas de Enlaces con las propiedades entregadas de la base de datos ya filtrada
        """

        ATRIBUTO = parameters[0].valueAsText[:10]
        V_ATRIBUTO = parameters[1].valueAsText

        Data_set = parameters[2].valueAsText
        path = os.path.dirname(os.path.abspath(__file__))

        V_ATRIBUTO_NAME=""
        for letra in V_ATRIBUTO:
            if letra=="." or letra=="." or letra=="-" or letra==" " or letra=="&" or letra=="/" or letra==";" or letra=="\xc2\xbf".decode('utf8') or letra==",":
                print("NO ASCII")
            else:
                V_ATRIBUTO_NAME=V_ATRIBUTO_NAME+letra

        #messages.addMessage("Campo: " + ATRIBUTO)
        #messages.addMessage("Valor de Campo: " + V_ATRIBUTO)
        mdx=arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mdx, "Layers")[0]
        for lyr in arcpy.mapping.ListLayers(mdx, "*", df):
            arcpy.mapping.RemoveLayer(df, lyr)
        dfh=FC.ejecutar(path, ATRIBUTO, V_ATRIBUTO, Data_set)
        #messages.addMessage(dfh)
        addLayer = arcpy.mapping.Layer(path + "\\data\\mapa\\nxprovincias.lyr")
        simbologia = arcpy.mapping.Layer(path + "\\data\\simbologia.lyr")
        def simbology_apply(layer_,NAME):
            #arcpy.mapping.AddLayer(df, layer_, "BOTTOM")
            arcpy.mapping.UpdateLayer(df, layer_, simbologia, True)
            if layer_.symbologyType == "UNIQUE_VALUES":
                layer_.symbology.valueField = NAME+".PERMISIONA"
                layer_.symbology.addAllValues()
            #arcpy.mapping.AddLayer(df, layer_, "BOTTOM")
            #arcpy.RefreshActiveView()
            #arcpy.RefreshTOC()
            return layer_
        #------AGREGA ETIQUETAS------------------
        def etiquetas(lyr,ClassName,Values_Expresion,Enter,Visible):
            cabecera = """ "<FNT name='Arial'>\" """
            indice = """\"</FNT>\" """
            espaciador = ["+[", "]"]
            Values_Expresion
            g = ""
            for valores in Values_Expresion:
                if Enter and valores!=Values_Expresion[len(Values_Expresion)-1]:
                    g = g + str(espaciador[0]) + valores + str(espaciador[1])+"+vbCrLf"
                else:
                    g = g + str(espaciador[0]) + valores + str(espaciador[1])
            if lyr.supports("LABELCLASSES"):
                for _lyr_ in lyr.labelClasses:
                    _lyr_.className = ClassName
                    _lyr_.Parser = "PYTHON_9.3"
                    _lyr_.expression =cabecera+ g +"+"+ indice
                    _lyr_.showClassLabels = Visible
                    _lyr_.visible = Visible
            lyr.showLabels = Visible
            return lyr
        dire = dr.Directorio()
        def listdir_recurd(files_list, root, folder, checked_folders, ruta_actual, destino):
            dest = destino
            if (folder != root):
                checked_folders.append(folder)

            for f in os.listdir(folder):
                d = os.path.join(folder, f)
                if os.path.isdir(d) and d not in checked_folders:
                    if os.path.join(folder, f) == os.path.join(folder, dest):
                        ruta_actual.append(os.path.join(folder, f))
                        print os.path.join(folder, dest)
                    listdir_recurd(files_list, root, d, checked_folders, ruta_actual, dest)
            return ruta_actual
        f=codecs.open(path + "\\temp\\address.txt","r",encoding='utf-8')
        address = listdir_recurd([], path + "\\data", path + "\\data", [], [], f.read())
        adds = sorted(address)
        f.close()

        path_filek = adds[0]
        dire.extract_data(path_filek)
        #messages.addMessage("dsa")
        #messages.addMessage(dire.files)
        arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
        #df.extent = addLayer.getSelectedExtent()
        f = open(path + "\\temp\\name.txt", "r")
        V_ATRIBUTO_NAME_CONCAT = f.read()
        f.close()
        #messages.addMessage(V_ATRIBUTO_NAME_CONCAT)
        for lyr in dire.files:
            if os.path.splitext(lyr)[1] == '.lyr':
                if lyr[len(lyr) - 5] == "_":
                    other='C:\Users\EstChristianRafaelMa\Desktop\ARGIS_PASANTIA\ToolBoox\\temp\EliminarNaN.lyr'
                    layer_k=lyr.replace(".lyr","_")
                    layer_l=lyr.replace(".lyr","")
                    arcpy.MakeFeatureLayer_management(lyr,layer_k)
                    find = arcpy.SelectLayerByLocation_management(layer_k, 'WITHIN', other, "","",'INVERT')
                    arcpy.Delete_management(layer_l)
                    prelo=arcpy.MakeFeatureLayer_management(find,layer_l)
                    prf=arcpy.SaveToLayerFile_management(prelo,layer_l,"ABSOLUTE")
                    arcpy.Delete_management(layer_k)
                    layer = arcpy.mapping.Layer(path_filek+"\\"+layer_l+".lyr")
                    #layer = arcpy.mapping.Layer(path_filek + "\\" + lyr)
                    # layer = simbology_apply(layer)
                    layer = etiquetas(layer, "Nodos", ["P___S___SE"], False, True)
                    layer.transparency = 60
                    arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")
                    #df.extent = layer.getSelectedExtent()
                elif lyr[len(lyr) - 5] == "A" or lyr[len(lyr) - 5] == "B":
                    #layer = arcpy.mapping.Layer(path_filek + "\\" + lyr)
                    other = 'C:\Users\EstChristianRafaelMa\Desktop\ARGIS_PASANTIA\ToolBoox\\temp\EliminarNaN.lyr'
                    layer_k = lyr.replace(".lyr", "_")
                    layer_l = lyr.replace(".lyr", "")
                    arcpy.MakeFeatureLayer_management(lyr, layer_k)
                    find = arcpy.SelectLayerByLocation_management(layer_k, 'WITHIN', other, "", "", 'INVERT')
                    arcpy.Delete_management(layer_l)
                    prelo = arcpy.MakeFeatureLayer_management(find, layer_l)
                    prf = arcpy.SaveToLayerFile_management(prelo, layer_l, "ABSOLUTE")
                    arcpy.Delete_management(layer_k)
                    layer = arcpy.mapping.Layer(path_filek + "\\" + layer_l + ".lyr")

                    layer = etiquetas(layer, "Estaciones", ["TIPO_SERVI"], False, True)
                    arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")
                    #df.extent = layer.getSelectedExtent()
                elif lyr[len(lyr) - 5] == "S":
                    #layer = arcpy.mapping.Layer(path_filek + "\\" + lyr)
                    other = 'C:\Users\EstChristianRafaelMa\Desktop\ARGIS_PASANTIA\ToolBoox\\temp\EliminarNaN.lyr'

                    layer_k = lyr.replace(".lyr", "_")
                    layer_l = lyr.replace(".lyr", "")
                    arcpy.MakeFeatureLayer_management(lyr, layer_k)
                    find = arcpy.SelectLayerByLocation_management(layer_k, 'WITHIN', other, "", "", 'INVERT')
                    arcpy.Delete_management(layer_l)
                    prelo = arcpy.MakeFeatureLayer_management(find, layer_l)
                    prf = arcpy.SaveToLayerFile_management(prelo, layer_l, "ABSOLUTE")
                    arcpy.Delete_management(layer_k)
                    layer = arcpy.mapping.Layer(path_filek + "\\" + layer_l + ".lyr")

                    try:
                        layer = simbology_apply(layer,V_ATRIBUTO_NAME_CONCAT)
                    except Exception:
                        messages.addMessage('Simbologia no valida, cree una compatible')
                        arcpy.AddWarning("Simbologia no Compatible")
                    layer = etiquetas(layer, "Enlaces", [V_ATRIBUTO_NAME_CONCAT.decode('utf8')+".PERMISIONA", V_ATRIBUTO_NAME_CONCAT.decode('utf8')+"."+ATRIBUTO], True, True)
                    arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")
                    #df.zoomToSelectedFeatures()
                    #df.extent = layer.getSelectedExtent()
                    df.scale *= 0.5
                    #df.extent = layer.getSelectedExtent()
        #arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
        #arcpy.SelectLayerByAttribute_management(layerE, "NEW_SELECTION",V_ATRIBUTO_NAME_CONCAT.decode('utf8')+".PROVINCIA"+"='LOJA'")
        #df.zoomToSelectedFeatures()
        #df.zoomToSelectedFeatures()
        #df.extent = layerE.getSelectedExtent()
        #ext = layerE.getExtent()
        #ext = layer.getSelectedExtent()
        #df.extent = ext
        #df.scale *= 1000,000000
        #activeFrame=mdx.activeDataFrame
        #activeFrame.extent=layer.getSelectedExtent()

        #arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")
        arcpy.RefreshActiveView()
        #arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        del mdx
        return


class Generate_Data_Compatible(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Generate_Data_Compatible"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        CAMPO = arcpy.Parameter(name="ITEMS", displayName="CAMPOS", datatype="GPString", parameterType="Optional")
        CAMPO.multiValue = True
        CAMPO.filter.type = "ValueList"

        return [CAMPO]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        path = os.path.dirname(os.path.abspath(__file__))
        """
        df = pd.read_excel(path + "\\Archivos Base de Datos" + '\REGISTRO SAI OTH-ATH.xlsx', sheetname='REGISTRO SAI',
                           header=None, skiprows=4, )

        datos = df.iloc[[0], :]
        da = []
        cabecera = []
        for index in datos[:].values.tolist():
            da = index

        for index in da:
            cabecera.append(index.encode('utf8'))

        # parameters[0].filter.list=sorted(set(cabecera))
        parameters[0].filter.list = cabecera
        # parameters[0].value=["PERMISIONARIO","PROVINCIA"]
        """
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        invalues = parameters[0].valueAsText
        path = os.path.dirname(os.path.abspath(__file__))
        #GE.ejecutar(path, invalues)
        return
