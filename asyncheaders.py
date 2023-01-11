#-*-coding:utf-8-*-
#pip install python-wappalyzer
#pip install aiohttp
#!/usr/bin/env python

import aiohttp
import asyncio
import time
import argparse
from Wappalyzer import Wappalyzer, WebPage
from bs4 import BeautifulSoup


async def fetch(session, url, port):
	fallo=0
	try:
		async with session.get(url, timeout=2, ssl=False) as response:
			datos=[]
		#        return await response.text()
			datos.append(url)
			datos.append(str(response.status))
			datos.append(await response.text())
			datos.append(response.headers.get('Server', ""))
			datos.append(response.headers.get('Location', ""))
			#print(response.headers)
			datos.append(port)
			datos.append(response.headers.get('X-Powered-By', ""))
	except aiohttp.client_exceptions.ClientConnectorCertificateError:
		print('SSL error caught')
		fallo="1"

	except aiohttp.client_exceptions.ClientConnectorError:
		print("------------------------------")
		print("Puerto "+port+" close")
		fallo="2"
	except asyncio.TimeoutError:
		print("------------------------------")
		print("Puerto "+port+" close")	
		fallo="3"

	if fallo != 0:
		datos=[]
		datos.append("")
		datos.append("")
		datos.append("")
		datos.append("")
		datos.append("")
		datos.append("")
		datos.append("")

	return datos


async def bucleespaciotemporal(urls,puertoshttp,puertoshttps,guardaren):
	async with aiohttp.ClientSession() as session:
		for dominio in f:
#Al existir dos await dentro del bucle se llaman dos veces una para http y otra para https lo suyo es crear dos arrays de tareas concurrentes
			#tareas para http
			tasks = []
			#tareas para https
			taskss = []
			dominio=dominio.replace('\n','')
			url="http://"+dominio
			urls="https://"+dominio
			for httport in puertoshttp:
				url2=url+":"+httport+"/"
				#print (url2)
				tasks.append(fetch(session, url2, httport))
				name = url.split("/")[2]
			htmls = await asyncio.gather(*tasks)
			for html in htmls:
				dom=html[0]
				code=html[1]
				servidor=html[3]
				powered=html[6]
				redireccion=html[4]
				#puelto=html[5]
				web=BeautifulSoup(html[2],'html.parser')
				title= web.find('title')
				aux=str(title)
				aux=aux.replace("title>","").replace("<","").replace("/","")
				print ("------------"+dom+"------------------")

				#print ("Puerto: "+puelto)
				if code != "":
					guardaren.write("------------"+dom+"------------------\nCodigo HTTP: " + code+"\nServidor: " + servidor+"\n")
					print("Codigo HTTP: " + code)
					print("Servidor: " + servidor)
					wappalyzer = Wappalyzer.latest()
					webpage = WebPage.new_from_url(dom)
					print("Wappalyzer: "+str(wappalyzer.analyze(webpage)))
					guardaren.write ("Wappalyzer: "+str(wappalyzer.analyze(webpage))+"\n")
					if powered != "" :
						print("X-Powered-By: " + powered)
						guardaren.write("X-Powered-By: "+powered+"\n")
					if redireccion != "":
						print("Redirecciona: " + redireccion)
						guardaren.write("Location" + redireccion + "\n")
					guardaren.write("------------------------------\n")
	
			for httsport in puertoshttps:
				urls2=urls+":"+httsport+"/"
				taskss.append(fetch(session, urls2, httsport))
				names = urls.split("/")[2]
			htmlss = await asyncio.gather(*taskss)
			for html2 in htmlss:
				dom=html2[0]
				code=html2[1]
				servidor=html2[3]
				redireccion=html2[4]
				powered = html2[6]
				#puelto=html2[5]
				web=BeautifulSoup(html2[2],'html.parser')
				title= web.find('title')
				aux=str(title)
				aux=aux.replace("title>","").replace("<","").replace("/","")
				print ("------------"+dom+"------------------")
				#print ("Puerto: "+puelto)
				if code != "" :
					guardaren.write("------------"+dom+"------------------\nCodigo HTTP: " + code+"\nServidor: " + servidor+"\n")
					wappalyzer = Wappalyzer.latest()
					webpage = WebPage.new_from_url(dom, verify=False)
					guardaren.write("Wappalyzer: " + str(wappalyzer.analyze(webpage))+"\n")
					print("Codigo HTTP: "+code)
					print("Servidor: "+servidor)
					print("Wappalyzer: "+str(wappalyzer.analyze(webpage)))
					if powered != "" :
						print("X-Powered-By: " + powered)
						guardaren.write("X-Powered-By: "+powered+"\n")

					if redireccion != "" :
						print("Redirecciona: " + redireccion)
						guardaren.write("Location"+redireccion+"\n")
					guardaren.write("------------------------------\n")

