import os
import pickle
from sklearn.neighbors import KNeighborsRegressor
from preprocessing import initialize_ML 

def train_knn():
    print("Avvio training KNN...")
    
    # 1. Caricamento dati
    X, y, scaler = initialize_ML()
    
    if X is None:
        return

    # 2. Addestramento Modello
    # n_neighbors=5 è standard, puoi rimettere 3 se preferisci
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X, y)

    # 3. Salvataggio
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    # Salviamo come knn.sav per compatibilità con la KnowledgeBase
    knn_filename = os.path.join(models_dir, 'knn.sav')
    pickle.dump(model, open(knn_filename, 'wb'))

    scaler_filename = os.path.join(models_dir, 'scaler_knn.sav')
    pickle.dump(scaler, open(scaler_filename, 'wb'))

    print(f"✅ Modello KNN salvato in {knn_filename}")

if __name__ == "__main__":
    train_knn()