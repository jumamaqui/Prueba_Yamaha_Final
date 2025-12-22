#Librerias 
import pandas as pd 
import sys
import yaml
import pickle
from sklearn.ensemble import RandomForestRegressor
pd.options.display.float_format = '{:.2f}'.format
def train():
    with open("params.yaml", "r") as f:
        config = yaml.safe_load(f)
    df = pd.read_csv("data/prepared_data.csv")
    
    X = df[config["prepare"]["features"]]
    y = df['Ventas']
    
    model = RandomForestRegressor(
        n_estimators=config["train"]["n_estimators"],
        max_depth=config["train"]["max_depth"],
        random_state=config["base"]["random_state"]
    )
    model.fit(X, y)
    
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train()