start=time.time()

ayuda = argparse.ArgumentParser()
ayuda.add_argument("--file", help="Indica la ruta donde esta el archivo", required=True)
ayuda.add_argument("--http_port", help="Indica los puertos http")
ayuda.add_argument("--https_port", help="Indica los puertos https")
ayuda.add_argument("--output", help="Indica fichero donde guardar la salida, por defecto salidorra")
args = ayuda.parse_args()
if args.http_port:
	httpport=args.http_port.split(",")
else:
	httpport=['80','81','8080','8000','8008','2082','2095','3000','8888','8834']

if args.https_port:
	httpsport=args.https_port.split(",")
else:
	httpsport=["443","8443","8003","2087","2096","3000","8888","8834"]
if args.output:
	archivo=open(args.output, "w")
else:
	archivo=open("salidorra", "w")
if args.file:
    path_file=args.file
    f = open(path_file, "r")
##Comienza la concurrencia	
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bucleespaciotemporal(f,httpport,httpsport,archivo))
#recorremos cada linea del fichero
    for dominio in f:
        #Eliminamos el retorno de carro para que no lo meta como dominio
        dominio=dominio.replace('\n','')
        print ("----------------"+dominio+"----------------------")
        url="http://"+dominio
        urls="https://"+dominio
        for x in httpport:
            print ("Peticion HTTP")
            peticion_http=peticion(url,x)
            if peticion_http != "FAIL!!!":
                html=BeautifulSoup(peticion_http.text,'html.parser')
                title= html.find('title')
                aux=str(title)
                aux=aux.replace("title>","").replace("<","").replace("/","")
                size=len(peticion_http.content)
                tamano=str(size)
                codigo=str(peticion_http.status_code)
                #print (peticion_http.text)
                print ("Puerto: "+x)
                print ("Titulo: "+aux)
                print ("Tamaño: "+tamano)
                print ("Codigo HTTP: "+codigo)
                if 'Server' in peticion_http.headers :
                    servidor=peticion_http.headers['Server']
                    print ("Servidor: "+servidor)
                else:
                    servidor=""
                #print (peticion_http)
                if 'Location' in peticion_http.headers :
                    redireccion=peticion_http.headers['Location']
                    print ("Redirige a: "+peticion_http.headers['Location'])
                else:
                    redireccion=""
            else:
                print (dominio+" no tiene web en el puerto "+x)
                codigo=""
                servidor=""
                aux=""
                tamano=""
                redireccion=""
            print ("----------------")
            print ("")
            archivo.write("Dominio: "+dominio+", Puerto: "+x+",Codigo HTTP: "+codigo+",Servidor: "+servidor+", Titulo: "+aux+", Tamaño: "+tamano+", Location: "+redireccion+"\n")
            archivo.write("----------------------------\n")
        for y in httpsport:
            print ("Peticion HTTPS")
            peticion_https=peticion(urls,y)
            if peticion_https != "FAIL!!!":
                htmls=BeautifulSoup(peticion_https.text,'html.parser')
                titles= html.find('title')
                sizes=len(peticion_https.content)
                auxs=str(titles)
                auxs=auxs.replace("title>","").replace("<","").replace("/","")
                tamanos=str(sizes)
                codigos=str(peticion_https.status_code)
                #print (peticion_https.text)
                print ("Puerto: "+y)
                print ("Tamaño: "+str(sizes))
                print ("Titulo: "+auxs.replace("title>","").replace("<","").replace("/",""))
                print ("Codigo HTTP: "+str(peticion_https.status_code))
                if 'Server' in peticion_https.headers :
                    servidors=peticion_https.headers['Server']
                    print ("Servidor: "+servidors)
                else:
                    servidors=""
                #print (peticion_https)
                if 'Location' in peticion_https.headers :
                    redireccions=peticion_https.headers['Location']
                    print ("Redirige a: "+redireccions)
                else:
                    redireccions=""
            else:
                print (dominio+" no tiene web en el puerto "+y)
                codigos=""
                servidors=""
                auxs=""
                tamanos=""
                redireccions=""
            print ("")
            archivo.write("Dominio: "+dominio+", Puerto: "+y+",Codigo HTTP: "+codigos+",Servidor: "+servidors+", Titulo: "+auxs+", Tamaño: "+tamanos+", Location: "+redireccions+"\n")
            archivo.write("----------------------------\n")

print ("--------------------------------------------------------------------------------")
archivo.close()
#end=time.time()
#tarda=end-start
#print("El tiempo que tarda en ejecutarse es de: "+tarda)
