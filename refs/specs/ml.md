# Objetivo
Nuestro objetivo es entrenar un modelo de machine-learning de forma reproducible para clasificar llamadas entrantes en una de las 11 categorías de soporte que hay en nuestra empresa.

# Implementación de partida

En la carpeta ml/notebooks encontrarás notebooks para:
- Realizar la limpieza de los datos de entrada,
- Validar los datos crudos y limpios mediante pandera
- Entrenar un modelo de machine learning basado en TfIdfVectorizer y persistir el pipeline de transformación y predicción (a partir de los datos limpios)
- Realizar inferencia a partir del modelo en fichero
En la carpeta ml/src/schemas:
- Esquemas mediante pandera para la validación de los datos raw y procesados

# Implementación en el proyecto

Sigue la implementación descrita en AGENTS.md con y refactoriza el código de los notebooks para respetar esa especificación generando los scripts de limpieza, entrenamiento, validación, inferencia, etc.
