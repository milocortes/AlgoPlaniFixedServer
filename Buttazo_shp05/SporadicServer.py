### Sporadic Server (SS)
"""
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
"""

### Generamos una clase para las Tareas

class Tarea:

    def __init__(self,deadline, consumo,release,id):
        self.deadline=deadline
        self.consumo=consumo
        self.release=release
        self.id=id

    def describe(self):
        print("Soy la tarea "+ self.id+ " y me resta por consumir "+ str(self.consumo))

    def disminuye(self):
        self.consumo-= 1

    def actualizar_consumo(self,consumo):
        self.consumo=consumo


### Generamos una clase para el Servidor de Sporadic Server

class ServidorSS:

    def __init__(self,deadline, consumo,release,id,estado,RT,RA):
        self.deadline=deadline
        self.consumo=consumo
        self.release=release
        self.id=id
        self.estado=estado
        self.RT=RT
        self.RA=RA

    def describe(self):
        print("Soy la tarea "+ self.id+ " y me resta por consumir "+ str(self.consumo)+". Estado del Server: "+ str(self.estado)+". Mi tiempo de reposición es "+str(self.RT)+" y la cantidad a reponer es "+str(self.RA))

    def disminuye(self):
        self.consumo-= 1

    def activa(self):
        self.estado=True

    def desactiva(self):
        self.estado=False

    def actualizar_consumo(self,consumo):
        self.consumo+=consumo

    def aumenta_RA(self):
        self.RA+=1

    def vacia_RA(self):
        self.RA=0

### Generamos una función que recibe una lista de tareas y selecciona la de menor Periodo

def elige_tarea(lista):
    minimo=min(list(map((lambda x: x.deadline),lista)))
    filtrado=list(filter((lambda x: x.deadline==minimo),lista))

    return filtrado[0]

### Generamos una función que recibe una lista de tareas y selecciona al ServidorSS

#def elige_servidor(lista):
#    filtrado=list(filter((lambda x: x.id=="Servidor"),lista))

#    return filtrado[0]

### Generamos una clase que ordenará las tareas

class Ordenador:
    def RM(lista,tiempo,lista_ap,servidor):

       ## print(sporadic_dict)
        if(sporadic_dict!={}):
            RT=next(iter(sporadic_dict))
            if(tiempo==RT):
                servidor.actualizar_consumo(sporadic_dict[RT])
                sporadic_dict.pop(RT)

        lista=[i for i in lista if i.consumo>0]

        if len(lista)>0:
            tarea=elige_tarea(lista)
            print('Tarea '+ tarea.id)

            if(tarea.id=="Servidor"):
                Servidor.RM(lista,lista_ap,tiempo,tarea)

            elif(tarea.id!="Servidor"):
                if(tarea.deadline<servidor.deadline):
                    estadoServerSS=servidor.estado
                    servidor.activa()
                    if(estadoServerSS!=servidor.estado):
                        servidor.RT=tiempo+servidor.deadline
                        servidor.vacia_RA()
                        sporadic_dict.update( {servidor.RT : servidor.RA})

                elif(tarea.deadline>servidor.deadline):
                    servidor.desactiva()
                tarea.disminuye()

        elif len(lista)==0:
            print('No hay tareas periódicas a ordenar')

### Generamos una clase Servidor que ordenará las tareas aperiódicas

class Servidor:
    def RM(listaP,listaAp,tiempo,servidor):


        lista=[i for i in listaAp if i.consumo>0]

        if len(lista)>0:
            tarea=elige_tarea(lista)

            if (tiempo>=tarea.release) :
                print('Tarea Aperiódica'+tarea.id)
                tarea.disminuye()
                estadoServerSS=servidor.estado
                servidor.activa()
                if(estadoServerSS!=servidor.estado):
                    servidor.RT=tiempo+servidor.deadline
                    servidor.vacia_RA()
                    sporadic_dict.update( {servidor.RT : servidor.RA} )

                servidor.disminuye()
                servidor.aumenta_RA()
                sporadic_dict.update({servidor.RT:servidor.RA})


            elif(tiempo<tarea.release):
                print('La tarea aperiódica '+tarea.id +' aún no alcanza su release igual a '+ str(tarea.release))
                servidor.desactiva()
                Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp,servidor)

        elif len(lista)==0:
            print('No hay tareas aperiódicas a ordenar')
            servidor.desactiva()
            Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp,servidor)


### Ejemplo 5.17 de Butazzo
print('*********************************************************')
print("Ejemplo 5.17 de Butazzo")

## Simularemos un recorrido de tiempo
## Imaginemos dos tareas periódicas y una tarea servidor:

"""
    T   C
t1  5   1
t2 15   4
ts 10   5
"""

## Imaginemos que tenemos dos tareas aperiódicas

"""
    R   C   T
j1  4   2   100
j2  8   2   200
"""

## Usaremos el algoritmo RM para ordenar las tareas
tareap1=Tarea(5,1,0,"1")
tareap2=Tarea(15,4,0,"2")
tareapS=ServidorSS(10,5,0,"Servidor",False,0,0)

tareaAp1=Tarea(100,2,4,"1Ap")
tareaAp2=Tarea(200,2,8,"2Ap")

lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[tareaAp1,tareaAp2]

## Creamos un diccionario para ir guardando los valores de RT y RA
sporadic_dict ={}

for i in range(0,40):

    if (i % 5)==0:
        tareap1.actualizar_consumo(1)
        lista_tareas=[tareap1,tareap2,tareapS]

    if (i % 15)==0:
        tareap2.actualizar_consumo(4)
        lista_tareas=[tareap1,tareap2,tareapS]


    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap,tareapS), print('*********'),list(map((lambda x:x.describe()),lista_tareas))

### Ejemplo 5.18 de Butazzo
print('*********************************************************')
print("Ejemplo 5.18 de Butazzo")

## Simularemos un recorrido de tiempo
## Imaginemos dos tareas periódicas y una tarea servidor:

"""
    T   C
t1 10   3
t2 15   4
ts  8   2
"""

## Imaginemos que tenemos dos tareas aperiódicas

"""
    R   C   T
j1  2   2   100
j2  7   2   200
"""

## Usaremos el algoritmo RM para ordenar las tareas
tareap1=Tarea(10,3,0,"1")
tareap2=Tarea(15,4,0,"2")
tareapS=ServidorSS(8,2,0,"Servidor",False,0,0)

tareaAp1=Tarea(100,2,2,"1Ap")
tareaAp2=Tarea(200,2,7,"2Ap")

lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[tareaAp1,tareaAp2]

## Creamos un diccionario para ir guardando los valores de RT y RA
sporadic_dict ={}

for i in range(0,40):

    if (i % 10)==0:
        tareap1.actualizar_consumo(3)
        lista_tareas=[tareap1,tareap2,tareapS]

    if (i % 15)==0:
        tareap2.actualizar_consumo(4)
        lista_tareas=[tareap1,tareap2,tareapS]


    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap,tareapS), print('*********'),list(map((lambda x:x.describe()),lista_tareas))
