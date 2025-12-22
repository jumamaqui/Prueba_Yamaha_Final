#Librerias 
import pandas as pd 
import sys
import yaml
import pickle
from sklearn.ensemble import RandomForestRegressor
pd.options.display.float_format = '{:.2f}'.format
def leer_data(input_path):
    df = pd.read_excel(input_path)
    df = df.rename(columns={'Precio Unitario': 'Precio_Unitario', 
    })
    return df 
def check_and_impute_dates(df, output_path,date_column='Fecha'):
    params = yaml.safe_load(open("params.yaml"))["prepare"]
    impute = params["imputation_strategy"]
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(date_column)
    full_range = pd.date_range(start=df[date_column].min(), 
                               end=df[date_column].max(), 
                               freq='D')
    if len(full_range) == len(df):
        print("Todas las fechas son consecutivas.")
        return df
    else:
        missing_days = len(full_range) - len(df)
        print(f" Se detectaron {missing_days} días faltantes. Iniciando imputación...")
        df = df.set_index(date_column).reindex(full_range).reset_index()
        df = df.rename(columns={'index': date_column})
        df['Ventas'] = df['Ventas'].fillna(impute["ventas"])
        df['Promo'] = df['Promo'].fillna(impute["promo"])   
        # Imputación dinámica para Precio_Unitario
        if impute["precio"] == "linear":
            df['Precio_Unitario'] = df['Precio_Unitario'].interpolate(method='linear')
        else:
            df['Precio_Unitario'] = df['Precio_Unitario'].fillna(0)    
        df['Precio_Unitario'] = df['Precio_Unitario'].round(2)
        df['Ventas'] = df['Ventas'].round(0).astype(int)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df = df.sort_values('Fecha')
        df['dia_semana'] = df['Fecha'].dt.dayofweek
        df['mes'] = df['Fecha'].dt.month
        df.to_csv(output_path, index=False)
        return df

if __name__ == "__main__":
    df = leer_data('data/Data.xlsx')
    df = check_and_impute_dates(df,'data/prepared_data.csv','Fecha')