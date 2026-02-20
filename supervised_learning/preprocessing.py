import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocessing():
    '''
    Funzione opzionale: se hai irrigation_raw.csv, lo converte in edit.
    Se hai già irrigation_edit.csv pronto, puoi saltare questa chiamata.
    '''
    try:
        data = pd.read_csv("dataset/irrigation_raw.csv")
        # Logica di conversione raw -> edit (omessa se usi file già editato)
        # Qui andrebbe la pulizia date e normalizzazione se necessaria
        print("Preprocessing raw -> edit non necessario se il file edit esiste già.")
    except FileNotFoundError:
        print("File raw non trovato, proseguo assumendo che irrigation_edit.csv esista.")

def initialize_ML():
    '''
    Carica il dataset 'irrigation_edit.csv' e prepara X e y per i modelli.
    Basato sulla struttura del tuo file CSV.
    '''
    try:
        # Carichiamo il dataset pronto
        dataset = pd.read_csv("dataset/irrigation_edit.csv")
    except FileNotFoundError:
        print("❌ Errore: 'dataset/irrigation_edit.csv' non trovato!")
        return None, None, None

    # SELEZIONE FEATURE (Input)
    # Usiamo le colonne che influenzano l'irrigazione presenti nel tuo file
    # CropType, SoilType, Moisture_Norm, Temp_Norm, Hour, Month
    feature_cols = ['CropType', 'SoilType', 'Moisture_Norm', 'Temp_Norm', 'Hour', 'Month']
    
    # Assicuriamoci che le colonne esistano
    X_cols = [c for c in feature_cols if c in dataset.columns]
    X = dataset[X_cols]
    
    # SELEZIONE TARGET (Output)
    # La colonna 'WaterNeed' indica quanta acqua serve
    y = dataset[['WaterNeed']]

    # Normalizzazione
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Per y, essendo un valore continuo (litri), possiamo non scalarlo o scalarlo
    # Qui non lo scaliamo per avere l'output leggibile in Litri diretti
    y_values = y.values.ravel() 

    return X_scaled, y_values, scaler