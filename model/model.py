from database.DB_connect import get_connection
from model.automobile import Automobile
from model.noleggio import Noleggio

'''
    MODELLO: 
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Autonoleggio:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_automobili(self) -> list[Automobile] | None:
        """
            Funzione che legge tutte le automobili nel database
            :return: una lista con tutte le automobili presenti oppure None
        """
        # TODO
        cnx = get_connection()
        if cnx is None:
            print("oh no")
            return None
        try:
            cursor = cnx.cursor()
            query= "SELECT * FROM automobile"
            cursor.execute(query)
            auto_list:list[Automobile] =[]
            for (codice,marca,modello,anno,posti,disponibile) in cursor:
                disp_bool=bool(disponibile)
                auto_list.append(Automobile(codice, marca, modello, anno, posti, disp_bool))
            return auto_list
        except Exception as e:
            print(e)
            return None
        finally:
            cnx.close()



    def cerca_automobili_per_modello(self, modello) -> list[Automobile] | None:
        """
            Funzione che recupera una lista con tutte le automobili presenti nel database di una certa marca e modello
            :param modello: il modello dell'automobile
            :return: una lista con tutte le automobili di marca e modello indicato oppure None
        """
        # TODO
        cnx = get_connection()
        if cnx is None:
            print("oh no")
            return None

        cursor = None
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
                    SELECT codice, marca, modello, anno, posti, disponibile
                    FROM automobile
                    WHERE modello LIKE %s
                """
            pattern = f"%{modello}%"
            cursor.execute(query, (pattern,))
            rows = cursor.fetchall()
            auto_list: list[Automobile] = []
            for r in rows:
                auto_list.append(
                    Automobile(
                        r["codice"],
                        r["marca"],
                        r["modello"],
                        r["anno"],
                        r["posti"],
                        bool(r["disponibile"]),
                    )
                )

            return auto_list

        except Exception as e:
            print(e)
            return None
        finally:
            try:
                if cursor:
                    cursor.close()
            finally:
                cnx.close()
