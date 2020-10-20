    #no_more_bytes = False
    #while(no_more_bytes == False):
    #    aux2 = sock.recv(1)
    #    if(type(aux2) != type(example)):
    #        no_more_bytes = True
    #        next_challenge = sock.recv(1024)
        
    #print(next_challenge.decode())



---------------------------------------------------------------------------------------------------------------------------------------------

https://docs.python.org/2/library/struct.html

--------------------------------------------------------------------------------------------------------------------------------------------

En el reto 5 el del WYP, se dice que usando las funciones aportadas en el enunciado y da como pista que se debe usar struct, y que se debe aplicar RFC1071 checksum

No se me ha quedado completamente claro que es lo que se debe hacer en este reto, ¿qué se debería de hacer en este reto?

--------------------------------------------------------------------------------------------------------------------------------------------

Hola, mi duda es la siguiente. Una vez has hecho el struct con el header y el payload (yo lo hago con formato '10s16s', no se si está bien), le envío lo resultante al servidor, y este me responde con otro mensaje tipo "WYP....", por lo que supongo que tenemos que usar unpack() para leerlo. 

Intento usar unpack así: mensaje = struct.unpack('10s16s', respuesta), pero me da el siguiente error: 

"struct.error: unpack requires a buffer of 26 bytes"

¿Alguna sugerencia?

Gracias

--------------------------------------------------------------------------------------------------------------------------------------------

Hola Rubén:

Efectivamente el servidor contesta usando el mismo protocolo. Piensa otra vez en el formato, ese "10s16s" no tiene buena pinta.

Saludos

---------------------------------------------------------------------------------------------------------------------------------------------

Gracias por la respuesta David. Probé a calcular el checksum de lo que enviaba con mi formato y no me salía a 0, así que como me decías, el formato estaba mal. Al final creo que lo he sacado porque ahora si me da 0 el checksum cuando lo vuelvo a calcular.

Pero sigo teniendo el problema de que unpack() me pide un buffer, ahora de 44 bytes: "struct.error: unpack requires a buffer of 44 bytes"

Estoy usándolo así: 

respuesta = sockServer.recv(1024)

print(struct.unpack(formato, respuesta))

Lo mismo pasa si en vez de imprimirlo lo guardo en una variable.

¿Alguna idea o consejo?

Gracias, un saludo

----------------------------------------------------------------------------------------------------------------------------------------------

Hola Ramón, respecto a tu formato, yo creo que sería '!3sBHH', porque los bytes de los tres últimos campos son 1-2-2, y además faltaría añadir al formato al final el campo del payload, que yo lo he sacado contando los caracteres que tiene. Así me llega a dar 0 el "recálculo" del checksum, pero no se si esto garantiza que esté bien.

Respecto al unpack y el buffer, todavía no se como hacerlo.

Un saludo

-----------------------------------------------------------------------------------------------------------------------------------------------

Ese formato sigue sin ser del todo correcto. Revisad el formato, quizá os ayude pensarlo desde 0. Mirad bien en las equivalencias para construir el formato que vosotros necesitáis. Ir aislando caso por caso.

Un saludo!

------------------------------------------------------------------------------------------------------------------------------------------------

Entonces si el formato de unpack() es correcto, se solucionaría el error del buffer? o es independiente?

------------------------------------------------------------------------------------------------------------------------------------------------

Vale, ya lo he conseguido. Por si a alguien le pasa lo mismo, para resolver el tamaño del buffer me ha servido utilizar las funciones "struct.calcsize()" y "len()" para ajustar el tamaño del formato de unpack al del mensaje que recibes.

Un saludo

-------------------------------------------------------------------------------------------------------------------------------------------------

Genial Rubén, gracias por compartir.

Sí, la función len la podemos usar para conocer el tamaño. Los formatos que compartíais eran incorrectos como os decía y era uno de los problemas.

Un saludo!