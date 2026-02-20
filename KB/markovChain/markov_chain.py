import numpy as np
from KB.markovChain.libs.HMM import HMM

def stimazione_stato_idrico(sequenza_osservazioni):
    """
    Input: sequenza di osservazioni dai sensori ['umidita_bassa', 'umidita_media', ...]
    Output: Stato più probabile della pianta (ottimale, stress_lieve, stress_critico)
    """

    # Stati Nascosti
    states = ['ottimale', 'stress_lieve', 'stress_critico']

    # Probabilità iniziali
    start_probs = {'ottimale': 0.6, 'stress_lieve': 0.3, 'stress_critico': 0.1}

    # Matrice di Transizione
    transitions = {
        'ottimale':       {'ottimale': 0.7, 'stress_lieve': 0.25, 'stress_critico': 0.05},
        'stress_lieve':   {'ottimale': 0.1, 'stress_lieve': 0.6,  'stress_critico': 0.3},
        'stress_critico': {'ottimale': 0.0, 'stress_lieve': 0.1,  'stress_critico': 0.9}
    }

    # Matrice di Emissione
    observations = {
        'umidita_alta':  {'ottimale': 0.8, 'stress_lieve': 0.15, 'stress_critico': 0.05},
        'umidita_media': {'ottimale': 0.15, 'stress_lieve': 0.6,  'stress_critico': 0.25},
        'umidita_bassa': {'ottimale': 0.05, 'stress_lieve': 0.25, 'stress_critico': 0.7}
    }

    # Validazione: sostituisce eventuali osservazioni non previste con 'umidita_media'
    sequenza_validata = [o if o in observations else 'umidita_media' for o in sequenza_osservazioni]

    # Creazione HMM
    hmm = HMM(states, transitions, observations, start_probs)

    # Calcolo probabilità stato finale (Filtering)
    risultato = hmm.filtering(sequenza_validata)

    # Restituisce lo stato più probabile
    return max(risultato, key=risultato.get)
