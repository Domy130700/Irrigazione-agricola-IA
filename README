# Installazione
Installare SWI Prolog in base al sistema operativo in uso (**scaricare la versione 8**):

[https://www.swi-prolog.org/download/stable?show=all](https://www.swi-prolog.org/download/stable?show=all)

Posizionarsi all'interno della root principale:

`cd irrigazione-intelligente`

Creare l'ambiente virtuale (facoltativo):

`python -m venv venv`

Installare le dipendenze:

`pip install -r requirements.txt`

---

# Guia all'utilizzo
## Caricamento file
Il programma, una volta avviato, chiede all'utente quale tipo di dati utilizzare. La scelta può essere tra le seguenti opzioni:

* **Utilizzare un file pre-caricato** sulla piattaforma (consigliato per comodità e velocità di elaborazione).
* **Caricare un file XML**, opzione per caricare un file dal proprio dispositivo. Il file deve avere la struttura standard OSM (OpenStreetMap) XML per un utilizzo corretto del programma. In pratica, i dati presenti nel file dovranno rispettare un formato preciso (tag sensori e valvole), per essere elaborati correttamente dal programma.

## Ottimizzazione globale (CSP)
Una volta caricato il file, il programma chiederà se si desidera ottimizzare la distribuzione idrica in modo globale (tramite CSP), per bilanciare la pressione ed evitare conflitti di erogazione tra i settori della zona in esame.

## Opzioni principali
Il menu verrà poi sostituito con le seguenti opzioni:

1. **Elenco Condotte (Tubi)**: restituisce tutte le tubature della rete idrica caricate dal file.
2. **Elenco Punti di Irrigazione (Valvole/Sensori)**: restituisce informazioni su tutti i componenti attivi presenti nella zona.
3. **Calcola percorso flusso ottimale (A*)**: prende in input un punto di origine e uno di destinazione e restituisce il percorso più efficiente per l'acqua.
4. **Ottimizza distribuzione idrica (CSP)**: permette di ricalcolare l'allocazione delle risorse per bilanciare la pressione.
5. **Stima Salute Piante (Markov)**: utilizza modelli probabilistici per determinare lo stato di benessere o stress delle colture.
6. **Predici fabbisogno idrico (Machine Learning)**: stima la quantità d'acqua necessaria per i cicli futuri in base ai dati storici.

---

## Esempi concreti di utilizzo
* **Visualizzazione rete**: Se si vuole visualizzare tutte le condotte presenti in una determinata zona, si può selezionare l'opzione "Elenco Condotte (Tubi)" dal menu e il programma mostrerà l'intera rete di distribuzione.
* **Ricerca percorso**: Se si vuole trovare il percorso più efficiente tra la sorgente e un settore specifico, si può selezionare l'opzione "Calcola percorso flusso ottimale (A*)" dal menu e inserire i nomi dei nodi interessati. Il programma mostrerà la sequenza di valvole da attivare e il costo del percorso.
