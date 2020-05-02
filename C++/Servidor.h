#pragma once
#include "Tarea.h"
#include "Ordenador.h"

#include <string>
#include<vector>
#include<algorithm>
#include <memory>
#include <functional>
#include <iostream>

using namespace std;

// Generamos una clase Servidor que ordenará las tareas aperiódicas
struct Servidor{
  static void RM(vector<Tarea *> listaP, vector<Tarea *> listaAp,int tiempo,Tarea* servidor){

    // Filtramos las tareas que su consumo es estrictamente mayor a cero
    listaAp.erase(remove_if(listaAp.begin(),listaAp.end(),[](Tarea* tarea){return tarea->consumo<=0;}),listaAp.end());

    // Accedemos al apuntador de la dirección de memoria
    Tarea* ptrServidor=servidor;

    if (listaAp.size()>0) {
      Tarea *ptrTarea=elige_tarea(listaAp);

      if (tiempo>=(ptrTarea->getRelease())) {
        cout << "Tarea Aperiódica " <<ptrTarea->getId()<< '\n';
        ptrTarea->disminuye();
        ptrServidor->disminuye();

      }else if (tiempo<(ptrTarea->getRelease())) {
        cout << "La tarea aperiódica " << ptrTarea->getId()<<" aún no alcanza su release igual a "<< ptrTarea->getRelease()<<'\n';
        // Enviamos la lista de tareas periódicas sin el Servidor
        std::vector<Tarea *> listaP_sinServer;
        copy_if(listaP.begin(),listaP.end(),back_inserter(listaP_sinServer),[=](Tarea* tarea){return tarea->getId()!="Servidor";});

      Ordenador::RM(listaP,tiempo,listaAp);
      }
    }
  }
};
