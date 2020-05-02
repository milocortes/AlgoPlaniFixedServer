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

### Generamos una función que calcule U

def calcula_u(lista):
    return str(sum(list(map((lambda x: x.consumo/x.deadline),lista))))

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
                data_dict.update({tiempo:tarea.id})

        elif len(lista)==0:
            print('No hay tareas periódicas a ordenar')
            data_dict.update({tiempo:'NT'})

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
                data_dict.update({tiempo:tarea.id})

            elif(tiempo<tarea.release):
                print('La tarea aperiódica '+tarea.id +' aún no alcanza su release igual a '+ str(tarea.release))
                Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp)

        elif len(lista)==0:
            print('No hay tareas aperiódicas a ordenar')
            Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp)

##### Ejemplo 1
print('*********************************************************')
print('*********************************************************')
print("Ejemplo 1")
print('*********************************************************')
print('*********************************************************')

## Simularemos un recorrido de tiempo
## Imaginemos dos tareas periódicas y una tarea servidor:

"""
    T   C
t1 10   4
t2 20   8
ts  5   1
"""

## Imaginemos que tenemos cinco tareas aperiódicas

"""
    R   C   T
j1  5   1   100
j2 12   1   200
j3 14   2   300
j4 20   3   400
j5 22   1   500
"""

## Usaremos el algoritmo RM para ordenar las tareas
tareap1=Tarea(10,4,0,"1")
tareap2=Tarea(20,8,0,"2")
tareapS=Tarea(5,1,0,"Servidor")

tareaAp1=Tarea(100,1,5,"1Ap")
tareaAp2=Tarea(200,1,12,"2Ap")
tareaAp3=Tarea(300,2,14,"3Ap")
tareaAp4=Tarea(400,3,20,"4Ap")
tareaAp5=Tarea(500,1,22,"5Ap")

lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[]

## Imprimimos U
print('U es igual a: '+ calcula_u(lista_tareas))

data_dict={}

for i in range(0,50):


    if (i % 5)==0 and (i!=0):
        tareapS=Tarea(5,1,0,"Servidor")
        lista_tareas=[tareap1,tareap2,tareapS]
        lista_tareas_ap.append(tareaAp1)
    if (i % 10)==0:
        tareap1=Tarea(10,4,0,"1")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 12)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp2)
    if (i % 14)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp3)
    if (i % 20)==0 and (i!=0):
        tareap2=Tarea(20,8,0,"2")
        lista_tareas=[tareap1,tareap2,tareapS]
        lista_tareas_ap.append(tareaAp4)
    if (i % 22)==0  and (i!=0):
        lista_tareas_ap.append(tareaAp5)


    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap), print('*********'),list(map((lambda x:x.describe()),lista_tareas))

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

data_plot=pd.DataFrame.from_dict(data_dict, orient='index',columns=['Tarea']).reset_index()

data_plot['Activa']=1
data_plot.loc[data_plot.Tarea=="NT",'Activa']=0


plt.figure(figsize=(10, 6))
sns.barplot(x="index", hue="Tarea", y="Activa", data=data_plot, dodge=False)
plt.ylim(0, 1.5)
plt.show()

##### Ejemplo 2

print('*********************************************************')
print("### Ejemplo 2")

## Simularemos un recorrido de tiempo
## Imaginemos dos tareas periódicas y una tarea servidor:

"""
    T   C
t1  5   1
t2 15   4
ts 10   5
"""

## Imaginemos que tenemos tres tareas aperiódicas

"""
    R   C   T
j1 11   1   100
j2 20   3   200
j3 25   5   300
"""

## Usaremos el algoritmo RM para ordenar las tareas
tareap1=Tarea(5,1,0,"1")
tareap2=Tarea(15,4,0,"2")
tareapS=Tarea(10,5,0,"Servidor")

tareaAp1=Tarea(100,1,11,"1Ap")
tareaAp2=Tarea(200,3,20,"2Ap")
tareaAp3=Tarea(300,5,25,"3Ap")

lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[]

## Imprimimos U
print('U es igual a: '+ calcula_u(lista_tareas))

data_dict={}

for i in range(0,25):


    if (i % 5)==0:
        tareap1=Tarea(5,1,0,"1")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 10)==0:
        tareapS=Tarea(10,5,0,"Servidor")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 11)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp1)
    if (i % 15)==0:
        tareap2=Tarea(15,4,0,"2")
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 20)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp2)
    if (i % 25)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp3)

    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap), print('*********'),list(map((lambda x:x.describe()),lista_tareas)), print('*********'),list(map((lambda x:x.describe()),lista_tareas))

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

data_plot=pd.DataFrame.from_dict(data_dict, orient='index',columns=['Tarea']).reset_index()

data_plot['Activa']=1
data_plot.loc[data_plot.Tarea=="NT",'Activa']=0


plt.figure(figsize=(10, 6))
sns.barplot(x="index", hue="Tarea", y="Activa", data=data_plot, dodge=False)
plt.ylim(0, 1.5)
plt.show()
