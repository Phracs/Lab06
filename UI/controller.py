import flet as ft
from mysql.connector.constants import flag_is_set

from UI.view import View
from model.model import Autonoleggio

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view : View, model : Autonoleggio):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    # TODO
    def mostra_automobili(self, e):
        auto_list=self._model.get_automobili()
        self._view.lista_auto.controls.clear()
        for auto in auto_list:
            self._view.lista_auto.controls.append(
                ft.Text(str(auto))
            )
        self._view.update()

    def cerca_automobili(self, e):
        modello= self._view.input_modello_auto.value.strip()
        if not modello:
            self._view.show_alert("Inserisci il modello dell'auto")
            return
        risultati = self._model.cerca_automobili_per_modello(modello)
        if risultati is None:
            self._view.lista_auto_ricerca.controls.clear()
            self._view.lista_auto_ricerca.controls.append(
                ft.Text("Errore di connessione o query. Riprova.")
            )
            self._view.update()
            return
        self._view.lista_auto_ricerca.controls.clear()
        if len(risultati) == 0:
            self._view.lista_auto_ricerca.controls.append(
            ft.Text(f"Nessuna automobile trovata per: '{modello}'.")
            )
        else:
            for auto in risultati:
                self._view.lista_auto_ricerca.controls.append(ft.Text(str(auto)))
            self._view.update()