#pragma once
#include "Tarea.h"

#include <string>
#include<vector>
#include<algorithm>
#include <memory>
#include <functional>
#include <iostream>

using namespace std;
// Generamos una clase que ordenará las tareas
struct Ordenador{

  static void Periodicas(vector<Tarea *> lista, int tiempo, vector<Tarea *> lista_ap) {
    // Filtramos las tareas que su consumo es estrictamente mayor a cero
    lista.erase(remove_if(lista.begin(),lista.end(),[](Tarea* tarea){return tarea->consumo<=0;}),lista.end());

    if (lista.size()>0) {
      Tarea *ptrTarea=elige_tarea(lista);
      cout << "Tarea " << ptrTarea-> getId()<<'\n';

      if (ptrTarea-> getId()=="Servidor") {
        Ordenador::Servidor(lista,lista_ap,tiempo,ptrTarea);
      }
      else if (ptrTarea-> getId()!="Servidor") {
        ptrTarea->disminuye();
      }

    }
    else if (lista.size()==0) {
      cout << "No hay tareas periódicas a ordenar" << '\n';
    }
  }

  static void Servidor(vector<Tarea *> listaP, vector<Tarea *> listaAp,int tiempo,Tarea* servidor){

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

        Ordenador::Periodicas(listaP_sinServer,tiempo,listaAp);
      }
    }
    else if (listaAp.size()==0) {
      cout<<"No hay tareas aperiódicas a ordenar"<<'\n';
      // Enviamos la lista de tareas periódicas sin el Servidor
      std::vector<Tarea *> listaP_sinServer;
      copy_if(listaP.begin(),listaP.end(),back_inserter(listaP_sinServer),[=](Tarea* tarea){return tarea->getId()!="Servidor";});

      Ordenador::Periodicas(listaP_sinServer,tiempo,listaAp);
    }
  }
};
