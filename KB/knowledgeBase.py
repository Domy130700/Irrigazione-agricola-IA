import copy
import time
import pickle
import numpy as np
import warnings
from pyswip import Prolog

# Sopprime warning sklearn (versioni diverse modelli)
warnings.filterwarnings("ignore", category=UserWarning)

# Import moduli sistema
from KB.path_finding.A_star import IrrigationNetworkProblem 
from KB.path_finding.libs.searchGeneric import AStarsearch
from KB.markovChain.markov_chain import stimazione_stato_idrico
from KB.CSP.CSP import SolveIrrigationCSP


class KnowledgeBase():
    def __init__(self, optimize=True):
        """
        Inizializza il sistema di controllo della rete idrica.
        """
        self.prolog = Prolog()
        self.optimize = optimize

        # PULIZIA COMPLETA PRIMA DI CARICARE I FILE
        try:
            list(self.prolog.query("abolish(prop/3)"))
        except:
            pass

        # Caricamento file Prolog (una sola volta)
        try:
            self.prolog.consult("KB/prolog/knowledge_base.pl")
            self.prolog.consult("KB/prolog/class_value/condotta.pl")
            self.prolog.consult("KB/prolog/class_value/punto_irrigazione.pl")
        except Exception as e:
            print(f"⚠️ Errore caricamento file Prolog. Esegui prima il parser! Error: {e}")

        # Caricamento modelli Machine Learning
        try:
            with open('supervised_learning/models/knn.sav', 'rb') as f:
                self.model_knn = pickle.load(f)

            with open('supervised_learning/models/tree_regression.sav', 'rb') as f:
                self.model_tree = pickle.load(f)

            with open('supervised_learning/models/scaler_knn.sav', 'rb') as f:
                self.scaler = pickle.load(f)

        except FileNotFoundError:
            print("⚠️ Modelli ML non trovati. Esegui prima i file di training in supervised_learning/.")
            self.model_knn = None
            self.model_tree = None
            self.scaler = None

    # ============================================================
    # 🔹 PROLOG QUERY
    # ============================================================

    def lista_condotte(self):
        condotte = []
        atoms = list(self.prolog.query("prop(ID, tipo, condotta)"))
        for atom in atoms:
            condotte.append(str(atom["ID"]))
        return condotte

    def lista_punti_irrigazione(self):
        """
        Restituisce i nodi della rete idrica, senza duplicati.
        """
        punti = []
        seen = set()
        atoms = list(self.prolog.query("prop(ID, tipo, punto_irrigazione)"))
        for atom in atoms:
            id_punto = str(atom["ID"])
            if id_punto in seen:
                continue
            seen.add(id_punto)

            query_info = f"prop({id_punto}, condotte_attestate, C)"
            infos = list(self.prolog.query(query_info))
            condotte = []
            for info in infos:
                condotte.extend([str(c) for c in info["C"]])
            punti.append({"id": id_punto, "condotte": list(set(condotte))})
        return punti

    def get_dati_punto(self, id_punto):
        info = {"valvola": "Assente"}
        res = list(self.prolog.query(
            f"prop({id_punto}, lat, Lat), "
            f"prop({id_punto}, lon, Lon), "
            f"prop({id_punto}, dispositivo_controllo, V)"
        ))

        if res:
            info["lat"] = res[0]["Lat"]
            info["lon"] = res[0]["Lon"]
            info["valvola"] = (
                "Presente (Elettrovalvola)"
                if str(res[0]["V"]) == "1"
                else "Assente (Snodo/Sensore)"
            )
        return info

    # ============================================================
    # 🔹 A* PATH FINDING
    # ============================================================

    def ricerca_percorso(self, start_node, end_node):
        problem = IrrigationNetworkProblem(self.prolog, start_node, {end_node})
        start_time = time.time()
        path = AStarsearch(problem)
        end_time = time.time()
        if path:
            return path.nodes(), (end_time - start_time)
        return [], 0

    # ============================================================
    # 🔹 MACHINE LEARNING
    # ============================================================

    def calcola_fabbisogno_idrico(self, dati_sensore):
        """
        Predice i litri d’acqua necessari.
        """
        if self.scaler is None or self.model_knn is None:
            raise RuntimeError("Modelli ML non caricati correttamente.")

        n_features_model = getattr(self.scaler, "n_features_in_", None)
        if n_features_model is None:
            raise RuntimeError("Scaler non addestrato correttamente.")

        # Se troppe feature → taglia
        if len(dati_sensore) > n_features_model:
            dati_sensore = dati_sensore[:n_features_model]

        # Se poche feature → errore chiaro
        if len(dati_sensore) < n_features_model:
            raise ValueError(
                f"Il modello richiede {n_features_model} feature, "
                f"ma ne hai fornite {len(dati_sensore)}."
            )

        dati_input = np.array(dati_sensore).reshape(1, -1)
        dati_scaled = self.scaler.transform(dati_input)
        pred_knn = self.model_knn.predict(dati_scaled)
        return float(pred_knn[0])

    # ============================================================
    # 🔹 MARKOV (HMM)
    # ============================================================

    def stima_salute_pianta(self, sequenza_umidita):
        return stimazione_stato_idrico(sequenza_umidita)

    # ============================================================
    # 🔹 CSP
    # ============================================================

    def ottimizza_distribuzione_idrica(self):
        solver = SolveIrrigationCSP(self.prolog)
        soluzione = solver.solveCSP()
        return soluzione
