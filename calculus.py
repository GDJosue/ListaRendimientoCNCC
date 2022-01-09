import xlsxwriter
import json
workbook = xlsxwriter.Workbook('C:/creaListaDerendimiento/preview.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
g = open('C:/creaListaDerendimiento/filter', "r")
for x in g:
    y= json.loads(x)
    worksheet.write(row, col, str(y["username"]))
    worksheet.write(row, col + 1, str(y["score"]))
    row += 1
g.close()
workbook.close()