import json
import requests
#idTorneo es el identificador del torneo el cual debe de ser anexado a la variable url;
idTorneo = "sdQpSTjp"
url = 'https://lichess.org/api/tournament/'+idTorneo+'/results'
r = requests.get(url, allow_redirects=True)
#Creamos los documentos con la información requerida para crear nuestra lista de rendimiento.
open('C:/creaListaDerendimiento/results', 'wb').write(r.content)
f = open('C:/creaListaDerendimiento/results', "r")
g= open('C:/creaListaDerendimiento/filter', "w+")
#FIltramos unicamente los miembros de nuestro equipo y los escribimos en nuestro archivo.
for x in f:
    y = json.loads(x)
    #Especificamos de cual equipo queremos obtener sus jugadores con su respectiva información.
    if y["team"] == "caballo-negro-chess-club":
        g.write(x)
f.close()
g.close()
