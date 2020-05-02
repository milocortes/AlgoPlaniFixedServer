/* Deferrable Server (DS)

El algoritmo DF mejora el tiempo de respuesta media de una solicitud aperiódica con respectp al PS. AL igual que el PS,
este algoritmo crea una tarea periódica(usualmente con alta prioridad) para servir a solicitudes aperiodicas.
Sin embargo, al contrario del PS, DS preserva su capacidad si no hay solicitudes pendientes para el servidor.
La capacidad es mantenida hasta el final de periodo, de manera que las solicitudes aperiódicas pueden ser servidas
con la misma prioridad del servidor en cualquier momento, en la medida que su capacidad ha sido consumida.
 Al inicio de cualquier periodo del servidor, su capacidad es reestablecida al máximo.
*/

#include <string>
#include<vector>
#include<algorithm>
#include <memory>
#include <functional>
#include <iostream>

#include "Ordenador.h"
#include "Tarea.h"

using namespace std;

// main del programa
int main(int argc, char const *argv[]) {

  // Ejemplo 1
  cout << "************************************************" << '\n';
  cout << "***************  EJEMPLO 1 *********************" << '\n';
  cout << "************************************************" << '\n';

  // Simularemos un recorrido de tiempo
  // Imaginemos dos tareas periódicas y una tarea servidor:

  /*
      T   C
  t1 10   4
  t2 20   8
  ts  5   1
  */

  // Imaginemos que tenemos cinco tareas aperiódicas

  /*
      R   C   T
  j1  5   1   100
  j2 12   1   200
  j3 14   2   300
  j4 20   3   400
  j5 22   1   500
  */

  // Inicializamos las tareas
  Tarea tareap1{10,4,0,"1"};
  Tarea tareap2{20,8,0,"2"};
  Tarea tareapS{5,1,0,"Servidor"};

  Tarea tareaAp1{100,1,5,"1Ap"};
  Tarea tareaAp2{200,1,12,"2Ap"};
  Tarea tareaAp3{300,2,14,"3Ap"};
  Tarea tareaAp4{400,3,20,"4Ap"};
  Tarea tareaAp5{500,1,22,"5Ap"};

  // Usaremos el algoritmo RM para ordenar las tareas
  // Instanciamos un vector con la dirección de memoria de las tareas periódicas creadas
  std::vector<Tarea *> lista_tareas{&tareap1,&tareap2,&tareapS};

  // Instanciamos un vector con la dirección de memoria de las tareas aperiódicas creadas
  std::vector<Tarea *> lista_tareas_ap{&tareaAp1,&tareaAp2,&tareaAp3,&tareaAp4,&tareaAp5};

  for (size_t i = 0; i < 50; i++) {
    if (i%5==0 && i!=0) {
       tareapS.actualizar_consumo(1);
    }
    else if (i%10==0 && i!=0) {
       tareapS.actualizar_consumo(4);
    }
    else  if (i%20==0 && i!=0) {
         tareapS.actualizar_consumo(8);
      }
    Ordenador::Periodicas(lista_tareas,i,lista_tareas_ap);
    std::cout << "**********************" << '\n';
    for_each(lista_tareas.begin(),lista_tareas.end(),[](Tarea* tarea){tarea->describe();});
  }

  return 0;
}
