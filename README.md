# Pregunta 1
> En qué requerimiento implementarías una cola de mensajes en una solución orientada a datos? ¿Qué lenguaje utilizarías y porque?

Pueden ser distintos casos:
- Supongamos que se necesita comunicar distintos microservicios y un requisito primordial es la disponibilidad de ellos, es decir, prácticamente no puede haber downtime, podemos utilizar una cola de mensajes para tratar estas solicitudes, recibiendo cada una y ejecutándolas con un worker que esté disponible para realizarla.

- Supongamos que tenemos un servicio que permite hacer algún procesamiento a un archivo, por ejemplo archivos de imágenes o archivos de audio, a los cuales se les puede aplicar algún filtro. Este tipo de procesos requiere del manejo de una serie de "tareas" a realizar, nuevamente podemos utilizar una cola de mensajes para procesar las tareas y dar también la respuesta que se solicita.

- El Internet de las Cosas (IoT) genera mucha información (telemetría) en muy poco tiempo, si se necesitara llevar un control de los distintos dispositivos y llevar un "logueo" de cada cosa que fue sucediendo, una cola de mensajería sería fundamental para poder tener estos resultados en tiempo real. Por ejemplo, si utilizo sensores en una máquina industrial, me gustaría saber al instante que dicha máquina está fallando y no esperar que un operario se de cuenta o que alguien tenga que darme aviso, podemos automiatizar esto llevando todo a un sistema en tiempo real.

- Continuando con el ejemplo anterior, sería vital que las transacciones que se realizan en un banco estén procesadas y, en el caso de encontrar alguna falla o algún tipo de fraude, sería fundamental que el cliente sea notificado con la menor demora posible. O prácticamente sin demora.
Básicamente podemos utilizar colas de mensajerías cuando se requiera interacción entre distintos procesos, con la posibilidad de que éstos estén desacoplados y que esta comunicación sea lo mas rápido posible, cercana a tiempo real.

Si se desea implementar una cola de mensajería "from scratch" lo haría utilizando Java ya que es un lenguaje muy potente y performante, debido a que es un lenguaje compilado.En cambio, si se quiere utilizar algunas de las herramientas existentes (RabbitMQ, Apache Kafka) sería cuestión de encontrar el cliente al lenguaje con el que más me sienta cómodo (por ejemplo python) siempre y cuando el cliente de ese lenguaje tenga la flexibilidad que se necesita. Cuando no se logra esto, sería buena idea utilizar los lenguajes con los que se desarrollaron dichas herramientas, ya que los clientes implementados en ese lenguaje normalmente tienen la mayor de las funcionalidades disponibles.

# Pregunta 2
> Qué experiencia posees sobre py spark o spark scala? Contar breves experiencias, en caso de contar experiencia con otro framework de procesamiento distribuido, dar detalles también.

No tengo experiencia formal utilizando la herramienta, solo ejemplos de uso de la misma, y tutoriales iniciales para tener el primer hands-on. Tengo las bases acerca de cómo funcionan las herramientas y también conocimientos generales sobre el ecosistema Hadoop y cómo este vino a solucionar los problemas de Big Data.

# Pregunta 3
> Qué funcionalidad podrías expandir desde el área de ingeniería de datos con una API y arquitectónicamente como lo modelarías?

Desde el área de datos se podrían implementar APIs para disponibilizar datos que son actualizados frecuentemente y también consultados.Si hablamos por ejemplo de la industria del Gaming, un juego necesita consultar en tiempo real cuáles fueron los objetos más utilizados en las últimas partidas/sesiones de juego. Esta información se procesaría como un streaming de eventos que suceden entre cada jugador y el servidor que hostea la partida. Esta información debe ser procesada por un sistema de datos, ya que se haría a gran escala, y se debe actualizar en tiempo real y disponibilizar la información. Los usuarios tienden a consultar este tipo de información ya que quieren "replicar" el uso de estos objetos en sus partidas, en pos de sacar el mejor provecho de los mismos ya que "son los objetos más usados".

Para procesar estos datos utilizaría una arquitectura como la que sigue:

1. Tendría un Hub en el cual extraigo los datos (los eventos logueados por el servidor)
2. Esta información que llega debe ser validada y normalizada para ser guardada en un almacenamiento temporal
3. Una vez validada la información se debe hacer la transformación necesaria para poder ser guardada en un Data Mart especifico para nuestro propósito
4. Este Data Mart debe disponibilizar una vista que contenga la operación a realizar, en nuestro caso, hacer una agregación para calcular los objetos más usados
5. Finalmente, este Data Mart puede ser consultado desde una API, la cual será consultada cuando un usuario quiera consultar por los objetos más usados, dentro del juego.