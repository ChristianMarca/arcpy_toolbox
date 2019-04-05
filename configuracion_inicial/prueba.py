import arcpy
import xlrd
import xlwt
import numpy as np
import pandas  as pd
import os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        #params = None
        #return params

        param0=arcpy.Parameter()
        param0.name="ITEMS"
        param0.displayName="CAMPOS"
        param0.parameterType="Optional"
        param0.datatype="GPString"
        param0.multiValue=True
        param0.filter.type="ValueList"

        return [param0]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        path=os.path.dirname(os.path.abspath(__file__))
        df=pd.read_excel(path+'\REGISTRO SAI OTH-ATH.xls',sheetname='REGISTRO SAI',header=None,skiprows=4,)

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

        book=xlrd.open_workbook(path+'\REGISTRO SAI OTH-ATH.xlsx')
        RegistroSai=book.sheet_by_index(0)

        df=pd.read_excel(path+'\REGISTRO SAI OTH-ATH.xls',sheetname='REGISTRO SAI',header=None,skiprows=4,)

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
            messages.addMessage("No selected")
            cont=[2,42,43,44,45,46,47,48,49,50,51,52,53,54]
        messages.addMessage(sorted(cont))

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
            os.remove(path+'\\DATA_PRUEBAk.xlsx')
        except Exception as e:
            messages.addMessage("Hola mundo")
        #writer = pd.ExcelWriter(path+'\\Datos.xls')
        #Data.to_excel(writer,'Registro Sai',index=False,header=False)
        #writer.save()

        writer = pd.ExcelWriter(path+'\\DATA_PRUEBAk.xlsx',engine='xlsxwriter')
        Data.to_excel(writer,sheet_name='Registro SAI', index=False, header=False)
        workbook=writer.book
        worksheet=writer.sheets['Registro SAI']
        #writer.save()
        formato1=workbook.add_format({'num_format':'#,##0.00'})
        #Data.to_excel(writer, 'Registro Sai', index=False, header=False)
        worksheet.set_column('I:I',1,formato1)
        writer.save()


        return
