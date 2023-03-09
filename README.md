# CyLIProject

## ¿Qué es esto?
Este es un proyecto para la materia de Comunicaciones y Laboratorio I de la Universidad de antioquia.
centrado en el tema de programación con sockets TCP o UPD.

Para esto se eligio el leguaje de python ya que tiene una libreria para trabajar con sockets muy fácil de aprender.

## ¿Cómo descargarlo?
Clonar este repositorio en la carpeta que desees.

## ¿Cómo se utiliza?
### En el mismo computador
Para usarlo en la misma máquina solo hay que entrar en la carpeta principal del repositorio y ejecutar el servidor con el siguiente comando:
~~~ bash
python server/main.py

# o también
python3 server/main.py
~~~

Luego de tener el servidor escuchando, hay que abrir los clientes. Para abrir un cliente se usa el siguiente comando.
~~~ bash
python client/main.py
~~~

### En LAN
Para que cualquier computador de la red lo pueda usar, se usan los mismos comandos pero con 2 argumentos extra

~~~ bash
# Para el servidor
python server/main.py <IP Address> <Port>

# Para los clientes
python client/main.py <IP Address> <Port>
~~~

donde `<IP Address>` es la direccion IP y `<Port>` el puerto en los que el servidor va a escuchar a los clientes.

## ¿Cómo se hizo?
Ir al archivo [Developer Manual](developer_manual.md)

## Fuentes
- [Sockets with Python 3](https://www.youtube.com/watch?v=Lbfe3-v7yE0&list=PLQVvvaa0QuDdzLB_0JSTTcl8E8jsJLhR5)
- [HOW TO - programación con sockets](https://docs.python.org/es/3/howto/sockets.html)
- [Documentación Python](https://docs.python.org/3/library/socket.html)
- [IBM](https://www.ibm.com/support/pages/why-does-send-return-eagain-ewouldblock)
