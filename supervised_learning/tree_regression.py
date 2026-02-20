import os
import pickle
from preprocessing import initialize_ML
from sklearn.tree import DecisionTreeRegressor

def train_tree():
    print("Avvio training Tree Regression...")
    
    # 1. Caricamento dati
    X, y, scaler = initialize_ML()
    
    if X is None: return

    # 2. Addestramento Modello
    # Parametri ottimizzati per evitare overfitting
    model = DecisionTreeRegressor(max_depth=15, min_samples_leaf=10)
    model.fit(X, y)

    # 3. Salvataggio
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    # Salviamo come tree_regression.sav
    filename = os.path.join(models_dir, 'tree_regression.sav')
    pickle.dump(model, open(filename, 'wb'))
    
    # Salviamo anche lo scaler specifico se necessario (o usiamo quello comune)
    scaler_filename = os.path.join(models_dir, 'scaler_tree.sav')
    pickle.dump(scaler, open(scaler_filename, 'wb'))

    print(f"✅ Modello Tree Regression salvato in {filename}")

if __name__ == "__main__":
    train_tree()