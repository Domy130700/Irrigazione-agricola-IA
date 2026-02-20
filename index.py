import os
import sys
from ontology.irrigation_parser import parse_osm_irrigation
from KB.knowledgeBase import KnowledgeBase

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("\n==============================================")
    print("       SISTEMA DI IRRIGAZIONE INTELLIGENTE    ")
    print("          Progetto ICON 2025-2026             ")
    print("==============================================\n")

    # --- FASE 1: CARICAMENTO MAPPA ---
    mappa_caricata = False
    while not mappa_caricata:
        print("CONFIGURAZIONE INIZIALE:")
        print("1. Carica e processa nuova mappa XML (campo_x.xml / map.xml)")
        print("2. Usa dati Prolog esistenti (salta parsing)")
        print("3. Esci")
        
        scelta_iniziale = input("\nSeleziona un'opzione: ")

        if scelta_iniziale == "1":
            parse_osm_irrigation()
            mappa_caricata = True
        elif scelta_iniziale == "2":
            if os.path.exists("KB/prolog/class_value/condotta.pl"):
                mappa_caricata = True
            else:
                print("❌ Errore: Nessun file Prolog trovato. Devi prima processare una mappa (Opzione 1).")
        elif scelta_iniziale == "3":
            sys.exit()
        else:
            print("Opzione non valida.")

    # --- FASE 2: INIZIALIZZAZIONE KNOWLEDGE BASE ---
    print("\nInizializzazione Base di Conoscenza in corso...")
    syncro = input("Vuoi attivare l'ottimizzazione CSP per il bilanciamento idrico? (Y/N): ")
    kb = KnowledgeBase(optimize=(syncro.upper() == "Y"))
    
    # --- FASE 3: MENU OPERATIVO ---
    while True:
        print("\n" + "="*45)
        print("             MENU OPERATIVO RETE IDRICA")
        print("="*45)
        print("1. Elenco Condotte (Tubi)")
        print("2. Elenco Punti di Irrigazione (Valvole/Sensori)")
        print("3. Calcola percorso flusso ottimale (A*)")
        print("4. Ottimizza distribuzione idrica (CSP)")
        print("5. Stima Salute Piante (Markov)")
        print("6. Predici fabbisogno idrico (Machine Learning)")
        print("7. Esci")
        print("="*45)

        opzione = input("Scegli un'operazione: ")

        if opzione == "1":
            condotte = kb.lista_condotte()
            print("\n--- ELENCO CONDOTTE ---")
            if condotte:
                print(", ".join(condotte))
            else:
                print("Nessuna condotta trovata nella KB.")

        elif opzione == "2":
            punti = kb.lista_punti_irrigazione()
            print("\n--- PUNTI DI IRRIGAZIONE RILEVATI ---")
            if punti:
                for p in punti:
                    info = kb.get_dati_punto(p['id'])
                    print(f"ID: {p['id']} | Tipo: {info['valvola']} | Collegato a: {', '.join(p['condotte'])}")
            else:
                print("Nessun punto di irrigazione trovato.")

        elif opzione == "3":
            print("\n--- RICERCA PERCORSO FLUSSO (A*) ---")
            n_inizio = input("ID Punto di Origine (es. serbatoio): ")
            n_fine = input("ID Punto di Destinazione (es. valvola_settore): ")
            
            percorso, tempo = kb.ricerca_percorso(n_inizio, n_fine)
            if percorso:
                print(f"\n✅ Percorso trovato in {tempo:.4f} secondi:")
                print(" -> ".join(percorso))
            else:
                print("\n❌ Impossibile trovare un collegamento idrico tra i punti specificati.")

        elif opzione == "4":
            print("\n--- OTTIMIZZAZIONE CSP (BILANCIAMENTO PRESSIONE) ---")
            soluzione = kb.ottimizza_distribuzione_idrica()
            if soluzione:
                print("Configurazione ottimale dei litri per settore:")
                for campo, litri in soluzione.items():
                    print(f" - {campo}: {litri} Litri")
            else:
                print("Nessuna soluzione trovata per i vincoli attuali.")

        elif opzione == "5":
            print("\n--- STIMA STATO IDRICO (MARKOV) ---")
            sequenza = [2, 1, 0, 0]
            stato = kb.stima_salute_pianta(sequenza)
            print(f"Lo stato di salute stimato per il settore è: {stato.upper()}")

        elif opzione == "6":
            print("\n--- PREDIZIONE FABBISOGNO (ML) ---")
            try:
                print("Inserisci dati sensore per la predizione:")
                moist = float(input("Umidità normalizzata (0-1): "))
                temp = float(input("Temperatura normalizzata (0-1): "))

                pred = kb.calcola_fabbisogno_idrico([1, 1, moist, temp, 12, 6])

                # 🔥 CONVERSIONE DEFINITIVA SICURA
                pred = float(pred)

                print(f"\n💧 Acqua consigliata: {pred:.2f} Litri")

            except Exception as e:
                print(f"Errore durante la predizione: {e}")

        elif opzione == "7":
            print("\nSpegnimento sistema.")
            break
        
        else:
            print("\nOpzione non valida, riprova.")

if __name__ == "__main__":
    main()
