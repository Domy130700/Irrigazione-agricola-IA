from numpy import mean, sqrt
from sklearn.model_selection import ShuffleSplit, cross_val_score

def k_fold_cross_validation(model, X, y):
    '''
    Valuta l'accuratezza del modello nel predire il fabbisogno idrico.
    '''
    # Cross Validation a 10 fold
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)

    # R2 Score (coefficiente di determinazione)
    r2 = mean(cross_val_score(model, X, y, cv=cv, scoring='r2'))
    
    # Mean Squared Error (negativo perché sklearn massimizza lo score)
    mse = -mean(cross_val_score(model, X, y, cv=cv, scoring='neg_mean_squared_error'))
    
    # Root Mean Squared Error (errore in litri)
    rmse = sqrt(mse)
    
    # Mean Absolute Error
    mae = -mean(cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error'))

    return r2, mae, mse, rmse

def stampa_valutazione(nome_modello, r2, mae, rmse):
    print(f"\n--- Valutazione {nome_modello} ---")
    print(f"R2 Score (Precisione): {r2:.4f}")
    print(f"MAE (Errore medio assoluto): {mae:.4f} Litri")
    print(f"RMSE (Scarto quadratico medio): {rmse:.4f} Litri")