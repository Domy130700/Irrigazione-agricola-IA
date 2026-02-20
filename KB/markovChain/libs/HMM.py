import random
from .display import Displayable


class HMM(Displayable):
    def __init__(self, states, trans, pobs, start_probs):
        self.states = states
        self.trans = trans  # trans[s1][s2]
        self.pobs = pobs    # pobs[obs][state]
        self.start_probs = start_probs

    def filtering(self, obs_sequence):
        """
        Calcola la probabilità degli stati data una sequenza di osservazioni.
        Gestisce automaticamente osservazioni non presenti in pobs.
        """
        prob_dist = self.start_probs.copy()

        for obs in obs_sequence:
            new_dist = {s: 0 for s in self.states}
            for s_curr in self.states:
                # Predizione
                p_prev = sum(prob_dist[s_prev] * self.trans[s_prev][s_curr] for s_prev in self.states)

                # Aggiornamento con osservazione: fallback se obs non presente
                obs_probs = self.pobs.get(obs)
                if obs_probs is None:
                    # Osservazione sconosciuta → distribuzione uniforme
                    fallback_prob = 1.0 / len(self.states)
                    new_dist[s_curr] = p_prev * fallback_prob
                else:
                    # Normal case
                    new_dist[s_curr] = obs_probs.get(s_curr, 1e-6) * p_prev

            # Normalizzazione
            norm = sum(new_dist.values())
            if norm == 0:
                # Evita divisione per zero
                prob_dist = {s: 1.0/len(self.states) for s in self.states}
            else:
                prob_dist = {s: v/norm for s, v in new_dist.items()}

        return prob_dist
