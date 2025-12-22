import pandas as pd 
import sys
import yaml
import pickle
from sklearn.ensemble import RandomForestRegressor
pd.options.display.float_format = '{:.2f}'.format
import json
import yaml
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np 

def evaluate():
    with open("params.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    df = pd.read_csv("data/prepared_data.csv")
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    
    features = config["prepare"]["features"]
    X = df[features]
    y = df['Ventas']
    
    predictions = model.predict(X)
    
    decimals = config.get("evaluate", {}).get("round_decimals", 4)
    
    mae = mean_absolute_error(y, predictions)
    mse = mean_squared_error(y, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, predictions)
    
    metrics = {
        "mae": round(float(mae), decimals),
        "rmse": round(float(rmse), decimals),
        "r2": round(float(r2), decimals)
    }
    
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/scores.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(f"Métricas calculadas con éxito: {metrics}")

if __name__ == "__main__":
    evaluate()