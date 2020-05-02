# Algoritmos de planificación con servidores de prioridad fija


Se presentan algunos algoritmos de planificación para manejar de tareas híbridas compuestas por un subconjunto de tareas periódicas complicadas y un subconjunto de tareas aperiódicas sencillas. Son tres los algoritmos presnetados, los cuales son estudiados a detalle en Butazzo(2010):

* Deferrable Server.
* Priority Exchange.
* Sporadic Server.

### Deferrable Server

El algoritmo DF mejora el tiempo de respuesta media de una solicitud aperiódica con respectp al PS. AL igual que el PS,
este algoritmo crea una tarea periódica(usualmente con alta prioridad) para servir a solicitudes aperiodicas.
Sin embargo, al contrario del PS, DS preserva su capacidad si no hay solicitudes pendientes para el servidor.
La capacidad es mantenida hasta el final de periodo, de manera que las solicitudes aperiódicas pueden ser servidas
con la misma prioridad del servidor en cualquier momento, en la medida que su capacidad ha sido consumida.
 Al inicio de cualquier periodo del servidor, su capacidad es reestablecida al máximo.

### Priority Exchange

El PS está pensado para servir a un conjunto de peticiones aperiódicas que se realizan con un conjunto de tareas periódicas complicadas.
Al contrario del DS, tiene un peor desempeño en términos de respuesta a tareas aperiódicas, pero tiene mejor desempeño a tareas periódicas.

Como el DS, PE usa un servidor periódico (usualmente de alta prioridad) para atender peticiones aperiódicas. Sin embargo, difiere
en la manera que la capacidad es preservada. Al contrario del DS, PE preserva su capacidad de alta prioridad intercambiándola por el tiempo
de ejecución de una tarea periódica de baja prioridad.

¿Cómo funciona el algoritmo? Al inicio de cada periodo, la capacidad se repone al full. Si una consulta aperiódica está pendiente y el server
está listo para la tarea de más alta prioridad, entonces la solicitud es atendida usando la capacidad disponible.
De otra manera, el Cs es cambiado por el tiempo de ejecución de una tarea periódica activa con la más alta prioridad.

### Sporadic Server

El algoritmo sporadic server permite mejorar el tiempo de respuesta promedio de una tarea aperiódica sin degradar sin degradar
la utilización del conjunto de tareas periódicas.Este algoritmo crea una tarea periódica de prioridad alta para atender las solicitudes
aperiódicas y, como el DS, preserva la capacidad del server a su nivel de prioridad más alto hasta el momento que una solicitud aperiódica ocurre.
Sin embargo, difiere del DS en la forma cómo el server repone su capacidad. Mientras que DS y PE periódicamente reponen su capacidad a su valor
máximo al inicio de cada periodo del server, SS repone su capacidad sólo después si ha sido consumido por la ejecución de una tarea aperiódica.

En términos de simplificar la descripción del método de reabastecimiento usado por SS, definimos los siguientes términos:

* $P_{exe}$: Denota el nivel de prioridad de la tarea que actualmente se está ejecutando.
* $P_s$: Denota el nivel de prioridad asociado con SS.
* $Active$: Se dice que el SS está **activo** cuando $P_{exe}$>$P$.
* $Idle$: Se dice que el SS está **ocioso** cuando $P_{exe}$<$P$.
* $RT$: Denota el **tiempo de reposición** al cual la capacidad de SS será reabastecida.
* $RA$: Denota la cantidad de reposición que será incorporada a la cantidad al tiempo $RT$.

Usando la terminología, la capacidad $C_s$ consumida por una solicitud aperiódica es reestablecida de acuerdo a la siguiente regla:

* El tiempo de reposición $RT$ se establece tan pronto como SS se hace activo y $C_s$ >0. Sea $t_A$ tal tiempo. El valor de $RT$ es definido igual
a $t_A$ m+as el periodo del server ($RT=t_A+ T_s$)
* La cantidad de reposición $RA$ ha ser hecha al tiempo $RT$, es calculada cuando SS llega a ser ocioso o $C_s$ ha sido consumida. Sea $t_I$ tal tiempo.
 El valor de $RA$ es definido como la capacidad consumida dentro del intervalo  $[t_A, t_I]$
