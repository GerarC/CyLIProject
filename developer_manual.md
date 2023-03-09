# **Manual del Desarrollador** - ¿Cómo se hizo?
## Server

### Base del servidor
Para Manejar el *servidor* se creó una clase llamada **Chatroom**,
Los atributos de esta clase definen el tamaño del header, el host, el socket que actuará como *server* y también sus opciones; y una lista con los socket conocidos.
![Chatroom Class](images/Server1.png)

En este caso se especifica un tamaño para el header predefinido, y se crea el socket con las opciones de `AF_INET` para que trabaje con IPv4 y `SOCK_STREAM` para que utilice el protocolo de tipo TCP (Si se quisiera que trabaje con el protocolo UDP se utilizaría `SOCK_DGRAM`). Luego, se definen otras opciones para el socket usando `SOL_SOCKET` para definir la capa del socket la cual se va a configurar y `SO_REUSEADDR` es la opción usada para dejar que el socket reuse direcciones.

Se define un método el cual alza el servidor, y lo pone a escuchar en la dirección guardada en `self._host`.
![Set It Up](images/Server2.png)

Chequea la lista de sockets conocidos y revisa si se pueden leer, o si tienen errores
![Check it](images/Server4.png)

### Recibir información
El método para recibir mensajes recibe el socket de un cliente como parámetro, intenta recibir del cliente el header, y si este está vacío o hay algún error retorna falso, sino decodifica el header y recibe la cantidad de datos que este especifica.
![It receives](images/Server3.png)
El formato del mensaje que recibe el servidor es el siguiente
~~~ python
"<header>  <Mensaje>"
# Donde el header es el tamaño del mensaje y está formateado a ocupar 10 dígitos.
~~~

### Una nueva Conexión

El servidor acepta al socket que haya mandado la solicitud de conectarse y recibe el usuario, si este no tiene un usuario Ignora la conexión, sino lo agrega a la lista de sockets conocidos y al diccionario de clientes.
![Connect it](images/Server5.png)

### Remover un Cliente
Es solo eliminarlo de la lista de sockets conocidos y removerlo del diccionario de clientes.
![Remove it](images/Server6.png)

### Recibiendo mensajes
Para Recibir un mensaje, se intenta recibir la información, si no hay información, entonces se elimina el socket de la lista de clientes y ya, si se recibe alguna información entonces se junta la información de quién lo envió con el mensaje que envió y se retorna eso (Después se usará para enviarlo a los clientes).
![Receive its message](images/Server7.png)

### Esparciendo mensajes
Para que a todos los clientes se les envíe la información se recorre la lista de clientes y se verifica que no sean el socket de origen, y se usa el comando del socket para enviar la información.
![Broadcast](images/Server8.png)

### Todo Junto, En un Bucle
![Bucle](images/Server9.png)

Para que todo esto funcione se instancia un objeto de la Clase `Chatroom` especificándole el tamaño del header, la dirección IP y el puerto en donde escuchará, se pone a escuchar y en un bucle se van chequeando qué sockets están bien y cuales están mal con `chatroom.check_sockets()`, los que están mal se eliminan de los sockets conocidos y de los clientes, a los que si están bien, incluyendo el servidor, se los itera. Cada vez que se tenga el socket del servidor se aceptarán nuevas opciones con `chatroom.newconnection`. A los clientes se leen los mensajes que hayan enviados y luego se esparce esa información al resto de clientes con el método `chatroom.broad_message`.

## Cliente

###  Base del cliente
Para el manejar el cliente se creó una clase llamada **ChatClient** que tiene como atributos el tamaño del header (El mismo que el del servidor), el nombre de usuario, el header del nombre del usuario, el host (una tupla con la dirección IP y el Puerto donde escucha el servidor), y el socket que se conecta al servidor que es de tipo TCP y tabaja con IPv4.
![Cliente](images/Client1.png)

El método que conecta al socket con el servidor, evita que el socket se bloquee y envía el usuario para que el servidor lo guarde en el diccionario de clientes.
![Set it up](images/Client2.png)

### Mandar Mensajes
Para mandar mensajes solo se codifica el mensaje, se crea su header (Con el tamaño del mensaje) y luego se mandan juntos con el método `send` del socket.
![Send it](images/Client3.png)

### Recibir Mensajes
Estos dos métodos hace casi lo mismo, uno recibe el header del nombre del usuario, si no existe entonces es que se cerró la sesión desde el servidor. Si lo recibe entonce retorna el string resultante de decodificarlo.

Por parte de `receive_message` no se verifica si hay o no hay conexión porque se supone que ya debió de llegar alguna información (el nombre de usuario).
![Receive it](images/Client4.png)

### Vista del cliente
Aquí lo único importante a resaltar es que se instancia un objeto de tipo `ChatClient`.
![chatview](images/Client5.png)

### Bucle Principal
Este es el bucle principal, acá se recibe los mensajes y se insertan en el Text de la vista. Las excepciones tienen que ver de la parte de `IOError` tienen que ver con la opción de `setblocking` que configuramos antes `EAGAIN` viene a ser inténtalo más tarde y `EWOULDBLOCK` significa que podría bloquear la aplicación.
![loop](images/Client8.png)

### Inicialización de la vista
En el método initialize de la vista, se conecta el cliente con le servidor y se crea un atributo loop el cual es un Hilo con el bucle de `_reload`, esto es para que no congele la aplicación mientras busca mensajes.
![initialize](images/Client6.png)