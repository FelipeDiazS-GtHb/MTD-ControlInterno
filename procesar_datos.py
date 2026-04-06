import pandas as pd

# =====================================================================
# FUNCIÓN 1: NOTA ENFERMERIA VENTILADOS
# =====================================================================
def procesar_nota_ventilados(ruta_archivo):
    print(f"\n[1] Procesando Ventilados: {ruta_archivo}")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1; IDX_CSV_PACIENTE = 3; IDX_CSV_TURNO = 21
    IDX_CSV_PROFESIONAL = 77; IDX_CSV_UBICACION = 78; IDX_CSV_PROXIMIDAD = 79     

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "VENTILADO"
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[2] = df_raw.iloc[:, IDX_CSV_FECHA].astype(str).str.split(" ").str[0]
    except IndexError: pass
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except IndexError: pass
    try:
        ubi = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
        prox = df_raw.iloc[:, IDX_CSV_PROXIMIDAD].fillna("").astype(str)
        df_target[8] = (ubi + " | " + prox).str.replace('nan', '').str.strip(' | ')
    except IndexError: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# FUNCIÓN 2: NOTA DE ENFERMERÍA NORMAL
# =====================================================================
def procesar_nota_enfermeria(ruta_archivo):
    print(f"\n[2] Procesando Enfermería Normal: {ruta_archivo}")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1; IDX_CSV_PACIENTE = 3; IDX_CSV_TURNO = 21          
    IDX_CSV_PROFESIONAL = 44; IDX_CSV_UBICACION = 45; IDX_CSV_PROXIMIDAD = 46     

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "NOTA ENFERMERIA" 
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[2] = df_raw.iloc[:, IDX_CSV_FECHA].astype(str).str.split(" ").str[0]
    except IndexError: pass
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except IndexError: pass
    try:
        ubi = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
        prox = df_raw.iloc[:, IDX_CSV_PROXIMIDAD].fillna("").astype(str)
        df_target[8] = (ubi + " | " + prox).str.replace('nan', '').str.strip(' | ')
    except IndexError: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# FUNCIÓN 3: NOTAS CUIDADOR (ACTIVIDADES BÁSICAS)
# =====================================================================
def procesar_cuidador_actividades(ruta_archivo):
    print(f"\n[3] Procesando Actividades Básicas: {ruta_archivo}")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1; IDX_CSV_PACIENTE = 3; IDX_CSV_TURNO = 14          
    IDX_CSV_PROFESIONAL = 35; IDX_CSV_UBICACION = 37; IDX_CSV_PROXIMIDAD = 38     

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "CUIDADOR" 
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[2] = df_raw.iloc[:, IDX_CSV_FECHA].astype(str).str.split(" ").str[0]
    except IndexError: pass
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except IndexError: pass
    try:
        ubi = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
        prox = df_raw.iloc[:, IDX_CSV_PROXIMIDAD].fillna("").astype(str)
        df_target[8] = (ubi + " | " + prox).str.replace('nan', '').str.strip(' | ')
    except IndexError: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# FUNCIÓN 4: NOTAS CUIDADOR (MEDIOS INVASIVOS)
# =====================================================================
def procesar_medios_invasivos(ruta_archivo):
    print(f"\n[4] Procesando Medios Invasivos: {ruta_archivo}")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1; IDX_CSV_PACIENTE = 3; IDX_CSV_TURNO = 14          
    IDX_CSV_PROFESIONAL = 33; IDX_CSV_UBICACION = 35; IDX_CSV_PROXIMIDAD = 36     

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "MEDIOS INVASIVOS"
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[2] = df_raw.iloc[:, IDX_CSV_FECHA].astype(str).str.split(" ").str[0]
    except IndexError: pass
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except IndexError: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except IndexError: pass
    try:
        ubi = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
        prox = df_raw.iloc[:, IDX_CSV_PROXIMIDAD].fillna("").astype(str)
        df_target[8] = (ubi + " | " + prox).str.replace('nan', '').str.strip(' | ')
    except IndexError: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# BLOQUE DE PRUEBA GENERAL
# =====================================================================
if __name__ == "__main__":
    # Definimos las rutas a los 4 archivos
    ruta_ventilados = "descargas control interno 2026-03-01/Nota_Enfermeria_Ventilados.csv"
    ruta_enfermeria = "descargas control interno 2026-03-01/Nota_Enfermeria.csv"
    ruta_actividades = "descargas control interno 2026-03-01/Notas_Cuidador_Actividades.csv"
    ruta_invasivos = "descargas control interno 2026-03-01/Notas_Cuidador_Invasivos.csv"
    
    # 1. VENTILADOS
    datos_ventilados = procesar_nota_ventilados(ruta_ventilados)
    print("-> MUESTRA (VENTILADOS):")
    for fila in datos_ventilados[:3]: print(fila)

    # 2. ENFERMERÍA NORMAL
    datos_enfermeria = procesar_nota_enfermeria(ruta_enfermeria)
    print("\n-> MUESTRA (ENFERMERÍA NORMAL):")
    for fila in datos_enfermeria[:3]: print(fila)

    # 3. ACTIVIDADES BÁSICAS
    datos_actividades = procesar_cuidador_actividades(ruta_actividades)
    print("\n-> MUESTRA (ACTIVIDADES BÁSICAS):")
    for fila in datos_actividades[:3]: print(fila)

    # 4. MEDIOS INVASIVOS
    datos_invasivos = procesar_medios_invasivos(ruta_invasivos)
    print("\n-> MUESTRA (MEDIOS INVASIVOS):")
    for fila in datos_invasivos[:3]: print(fila)