# Asyncheaders
Script utiliza corrutinas para obtener datos de una lista de dominios

# Utilizacion
El script tiene un help,
```
usage: asyncheaders.py [-h] --file FILE [--http_port HTTP_PORT] [--https_port HTTPS_PORT] [--output OUTPUT]
asyncheaders.py: error: the following arguments are required: --file
```
La opción `--file` es la ruta donde se encuentra el archivo con la lista de los dominios.

En caso de no introducir las opciones --http_port --https_port --output, tendrán los siguientes valores por defecto
- `--http_port`: Puertos que se tratara de realizar peticiones http, por defecto,`'80','81','8080','8000','8008','2082','2095','3000','8888','8834'`
- `--https_port`: Puertos que se tratara de realizar peticiones https, por defecto,`"443","8443","8003","2087","2096","3000","8888","8834"`
- `--output`: Es el nombre archivo que tendrá la salida, por defecto será, `salidorras`
