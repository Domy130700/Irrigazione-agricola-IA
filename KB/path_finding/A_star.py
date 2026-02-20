from KB.path_finding.libs.searchGeneric import Arc, Search_problem
import math

class IrrigationNetworkProblem(Search_problem):
    """
    Rappresenta la rete idrica come un grafo per l'algoritmo A*.
    L'obiettivo è trovare il percorso di flusso dal nodo Start al nodo Goal
    attraverso le condotte.
    """

    def __init__(self, prolog, start, goals):
        self.prolog = prolog
        self.start = start # ID nodo di partenza (es. Pompa)
        self.goals = goals # Set di ID nodi destinazione
        
        # Cache delle posizioni per velocizzare l'euristica
        self.positions = {} 
        self._cache_positions()

    def _cache_positions(self):
        """Pre-carica le coordinate dei punti per l'euristica"""
        # Cerca tutti i punti di irrigazione noti
        for atom in self.prolog.query("prop(ID, lat, Lat), prop(ID, lon, Lon)"):
            self.positions[str(atom['ID'])] = (float(atom['Lat']), float(atom['Lon']))

    def start_node(self):
        return self.start
    
    def is_goal(self, node):
        return node in self.goals

    def neighbors(self, node, seconds_from_start=0):
        """
        Trova i nodi adiacenti (connessi da una condotta).
        Sostituisce la vecchia logica stradale.
        """
        arcs = []
        
        # 1. Troviamo tutte le condotte che contengono il nodo attuale
        # La query cerca condotte dove 'node' è nella lista 'nodi_collegati'
        # Nota: In Prolog la lista è stringa o atomo, qui la gestiamo lato Python per sicurezza
        
        query = "prop(ID_Condotta, nodi_collegati, ListaNodi)"
        for soln in self.prolog.query(query):
            nodi = soln['ListaNodi'] # PySwip restituisce una lista di atomi/interi
            nodi = [str(n) for n in nodi] # Convertiamo tutto in stringa per confronto
            
            if str(node) in nodi:
                # Se il nodo è in questa condotta, i vicini sono il precedente e il successivo
                idx = nodi.index(str(node))
                
                vicini_diretti = []
                if idx > 0: vicini_diretti.append(nodi[idx-1])
                if idx < len(nodi) - 1: vicini_diretti.append(nodi[idx+1])
                
                for vicino in vicini_diretti:
                    # Calcolo costo (distanza euclidea o fittizia 1 per semplicità)
                    costo = self.calcola_distanza(node, vicino)
                    # Creiamo l'arco
                    arcs.append(Arc(node, vicino, cost=costo, action=f"Flusso verso {vicino}"))
        
        return arcs

    def calcola_distanza(self, n1, n2):
        """Calcola distanza in metri (approssimata) tra due nodi"""
        if n1 in self.positions and n2 in self.positions:
            lat1, lon1 = self.positions[n1]
            lat2, lon2 = self.positions[n2]
            # Semplice distanza euclidea su coordinate (sufficiente per A*)
            return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2) * 100000 
        return 1 # Costo default se coordinate mancanti

    def heuristic(self, node):
        """
        Stima la distanza in linea d'aria verso il goal più vicino.
        """
        min_dist = float('inf')
        if node not in self.positions:
            return 0
            
        current_pos = self.positions[node]
        
        for goal in self.goals:
            if goal in self.positions:
                goal_pos = self.positions[goal]
                dist = math.sqrt((current_pos[0]-goal_pos[0])**2 + (current_pos[1]-goal_pos[1])**2) * 100000
                if dist < min_dist:
                    min_dist = dist
        
        return min_dist if min_dist != float('inf') else 0