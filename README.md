# Pronóstico de Ventas - Incolmotos Yamaha

## 🚀 Arquitectura del Proyecto
El pipeline está automatizado mediante `dvc.yaml` e incluye las siguientes etapas:
1. **Preparación:** Limpieza de datos y feature engineering.
2. **Entrenamiento:** Ajuste del modelo utilizando parámetros configurables.
3. **Evaluación:** Generación de métricas de desempeño.

## 🛠️ Requisitos e Instalación
Para replicar este entorno localmente:

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/jumamaqui/Prueba_Yamaha_Final.git](https://github.com/jumamaqui/Prueba_Yamaha_Final.git)

## Ejecución

- Poetry: poetry run dvc repro
- Sin Poetry: dvc repro

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

## Explicación

"Se implementó un sistema de seguimiento de experimentos basado en los archivos params.yaml y metrics/scores.json. La comparación se realiza mediante el comando dvc metrics diff, el cual permite contrastar el desempeño de diferentes arquitecturas del modelo (variando hiperparámetros como max_depth o min_samples_split) de manera cuantitativa. El 'Mejor Modelo' se define como aquel que presenta el menor RMSE en el conjunto de evaluación, y es marcado en el historial de Git mediante un 'Tag' para asegurar su trazabilidad absoluta."

## 📝 Control de Versiones y Comparación
Este proyecto utiliza Git Tags y DVC para la gestión de experimentos:

- **v1.0**: Modelo base (Random Forest) - $R^2: 0.75$.
- **Comparar versiones**: `dvc metrics diff v1.0`
- **Restaurar una versión**: `git checkout v1.0 && dvc checkout`

## Integración
- Generación de métricas: Calcula MAE, RMSE y $R^2$ para evaluar el pronóstico de ventas2222.
- Comparación de resultados: Al guardar los resultados en metrics/scores.json, DVC permite usar el comando dvc metrics diff para comparar qué ejecución (o qué cambio en los parámetros del modelo) dio un mejor resultado3.
- Consistencia: Utiliza las mismas variables (features) y lógica de redondeo definidas en el archivo central de parámetros4.