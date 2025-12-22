# Pronóstico de Ventas - Incolmotos Yamaha

## ¿Cómo funciona el pipeline?
El pipeline utiliza DVC para conectar los datos con el código. Cada etapa (stage) define sus dependencias (archivos de entrada) y sus salidas (outs). Al ejecutar dvc repro, DVC verifica si algo ha cambiado. Si los archivos de entrada no han variado, utiliza el caché; si han cambiado, ejecuta solo las partes necesarias del proceso.

## ¿Qué ocurre cuando cambian los datos o el código?
Cambio en Datos: Si Data.xlsx se actualiza, DVC detecta un cambio en el hash del archivo. Al ejecutar dvc repro, se invalidan todas las etapas posteriores y se vuelve a ejecutar la preparación, el entrenamiento y la evaluación.

Cambio en Código: Si modificas train.py, DVC nota el cambio en la dependencia y vuelve a entrenar el modelo, asegurando que el archivo model.pkl siempre sea consistente con el código actual.

## ¿Cómo se define el mejor modelo?
El mejor modelo se define mediante la comparación de las métricas generadas en la etapa de evaluación (ej. RMSE o MAE).

Se ejecutan experimentos con diferentes parámetros en params.yaml.

Se usa el comando dvc metrics diff para comparar los resultados entre diferentes versiones de Git (commits).

El modelo con el error más bajo y que no presente sobreajuste (overfitting) se marca como la versión productiva mediante un Git Tag.