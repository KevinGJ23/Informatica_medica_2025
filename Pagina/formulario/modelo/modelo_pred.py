# Librerias necesarias
import pandas as pd
import joblib
import os

# === Carga del modelo previamente entrenado y serializado ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # Directorio actual del archivo
MODEL_PATH = os.path.join(BASE_DIR, 'modelo_catboost.pkl')  # Ruta absoluta al modelo
pipeline = joblib.load(MODEL_PATH)                          # Cargar el modelo con joblib

# === Diccionario de mapeos de variables categóricas a valores numéricos ===
# Este mapeo se aplica a los datos del formulario antes de pasar al modelo.
mapeos = {
    "SEXO": {"F": 0, "M": 1},
    "TIPO_INGRESO": {"PROGRAMADO": 0, "URGENCIA": 1},
    "CUIDADOS_INTENSIVOS": {"NO": 0, "SI": 1},
    "SITUACION_ALTA": {"ALTA MÉDICA": 0, "FALLECIDO": 1},
    "TIPO_SERVICIO": {"CIRUGÍA": 0, "URGENCIA PEDÍATRICAS": 1, "NO APLICA": 2, "URGENCIA ADULTOS": 3},
    "DX_EGRESO_AGRUPADO": {
        "Vacio": 0, "Infecciosas": 1, "Neoplasias": 2, "Endocrino": 3, "Psicológico": 4,
        "Neurológico": 5, "Sensorial": 6, "Circulatorio": 7, "Respiratorio": 8, "Digestivo": 9,
        "Dermatológico": 10, "Musculoesquelético": 11, "Genitourinario": 12, "Traumatismo": 13, "Otros": 14
    },
    "PROC_1_GRUPO": {
        "Desconocido": 0, "Misceláneos": 1, "Sistema nervioso": 2, "Endócrino": 3, "Ojo y oído": 4,
        "Respiratorio": 5, "Cardiovascular": 6, "Linfático y bazo": 7, "Digestivo": 8,
        "Genitourinario": 9, "Parto y puerperio": 10, "Musculoesquelético": 11, "Tegumentario": 12,
        "Obstetricia": 13, "Cirugía músculo-esquelética": 14, "Mama y piel": 15,
        "Diagnóstico/terapéutico": 16, "Otros": 17
    },
    "PROC_2_GRUPO": {
        "Desconocido": 0, "Misceláneos": 1, "Sistema nervioso": 2, "Endócrino": 3, "Ojo y oído": 4,
        "Respiratorio": 5, "Cardiovascular": 6, "Linfático y bazo": 7, "Digestivo": 8,
        "Genitourinario": 9, "Parto y puerperio": 10, "Musculoesquelético": 11, "Tegumentario": 12,
        "Obstetricia": 13, "Cirugía músculo-esquelética": 14, "Mama y piel": 15,
        "Diagnóstico/terapéutico": 16, "Otros": 17
    },
    "PROC_3_GRUPO": {
        "Desconocido": 0, "Misceláneos": 1, "Sistema nervioso": 2, "Endócrino": 3, "Ojo y oído": 4,
        "Respiratorio": 5, "Cardiovascular": 6, "Linfático y bazo": 7, "Digestivo": 8,
        "Genitourinario": 9, "Parto y puerperio": 10, "Musculoesquelético": 11, "Tegumentario": 12,
        "Obstetricia": 13, "Cirugía músculo-esquelética": 14, "Mama y piel": 15,
        "Diagnóstico/terapéutico": 16, "Otros": 17
    },
    "EDAD_AGRUPADA": {
        "Neonato": 0, "Niñez": 1, "Adolescencia": 2, "Joven adulto": 3, "Adulto": 4, "Adulto mayor": 5
    },
    "ESTANCIA_AGRUPADA": {
        "<2 días": 0, "2-4 días": 1, "5-7 días": 2, "8-14 días": 3, "15+ días": 4
    },
    "UCI_AGRUPADA": {
        "Sin cuidados": 0, "1 día": 1, "2-4 días": 2, "5-9 días": 3, "10+ días": 4
    },
    "DXR_3": {
        "Vacio": 0, "Infecciosas": 1, "Neoplasias": 2, "Endocrino": 3, "Psicológico": 4,
        "Neurológico": 5, "Sensorial": 6, "Circulatorio": 7, "Respiratorio": 8, "Digestivo": 9,
        "Dermatológico": 10, "Musculoesquelético": 11, "Genitourinario": 12, "Traumatismo": 13, "Otros": 14
    },
    "DXR_1": {
        "Vacio": 0, "Infecciosas": 1, "Neoplasias": 2, "Endocrino": 3, "Psicológico": 4,
        "Neurológico": 5, "Sensorial": 6, "Circulatorio": 7, "Respiratorio": 8, "Digestivo": 9,
        "Dermatológico": 10, "Musculoesquelético": 11, "Genitourinario": 12, "Traumatismo": 13, "Otros": 14
    }
}

