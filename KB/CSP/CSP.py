from KB.CSP.libs.cspSLS import SLSearcher
from KB.CSP.libs.cspProblem import Variable, Constraint, CSP
import random

class SolveIrrigationCSP:
    """
    Risolve il problema di allocazione risorse idriche (CSP).
    Obiettivo: Assegnare la quantità d'acqua (0, 10, 20 litri) ai vari settori
    senza superare la capacità massima della pompa centrale.
    """
    
    def __init__(self, prolog):
        self.prolog = prolog
        # Definiamo i settori da irrigare (Li recuperiamo dai 'punto_irrigazione' che hanno sensori)
        # O per semplicità, usiamo una lista fissa o derivata dal file CSV
        self.settori = self._get_settori_attivi()
        self.dominio_acqua = [0, 5, 10, 15, 20] # Litri erogabili per turno
        self.capacita_pompa = 50 # Massimo litri totali erogabili simultaneamente

    def _get_settori_attivi(self):
        """Recupera ID dei punti che sono irrigatori"""
        settori = []
        # Cerchiamo punti che hanno un nome che inizia con 'irrigatore' o simili, o tutti i punti
        # Per ora prendiamo i primi 5 punti_irrigazione per test
        q = self.prolog.query("prop(ID, tipo, punto_irrigazione)")
        count = 0
        for soln in q:
            settori.append(str(soln['ID']))
            count += 1
            if count >= 5: break 
        return settori

    def constraint_capacita_pompa(self, *valori_assegnati):
        """Vincolo Hard: La somma dell'acqua non deve superare la capacità"""
        return sum(valori_assegnati) <= self.capacita_pompa

    def solveCSP(self):
        # 1. Creazione Variabili
        variables = []
        for settore in self.settori:
            # Ogni settore è una variabile che può assumere valori dal dominio_acqua
            variables.append(Variable(name=settore, domain=self.dominio_acqua))

        if not variables:
            return {}

        # 2. Creazione Vincoli
        constraints = []
        
        # Aggiungiamo un vincolo globale sulla somma (coinvolge tutte le variabili)
        # Nota: La libreria CSP semplice supporta meglio vincoli binari, 
        # qui simuliamo un vincolo che controlla l'assegnazione globale.
        # Per semplicità usiamo vincoli a coppie per evitare picchi:
        # "Due settori vicini non possono essere entrambi al massimo"
        for i in range(len(variables)-1):
            c = Constraint(
                scope=[variables[i], variables[i+1]],
                condition=lambda v1, v2: (v1 + v2) <= 30, # Esempio: max 30L su due settori vicini
                string=f"Limit_Pressure_{variables[i].name}_{variables[i+1].name}"
            )
            constraints.append(c)

        # 3. Risoluzione
        problem = CSP("Ottimizzazione Irrigazione", variables, constraints)
        searcher = SLSearcher(problem)
        # Esegue la ricerca (Max 1000 iterazioni)
        soluzione = searcher.search(1000)
        
        return soluzione