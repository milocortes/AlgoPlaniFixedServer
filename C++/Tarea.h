#pragma once

#include <string>
#include<vector>
#include<algorithm>
#include <memory>
#include <functional>
#include <iostream>

#include "Ordenador.h"

using namespace std;

// Generamos una clase para las Tareas
struct Tarea{
  unsigned short int deadline;
  unsigned short int consumo;
  unsigned short int release;
  string id;

  // Definimos los getter
  unsigned short int getConsumo(/* arguments */) {
    return consumo;
  }

  unsigned short int getDeadline(/* arguments */) {
    return deadline;
  }
  unsigned short int getRelease(/* arguments */) {
    return release;
  }
  string getId(){
    return id;
  }

  // Definimos los métodos de la clase
  void describe() {
    std::cout << "Soy el proceso " << id <<" y me resta por consumir "<< consumo<<'\n';
  }

  void disminuye() {
    consumo-=1;
  }
  void actualizar_consumo(unsigned short int consumo_act) {
    consumo=consumo_act;
  }
};

// Generamos una función que recibe una lista de tareas y regresa un apuntador a la tarea de menor periodo

Tarea* elige_tarea(vector<Tarea *> tareas){

  // Definimos un vector que recibirá los consumos de las tareas
  vector<unsigned short int> consumos_vec;

  // Usamos for_each, que applies a function to a range of elements, para aplicar sobre el vector de tareas la expresión lambda que agrega al vector
  // consumo_vec el consumo de las tareas con push_back.
  // Usamos también the member-of-pointer operator, or arrow operator ( -> ), performs two simultaneous operations:
  //      * It dereferences a pointer.
  //      * It accesses a member of the pointed-to object.
  for_each(tareas.begin(),tareas.end(), [&consumos_vec] (Tarea* tarea){consumos_vec.push_back(tarea->getConsumo());});

  // Aquí utilizamos el deference operator *, el cual es un operador unitario que accede al objeto que el apuntador refiere.
  // Esta es la operación inversa al operador address-of. Dada una dirección, podemos obtener el objeto que reside ahí.
  // Para usar este operador, agregamos por la izquierda del apuntador el operador *
  int minimo= *min_element(consumos_vec.begin(),consumos_vec.end());

  std::vector<Tarea *> vector_filtrado;
  copy_if(tareas.begin(),tareas.end(),back_inserter(vector_filtrado),[=](Tarea* tarea){return tarea->getConsumo()==minimo;});

  return vector_filtrado[0];
}
