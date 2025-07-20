from django.shortcuts import render                       # Importa la función 'render' para devolver respuestas HTTP con plantillas HTML
from .modelo.modelo_pred import predecir, agrupar_codigo  # Funciones del modelo

# Opciones fijas del formulario. Los campos DXR_* están vacíos porque se completan con códigos crudos.
opciones = {
    "SEXO": ["F", "M"],
    "TIPO_INGRESO": ["URGENCIA", "PROGRAMADO"],
    "CUIDADOS_INTENSIVOS": ["SI", "NO"],
    "DXR_1": [],
    "DXR_3": [],
    "SITUACION_ALTA": ["ALTA MÉDICA", "FALLECIDO"],
    "TIPO_SERVICIO": ["URGENCIA ADULTOS", "NO APLICA", "URGENCIA PEDÍATRICAS", "CIRUGÍA"],
    "DX_EGRESO_AGRUPADO": [],
    "PROC_1_GRUPO": ["Misceláneos", "Sistema nervioso", "Endócrino", "Ojo y oído", "Respiratorio",
                     "Cardiovascular", "Linfático y bazo", "Digestivo", "Genitourinario",
                     "Parto y puerperio", "Musculoesquelético", "Tegumentario", "Obstetricia",
                     "Cirugía músculo-esquelética", "Mama y piel", "Diagnóstico/terapéutico", "Otros"],
    "PROC_2_GRUPO": ["Misceláneos", "Sistema nervioso", "Endócrino", "Ojo y oído", "Respiratorio",
                     "Cardiovascular", "Linfático y bazo", "Digestivo", "Genitourinario",
                     "Parto y puerperio", "Musculoesquelético", "Tegumentario", "Obstetricia",
                     "Cirugía músculo-esquelética", "Mama y piel", "Diagnóstico/terapéutico", "Otros"],
    "PROC_3_GRUPO": ["Misceláneos", "Sistema nervioso", "Endócrino", "Ojo y oído", "Respiratorio",
                     "Cardiovascular", "Linfático y bazo", "Digestivo", "Genitourinario",
                     "Parto y puerperio", "Musculoesquelético", "Tegumentario", "Obstetricia",
                     "Cirugía músculo-esquelética", "Mama y piel", "Diagnóstico/terapéutico", "Otros"],
    "EDAD_AGRUPADA": ["Neonato", "Niñez", "Adolescencia", "Joven adulto", "Adulto", "Adulto mayor"],
    "ESTANCIA_AGRUPADA": ["15+ días", "2-4 días", "8-14 días", "5-7 días", "<2 días"],
    "UCI_AGRUPADA": ["Sin cuidados", "1 día", "2-4 días", "5-9 días", "10+ días"]
}

def formulario_view(request):
    resultado = None    # Variable para almacenar el resultado de la predicción
    seleccionados = {}  # Diccionario para guardar los valores seleccionados por el usuario

    if request.method == "POST":
        # Recupera los datos enviados por el formulario
        seleccionados = {campo: request.POST[campo] for campo in opciones}

        # Agrupa los códigos DXR_* crudos a sus versiones agrupadas usando el modelo
        for campo in ["DXR_1", "DXR_3", "DX_EGRESO_AGRUPADO"]:
            if campo in seleccionados:
                seleccionados[campo] = agrupar_codigo(seleccionados[campo])

        # Llama al modelo para obtener la predicción
        resultado = predecir(seleccionados)

    # Renderiza la plantilla HTML pasando las opciones, los datos seleccionados y el resultado
    return render(request, "formulario/index.html", {
        "opciones": opciones,
        "resultado": resultado,
        "seleccionados": seleccionados
    })
