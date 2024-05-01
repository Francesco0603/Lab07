import copy
import time

import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0
        # dizionario di tuple possibili per la ricorsione
        self._listaRicorsione = {}
        # lista di liste di tre elementi aventi la situazione nello stesso giorno delle 3 città:
        # 0 --> Genova
        # 1 --> Milano
        # 2 --> Torino
        self._listalisteCitta = [[] for i in range(15)]

    def handle_umidita_media(self, e):
        if self._mese == 0:
            self._view.create_alert("SELEZIONARE un mese!!")
            return
        totUmidity = 0
        n=0
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        for citta in ["Torino", "Milano", "Genova"]:
            for situa in self._model.situazioni:
                if situa.localita == citta and situa.data.month == self._mese:
                    totUmidity += situa.umidita
                    n += 1
            self._view.lst_result.controls.append(ft.Text(f"{citta}: {totUmidity/n}"))
            totUmidity = 0
            n = 0
        self._view.update_page()
        return

    def recursion(self, lista, listaCitta, costo, dizionarioConti, permanenza):
        flag = True
        dim = len(lista)
        costoNuovo = costo
        newDic = copy.deepcopy(dizionarioConti)
        newPerm = permanenza
        for c in self._listaRicorsione.values():
            if costo > c:
                return
        if dim == 15:
            tupla = tuple(lista)
            self._listaRicorsione[tupla] = costo
            return
        for i in range(3):
            if dizionarioConti[listaCitta[0][i].localita] == 6 :
                continue
            if len(lista) > 0 and not listaCitta[0][i].stessaCitta(lista[-1]):
                if permanenza < 3:
                    continue
                else:
                    costoNuovo += 200
                    flag = False
                    newPerm = 0
            newPerm+=1
            newDic[listaCitta[0][i].localita] += 1
            lista.append(listaCitta[0][i])
            listaCittaNuova = listaCitta[1:]
            costoNuovo += listaCitta[0][i].umidita
            if lista[0].localita == "Torino":
                pass
            self.recursion(lista, listaCittaNuova, costoNuovo, newDic, newPerm)
            lista.pop()
            newDic[listaCitta[0][i].localita] -= 1
            newPerm -= 1
            costoNuovo-= listaCitta[0][i].umidita
            if not flag:
                costoNuovo-= 200
                flag = True

    def handle_sequenza(self, e):
        self._listaRicorsione.clear()
        if self._mese == 0:
            self._view.create_alert("SELEZIONARE un mese!!")
            return
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Porco giuda se sto impazzendo:"))
        for situa in self._model.situazioni:
            if situa.data.month == self._mese:
                if situa.data.day > len(self._listalisteCitta):
                    break
                else:
                    self._listalisteCitta[situa.data.day-1].append(situa)
        x = time.time()
        self.recursion([],self._listalisteCitta,0,{"Torino":0,"Milano":0,"Genova":0},0)
        print(time.time()-x)
        print(self._listaRicorsione.values())
        for element in self._listaRicorsione.keys():
            self._view.lst_result.controls.append(ft.Text('---'))
            self._view.lst_result.controls.append(ft.Text(f"COSTO COMPLESSIVO: {self._listaRicorsione[element]}"))
            self._view.lst_result.controls.append(ft.Text('---'))
            for situa in element:
                self._view.lst_result.controls.append(ft.Text(str(situa)))
        self._view.update_page()
        return

    def read_mese(self, e):
        self._mese = int(e.control.value)

