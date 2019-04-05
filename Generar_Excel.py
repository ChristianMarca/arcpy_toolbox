#-*- conding: utf-8 -*-
import arcpy
import xlrd
import pandas  as pd
import os

def ejecutar(path,invalues):
    #book=xlrd.open_workbook(path+"\\Archivos Base de Datos"+'\REGISTRO SAI OTH-ATH.xls',formatting_info=True)
    book=xlrd.open_workbook(path+"\\Archivos Base de Datos"+'\REGISTRO SAI OTH-ATH.xlsx')
    RegistroSai=book.sheet_by_index(0)

    df=pd.read_excel(path+"\\Archivos Base de Datos"+'\REGISTRO SAI OTH-ATH.xlsx',sheetname='REGISTRO SAI',header=None,skiprows=4,)

    datos=df.iloc[[0],:]
    try:
        selected_values = invalues.split(";")
        datos_list=[]
        for selected_value in selected_values:
            #arcpy.AddWarning(selected_value)
            arcpy.AddMessage(selected_value)
            datos_list.append(selected_value.encode('utf8').replace("'",""))


        da=[]
        cabecera=[]
        cont=[2,42,43,44,45,46,47,48,49,50,51,52,53,54]
        for index in datos[:].values.tolist():
            da=index

        for index in da:
            cabecera.append(index.encode('utf8'))
        #cont=[]
        #messages.addMessage(len(cabecera))
        #messages.addMessage(len(datos_list))
        for i in range(len(datos_list)):

            for j in range(len(cabecera)):
                if datos_list[i]== cabecera[j]:
                    cont.append(j)

    except Exception as e:
        #messages.addMessage("No selected")
        cont=[2,42,43,44,45,46,47,48,49,50,51,52,53,54]
    #messages.addMessage(sorted(cont))

    datos=df.iloc[:,cont]


    def getColor(book,sheet,fila,col):
        xfx = sheet.cell_xf_index(fila,col)
        xf = book.xf_list[xfx]
        col=xf.background.pattern_colour_index
        color = book.colour_map[col]
        return color

    Color=[]
    """
    for a in range (4, RegistroSai.nrows):
        Aux=getColor(book,RegistroSai,a,2)
        if Aux==None:
            Color.append([1])
        else:
            Color.append([0])
    
    Color[0]='ESTADO'
    """
    df =pd.DataFrame(Color)



    header=cont

    for i in range (len(header)):
        datos[header[i]]=map(lambda x: unicode(x).upper(),datos[header[i]])


    Data=datos.join(df)
    Dataf=Data.drop(1,axis=0)
    try:
        os.remove(path+"Archivos Base de Datos"+'\\DATA_PRUEBA.xls')
    except Exception as e:
        #messages.addMessage("NO DATA")
        print("NO DATA")
    writer = pd.ExcelWriter(path+"\\Archivos Base de Datos"+'\\DATA_PRUEBA.xls')
    Data.to_excel(writer,'Registro Sai',index=False,header=False)
    writer.save()