### Priority Exchange (PE)
"""
El PS está pensado para servir a un conjunto de peticiones aperiódicas que se realizan con un conjunto de tareas periódicas complicadas.
Al contrario del DS, tiene un peor desempeño en términos de respuesta a tareas aperiódicas, pero tiene mejor desempeño a tareas periódicas.

Como el DS, PE usa un servidor periódico (usualmente de alta prioridad) para atender peticiones aperiódicas. Sin embargo, difiere
en la manera que la capacidad es preservada. Al contrario del DS, PE preserva su capacidad de alta prioridad intercambiándola por el tiempo
de ejecución de una tarea periódica de baja prioridad.

¿Cómo funciona el algoritmo? Al inicio de cada periodo, la capacidad se repone al full. Si una consulta aperiódica está pendiente y el server
está listo para la tarea de más alta prioridad, entonces la solicitud es atendida usando la capacidad disponible.
De otra manera, el Cs es cambiado por el tiempo de ejecución de una tarea periódica activa con la más alta prioridad.
"""

### Generamos una clase para las Tareas

class Tarea:

    def __init__(self,deadline, consumo,release,id,budgetps):
        self.deadline=deadline
        self.consumo=consumo
        self.release=release
        self.id=id
        self.budgetps=budgetps

    def describe(self):
        print("Soy la tarea "+ self.id+ " y me resta por consumir "+ str(self.consumo)+' y tengo un budget de '+ str(self.budgetps))

    def disminuye(self):
        self.consumo-= 1

    def vaciar_servidor(self):
        self.consumo=0

    def transferir_servidor(self):
        budget=self.consumo
        self.vaciar_servidor()
        return budget

    def vaciar(self):
        self.budgetps=0

    def transferir(self):
        budgetps=self.budgetps
        self.vaciar()
        return budgetps

    def acumular(self,budget_trans):
        self.budgetps+=budget_trans

    def actualizar_consumo(self,consumo):
        self.consumo=consumo

    def disminuye_budget(self):
        self.budgetps-=1

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
    def RM(lista,tiempo,lista_ap,budget_ord):
        lista=[i for i in lista if ((i.consumo>0) or (i.budgetps>0))]
        if len(lista)>0:
            tarea=elige_tarea(lista)
            print('Tarea '+ tarea.id)

            if(tarea.id=="Servidor"):
                Servidor.RM(lista,lista_ap,tiempo,tarea)
            elif(tarea.id!="Servidor"):
                tarea.acumular(budget_ord)

                ### Comparamos si la tarea aperiódica ya está lista a ejecutarse. Si es así, utilizamos el
                ### budget acumulado de la tarea periódica para satisfacer la solicitud aperiódica

                PE.intercambio(tarea,lista_ap,tiempo)


                ### Transferimos el presupuesto a la tarea periódica con la siguiente mayor prioridad
                if(tarea.consumo==0):
                    lista_transferencia=[i for i in lista if i.id!=tarea.id]

                    if len(lista_transferencia)>0:
                        tarea_pe=elige_tarea(lista_transferencia)
                        budget_pe=tarea.transferir()
                        tarea_pe.acumular(budget_pe)
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
                budget_tr=servidor.transferir_servidor()
                Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp,budget_tr)
        elif len(lista)==0:
            print('No hay tareas aperiódicas a ordenar')
            budget_tr=servidor.transferir_servidor()
            Ordenador.RM([i for i in listaP if i.id!="Servidor"],tiempo,listaAp,budget_tr)

class PE:
    def intercambio(tarea, listaAp,tiempo):
        lista=[i for i in listaAp if i.consumo>0]
        if (len(lista)>0) & (tarea.budgetps>0):
            tarea_pe=elige_tarea(lista)
            if (tiempo>=tarea_pe.release) :
                print('Tarea Aperiódica'+tarea_pe.id)
                tarea_pe.disminuye()
                tarea.disminuye_budget()
                data_dict.update({tiempo:tarea_pe.id})
            elif(tiempo<tarea_pe.release):
                print('La tarea aperiódica '+tarea_pe.id +' aún no alcanza su release igual a '+ str(tarea_pe.release))
                tarea.disminuye()
                data_dict.update({tiempo:tarea.id})
        elif (len(lista)==0) or (tarea.budgetps==0):
            print('No hay tareas aperiódicas a ordenar')
            if(tarea.consumo>0):
                tarea.disminuye()
                data_dict.update({tiempo:tarea.id})



##### Ejemplo 1
print('*********************************************************')
print('*********************************************************')
print("1")
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
tareap1=Tarea(10,4,0,"1",0)
tareap2=Tarea(20,8,0,"2",0)
tareapS=Tarea(5,1,0,"Servidor",0)

tareaAp1=Tarea(100,1,5,"1Ap",0)
tareaAp2=Tarea(200,1,12,"2Ap",0)
tareaAp3=Tarea(300,2,14,"3Ap",0)
tareaAp4=Tarea(400,3,20,"4Ap",0)
tareaAp5=Tarea(500,1,22,"5Ap",0)

lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[]

## Imprimimos U
print('U es igual a: '+ calcula_u(lista_tareas))

data_dict={}

for i in range(0,50):

    if (i % 5)==0 and (i!=0):
        tareapS=Tarea(5,1,0,"Servidor",0)
        lista_tareas=[tareap1,tareap2,tareapS]
        lista_tareas_ap.append(tareaAp1)
    if (i % 10)==0:
        tareap1=Tarea(10,4,0,"1",0)
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 12)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp2)
    if (i % 14)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp3)
    if (i % 20)==0 and (i!=0):
        tareap2=Tarea(20,8,0,"2",0)
        lista_tareas=[tareap1,tareap2,tareapS]
        lista_tareas_ap.append(tareaAp4)
    if (i % 22)==0  and (i!=0):
        lista_tareas_ap.append(tareaAp5)

    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap,0), print('*********'),list(map((lambda x:x.describe()),lista_tareas))

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
print('*********************************************************')
print("### Ejemplo 2")
print('*********************************************************')
print('*********************************************************')

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
tareap1=Tarea(5,1,0,"1",0)
tareap2=Tarea(15,4,0,"2",0)
tareapS=Tarea(10,5,0,"Servidor",0)

tareaAp1=Tarea(100,1,11,"1Ap",0)
tareaAp2=Tarea(200,3,20,"2Ap",0)
tareaAp3=Tarea(300,5,25,"3Ap",0)


lista_tareas=[tareap1,tareap2,tareapS]
lista_tareas_ap=[]

## Imprimimos U
print('U es igual a: '+ calcula_u(lista_tareas))

data_dict={}

for i in range(0,50):

    if (i % 5)==0:
        tareap1=Tarea(5,1,0,"1",0)
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 10)==0:
        tareapS=Tarea(10,5,0,"Servidor",0)
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 11)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp1)
    if (i % 15)==0:
        tareap2=Tarea(15,4,0,"2",0)
        lista_tareas=[tareap1,tareap2,tareapS]
    if (i % 20)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp2)
    if (i % 25)==0 and (i!=0):
        lista_tareas_ap.append(tareaAp3)


    print(i), Ordenador.RM(lista_tareas,i,lista_tareas_ap,0), print('*********'),list(map((lambda x:x.describe()),lista_tareas))

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
