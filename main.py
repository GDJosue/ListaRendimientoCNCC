#Librerias necesarias para que funcione el programa
import requests
import xlsxwriter
import json
import openpyxl

def maxColum(sheet):
    auxtemp = 0
    columna = 0
    if sheet['B' + str(5)].value is None:
        columna = 2
    else:
        for j in range(26):
            auxtemp = 0
            for m in range(1, sheet.max_row-4):
                if sheet[chr(j + 97) + str(m+4)].value is None:
                    auxtemp = auxtemp + 1
            print(auxtemp)
            if auxtemp == sheet.max_row-5:
                columna = j
                break
    return columna+1

#idTorneo es el identificador del torneo el cual debe de ser anexado a la variable url;
idTorneo = "XqClhOsm"
url = 'https://lichess.org/api/tournament/'+idTorneo+'/results'
r = requests.get(url, allow_redirects=True)
#Creamos los documentos con la información requerida para crear nuestra lista de rendimiento.
open('C:/creaListaDerendimiento/results', 'wb').write(r.content)
f = open('C:/creaListaDerendimiento/results', "r")
g = open('C:/creaListaDerendimiento/filter', "w+")
#FIltramos unicamente los miembros de nuestro equipo y los escribimos en nuestro archivo.
for x in f:
    y = json.loads(x)
    #Especificamos de cual equipo queremos obtener sus jugadores con su respectiva información.
    if y["team"] == "caballo-negro-chess-club":
        g.write(x)
f.close()
g.close()
#Creamos una lista previa en excel
workbook = xlsxwriter.Workbook('C:/creaListaDerendimiento/preview.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
g = open('C:/creaListaDerendimiento/filter', "r")
for x in g:
    y = json.loads(x)
    worksheet.write(row, col, str(y["username"]))
    worksheet.write(row, col + 1, str(y["score"]))
    row += 1
g.close()
workbook.close()
#Acomodar los puntos realizados y en base de de ellos sumarlos en el excel de forma acumulativa.
torneoActual = openpyxl.load_workbook('C:/creaListaDerendimiento/preview.xlsx')
rendimientoActual = openpyxl.load_workbook('C:/creaListaDerendimiento/final.xlsx')
sheet_rangesTA = torneoActual['Sheet1']
sheet_rangesRA = rendimientoActual['Sheet1']
print("Las filas maximas del documento es:"+str(sheet_rangesRA.max_row))
print("El numero maximo de columas es:"+str(maxColum(sheet_rangesRA))+"En otras palabras en la letra:"+chr(maxColum(sheet_rangesRA)+96))
columnaMax = maxColum(sheet_rangesRA)
aux = 0
for x in range(1, sheet_rangesTA.max_row + 1):
    if sheet_rangesRA['A' + str(x + 4)].value is None:
        sheet_rangesRA['A' + str(x + 4)].value = sheet_rangesTA['A' + str(x)].value
        sheet_rangesRA[chr(columnaMax+96) + str(x + 4)].value = sheet_rangesTA['B' + str(x)].value
    else:
        for y in range(1, sheet_rangesTA.max_row + 1):
            if sheet_rangesRA['A'+str(x+4)].value == sheet_rangesTA['A' + str(y)].value:
                print(sheet_rangesRA['A'+str(x+4)].value)
                sheet_rangesRA[chr(columnaMax + 96) + str(x + 4)].value = sheet_rangesTA['B' + str(x)].value
            else:
                aux =+ 1
            if(aux == sheet_rangesTA.max_row + 1):
                sheet_rangesRA['A'+str(sheet_rangesTA.max_row + 1)].value = sheet_rangesTA['A' + str(y)].value
                sheet_rangesRA[chr(columnaMax + 96) + str(x + 4)].value = sheet_rangesTA['B' + str(x)].value
rendimientoActual.save("C:/creaListaDerendimiento/final.xlsx")





