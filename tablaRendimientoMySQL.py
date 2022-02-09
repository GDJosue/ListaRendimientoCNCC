import pymysql
import requests
import json
from datetime import datetime

miConexion = pymysql.connect( host='127.0.0.1', user= 'root', passwd='1234', db='CaballoNegroChessClub' )
torneos = ["PrgJ0eX2"]
tpTorneo = [1]
if len(torneos) == len(tpTorneo):
    print("Es par")
for contador in range(len(torneos)):
    # idTorneo es el identificador del torneo el cual debe de ser anexado a la variable url;
    idTorneo = torneos[contador]
    # Tipo de torneo, 1 para puntos normales, 2 para puntos modificados
    bonificacion = tpTorneo[contador]
    url = 'https://lichess.org/api/tournament/' + idTorneo
    # Esta variable obtendra los resultados del torneo
    r = requests.get(url + '/results', allow_redirects=True)
    # Esta variable obtendra la información completa del torneo
    rn = requests.get(url, allow_redirects=True)
    # Se guarda el Json para obtener el nombre
    infTor = json.loads(rn.content)
    # Obtenemos el nombre completo del torneo
    nombreTorneo = infTor['fullName']
    nombreTorneo=nombreTorneo.replace("'", "_")
    fechaTorneo = datetime.today().strftime('%Y-%m-%d')
    mycursor = miConexion.cursor()
    print("insert ignore torneo values('" + idTorneo + "','" + nombreTorneo + "','" + fechaTorneo + "'," + str(bonificacion) + ");")
    sql = "insert ignore torneo values('" + idTorneo + "','" + nombreTorneo + "','" + fechaTorneo + "'," + str(bonificacion) + ");"
    mycursor.execute(sql)
    miConexion.commit()
    # Creamos los documentos con la información requerida para crear nuestra lista de rendimiento.
    open('C:/creaListaDerendimiento/results', 'wb').write(r.content)
    f = open('C:/creaListaDerendimiento/results', "r")
    g = open('C:/creaListaDerendimiento/filter', "w+")
    # Filtramos unicamente los miembros de nuestro equipo y los escribimos en nuestro archivo.
    for x in f:
        y = json.loads(x)
        # Especificamos de cual equipo queremos obtener sus jugadores con su respectiva información.
        if y["team"] == "caballo-negro-chess-club" or "caballo-negro-chess-club-cncc":
            g.write(x)
    f.close()
    g.close()
    g = open('C:/creaListaDerendimiento/filter', "r")
    for x in g:
        y = json.loads(x)
        jugador = y["username"]
        mycursor = miConexion.cursor()
        print("insert ignore jugadores values('"+jugador+"');")
        sql = "insert ignore jugadores values('"+jugador+"');"
        mycursor.execute(sql)
        miConexion.commit()
        mycursor = miConexion.cursor()
        puntaje = y["score"]
        print("insert into performance values("+str(puntaje*bonificacion)+",'"+idTorneo+"','"+jugador+"','" + fechaTorneo + "');")
        sql = "insert into performance values("+str(puntaje*bonificacion)+",'"+idTorneo+"','"+jugador+"','" + fechaTorneo + "');"
        mycursor.execute(sql)
        miConexion.commit()
    g.close()


