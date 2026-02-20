# Irrigazione Intelligente
**De Palma Domenico (mat. 726970)**

# Installazione
Installare SWI Prolog in base al sistema operativo in uso (**scaricare la versione 8**):

`https://www.swi-prolog.org/download/stable?show=all`

Posizionarsi all'interno della root principale:

`cd Irrigazione-agricola-IA-main`

Creare l'ambiente virtuale (facoltativo):

`python -m venv venv`

Installare le dipendenze:

`pip install -r requirements.txt`

# Guida all'utilizzo
## Caricamento file
Il programma, una volta avviato, chiede all'utente quale tipo di dati utilizzare. La scelta può essere tra le seguenti opzioni:

- Utilizzare un file pre-caricato sulla piattaforma (consigliato per comodità e velocità di elaborazione)

- Caricare un file XML, opzione per caricare un file dal proprio dispositivo. Il file deve avere la struttura standard OSM (OpenStreetMap) XML per un utilizzo corretto del programma. In pratica, i dati presenti nel file dovranno rispettare un formato preciso, per essere elaborati correttamente dal programma.

## Ottimizzazione globale (CSP)
Una volta caricato il file, il programma chiederà se si desidera ottimizzare la distribuzione idrica in modo globale, per bilanciare la pressione ed evitare conflitti di erogazione tra i settori della zona in esame.

## Opzioni principali
Il menu verrà poi sostituito con le seguenti opzioni:

- **Elenco Condotte (Tubi)**, restituisce tutte le tubature della rete idrica caricate dal file.

- **Elenco Punti di Irrigazione (Valvole/Sensori)**, restituisce informazioni su tutti i componenti attivi presenti nella zona.

- **Calcola percorso flusso ottimale A***, prende in input un punto di origine e uno di destinazione e restituisce il percorso più efficiente per l'acqua.

- **Ottimizza distribuzione idrica (CSP)**, permette di ricalcolare l'allocazione delle risorse per bilanciare la pressione.

- **Stima Salute Piante (Markov)**, utilizza modelli probabilistici per determinare lo stato di benessere o stress delle colture.

- **Predici fabbisogno idrico (Machine Learning)**, stima la quantità d'acqua necessaria per i cicli futuri in base ai dati storici.
