### Deferrable Server (DS)
"""
El algoritmo DF mejora el tiempo de respuesta media de una solicitud aperiódica con respectp al PS. AL igual que el PS,
este algoritmo crea una tarea periódica(usualmente con alta prioridad) para servir a solicitudes aperiodicas.
Sin embargo, al contrario del PS, DS preserva su capacidad si no hay solicitudes pendientes para el servidor.
La capacidad es mantenida hasta el final de periodo, de manera que las solicitudes aperiódicas pueden ser servidas
con la misma prioridad del servidor en cualquier momento, en la medida que su capacidad ha sido consumida.
 Al inicio de cualquier periodo del servidor, su capacidad es reestablecida al máximo.
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

### Generamos una función que recibe una lista de tareas y selecciona la de menor Periodo
def elige_tarea(lista):
    minimo=min(list(map((lambda x: x.deadline),lista)))
    filtrado=list(filter((lambda x: x.deadline==minimo),lista))

    return filtrado[0]
### Generamos una clase que ordenará las tareas

class Ordenador:
    def RM(lista,tiempo,lista_ap):

        lista=[i for i in lista if i.consumo>0]

        if len(lista)>0:
            tarea=elige_tarea(lista)
            print('Tarea '+ tarea.id)

            if(tarea.id=="Servidor"):
                Servidor.RM(lista,lista_ap,tiempo,tarea)

            elif(tarea.id!="Servidor"):
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
                servidor.disminuye()

            elif(tiempo<tarea.release):
                print('La tarea aperiódica '+tarea.id +' aún no alcanza su release igual a '+ str(tarea.release))
                Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp)

        elif len(lista)==0:
            print('No hay tareas aperiódicas a ordenar')
            Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp)

### Ejemplo 5.7 de Butazzo
print('*********************************************************')
print("Ejemplo 5.7 de Butazzo")
## Simularemos un recorrido de tiempo
## Imaginemos dos tareas periódicas y una tarea servidor:

"""
    T   C
t1  4   1
t2  6   2
ts  5   2
"""

## Imaginemos que tenemos dos tareas aperiódicas

"""
    R   C   T
j1  2   2   100
j2  8   1   200
j3  12  2   300
j4  19  1   400
"""

## Usaremos el algoritmo RM para ordenar las tareas
tareap1=Tarea(4,1,0,"1")
tareap2=Tarea(6,2,0,"2")
tareapS=Tarea(5,2,0,"Servidor")

tareaAp1=Tarea(100,2,2,"1Ap")
tareaAp2=Tarea(200,1,8,"2Ap")
tareaAp3=Tarea(300,2,12,"3Ap")
tareaAp4=Tarea(400,1,19,"4Ap")

lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[tareaAp1,tareaAp2,tareaAp3,tareaAp4]

for i in range(0,25):

    if (i % 4)==0:
        tareap1=Tarea(4,1,0,"1")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 5)==0:
        tareapS=Tarea(5,2,0,"Servidor")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 6)==0:
        tareap2=Tarea(6,2,0,"2")
        lista_tareas=[tareap1,tareap2,tareapS]


    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap)


### Ejemplo 5.8 de Butazzo
print('*********************************************************')
print("### Ejemplo 5.8 de Butazzo")

## Simularemos un recorrido de tiempo
## Imaginemos dos tareas periódicas y una tarea servidor:

"""
    T   C
t1  8   2
t2 10   3
ts  6   2
"""

## Imaginemos que tenemos dos tareas aperiódicas

"""
    R   C   T
j1  5   2   100
j2  9   1   200
j3  11  2   300
j4  16  1   400
"""

## Usaremos el algoritmo RM para ordenar las tareas
tareap1=Tarea(8,2,0,"1")
tareap2=Tarea(10,3,0,"2")
tareapS=Tarea(6,2,0,"Servidor")

tareaAp1=Tarea(100,2,5,"1Ap")
tareaAp2=Tarea(200,1,9,"2Ap")
tareaAp3=Tarea(300,2,11,"3Ap")
tareaAp4=Tarea(400,1,16,"4Ap")

lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[tareaAp1,tareaAp2,tareaAp3,tareaAp4]

for i in range(0,25):

    if (i % 6)==0:
        tareapS=Tarea(6,2,0,"Servidor")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 8)==0:
        tareap1=Tarea(8,2,0,"1")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 10)==0:
        tareap2=Tarea(10,3,0,"2")
        lista_tareas=[tareap1,tareap2,tareapS]


    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap)