# === Función de predicción principal ===
def predecir(data_dict):
    """
    Convierte el diccionario del formulario a DataFrame,
    aplica los mapeos y ejecuta la predicción con el modelo cargado.
    """
    df = pd.DataFrame([data_dict])  # Convertir entrada a DataFrame
    for col, mapa in mapeos.items():
        if col in df.columns:
            df[col] = df[col].map(mapa)  # Aplicar codificación numérica
    return pipeline.predict(df)[0]  # Retornar la predicción (0 o 1)

# === Función para agrupar códigos CIE-10 en categorías clínicas ===
def agrupar_codigo(codigo):
    """
    Clasifica un código CIE-10 (por ejemplo, 'I10') en una categoría clínica general.
    Retorna una de las categorías estandarizadas utilizadas por el modelo.
    """
    if not isinstance(codigo, str) or len(codigo) < 3:
        return 'Vacio'

    letra = codigo[0].upper()
    try:
        num = int(codigo[1:3])
    except:
        num = None

    if letra in ['A', 'B']:
        grupo = 'A-B'
    elif letra == 'C':
        grupo = 'C-D1'
    elif letra == 'D':
        grupo = 'C-D2' if num is not None and num <= 48 else 'D-D'
    elif letra == 'E':
        grupo = 'E-E'
    elif letra == 'F':
        grupo = 'F-F'
    elif letra == 'G':
        grupo = 'G-G'
    elif letra == 'H':
        grupo = 'H-H'
    elif letra == 'I':
        grupo = 'I1' if num is not None and (10 <= num <= 15 or 20 <= num <= 25 or 60 <= num <= 69) else 'I2'
    elif letra == 'J':
        grupo = 'J-J'
    elif letra == 'K':
        grupo = 'K1' if num is not None and 0 <= num <= 63 else 'K2'
    elif letra == 'L':
        grupo = 'L-L'
    elif letra == 'M':
        grupo = 'M-M'
    elif letra == 'N':
        grupo = 'N-N'
    elif letra in ['O', 'P', 'Q', 'R', 'Z']:
        grupo = 'P-Q-O-R-Z'
    elif letra == 'S':
        grupo = 'S-T1'
    elif letra == 'T':
        grupo = 'S-T2'
    elif letra in ['V', 'W', 'X', 'Y']:
        grupo = 'S-T3'
    else:
        grupo = 'OTROS'

    # Diccionario de mapeo final a categoría clínica
    reagrupacion = {
        'J-J': 'Respiratorio',
        'N-N': 'Genitourinario',
        'I1': 'Circulatorio',
        'I2': 'Circulatorio',
        'S-T1': 'Traumatismo',
        'S-T2': 'Traumatismo',
        'S-T3': 'Traumatismo',
        'C-D1': 'Neoplasias',
        'C-D2': 'Neoplasias',
        'D-D': 'Neoplasias',
        'A-B': 'Infecciosas',
        'K1': 'Digestivo',
        'K2': 'Digestivo',
        'G-G': 'Neurológico',
        'F-F': 'Psicológico',
        'E-E': 'Endocrino',
        'M-M': 'Musculoesquelético',
        'L-L': 'Dermatológico',
        'H-H': 'Sensorial',
        'P-Q-O-R-Z': 'Otros',
        'OTROS': 'Vacio'
    }

    return reagrupacion.get(grupo, 'Vacio')
