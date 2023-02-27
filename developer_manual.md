# Cómo se hizo

## Server
Primero había que crear un socket que actuara como servidor..
~~~ python
import socket

# Para instanciar el socket.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
~~~
    
El primer parametro del constructor es la familia del socket, en este caso es `socket.AF_INET` se utiliza para las conecciones con IPv4. El segundo es el tipo de comunicación que tendrá el socket, `SOCK_STREAM` es para una orientada a la conexión, pero también existe `SOCK_DGRAM` para un protocolo no orientado a la conexión.   
   
Luego de esto hay que darle una direccion IP y ponerlo a escuchar.
~~~ python
server_socket.bind((192.168.3.5, 1234))
server_socket.listen(10)
~~~
El método `bind` recibe como argumento una tupla con la dirección IP y el puerto. Y el método `listen` recibe un entero que dicta el máximo de conecciones que puede tener.
    
### Recibir mensajes del cliente.
Para recibir mensajes de los clientes primero hay que aceptar su conección.
~~~ python
while True:
    client_sock, client_addr = server_socket.accept()
~~~
Luego de aceptar la conección entonces se recibe el mensaje.
~~~ python

~~~

