import pandas as pd
import os

# =====================================================================
# FUNCIÓN 1: NOTA ENFERMERIA VENTILADOS
# =====================================================================
def procesar_nota_ventilados(ruta_archivo):
    print(f"  -> Procesando: Ventilados")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1; IDX_CSV_PACIENTE = 3; IDX_CSV_TURNO = 21
    IDX_CSV_PROFESIONAL = 77; IDX_CSV_UBICACION = 78     
    IDX_CSV_ESTADO = 79 # (CB)

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "VENTILADO"
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    # --- BLINDAJE CONTRA EL ERROR DE MERGE ---
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, IDX_CSV_FECHA], errors='coerce', dayfirst=True)
        f_limpia = fechas_dt.dt.strftime('%d/%m/%Y').tolist()
        f_cruda = df_raw.iloc[:, IDX_CSV_FECHA].fillna("").astype(str).tolist()
        df_target[2] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(f_limpia, f_cruda)]
    except Exception: pass
    
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except Exception: pass
    try: df_target[8] = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
    except Exception: pass
    try: df_target[9] = df_raw.iloc[:, IDX_CSV_ESTADO].fillna("").astype(str)
    except Exception: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# FUNCIÓN 2: NOTA DE ENFERMERÍA NORMAL
# =====================================================================
def procesar_nota_enfermeria(ruta_archivo):
    print(f"  -> Procesando: Enfermería Normal")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1; IDX_CSV_PACIENTE = 3; IDX_CSV_TURNO = 21          
    IDX_CSV_PROFESIONAL = 44; IDX_CSV_UBICACION = 45   
    IDX_CSV_ESTADO = 46 # (AU)

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "NOTA ENFERMERIA" 
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    # --- BLINDAJE CONTRA EL ERROR DE MERGE ---
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, IDX_CSV_FECHA], errors='coerce', dayfirst=True)
        f_limpia = fechas_dt.dt.strftime('%d/%m/%Y').tolist()
        f_cruda = df_raw.iloc[:, IDX_CSV_FECHA].fillna("").astype(str).tolist()
        df_target[2] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(f_limpia, f_cruda)]
    except Exception: pass
    
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except Exception: pass
    try: df_target[8] = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
    except Exception: pass
    try: df_target[9] = df_raw.iloc[:, IDX_CSV_ESTADO].fillna("").astype(str)
    except Exception: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# FUNCIÓN 3: NOTAS CUIDADOR (ACTIVIDADES BÁSICAS)
# =====================================================================
def procesar_cuidador_actividades(ruta_archivo):
    print(f"  -> Procesando: Actividades Básicas")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1       # Columna B
    IDX_CSV_PACIENTE = 3    
    IDX_CSV_TURNO = 14      
    IDX_CSV_PROFESIONAL = 35 
    IDX_CSV_UBICACION = 39  # Columna AN 
    IDX_CSV_ESTADO = 40     # Columna AO 

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "CUIDADOR" 
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    # --- BLINDAJE CONTRA EL ERROR DE MERGE ---
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, IDX_CSV_FECHA], errors='coerce', dayfirst=True)
        f_limpia = fechas_dt.dt.strftime('%d/%m/%Y').tolist()
        f_full = fechas_dt.dt.strftime('%d/%m/%Y %H:%M').tolist()
        f_cruda = df_raw.iloc[:, IDX_CSV_FECHA].fillna("").astype(str).tolist()
        
        df_target[2] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(f_limpia, f_cruda)]
        df_target[5] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(f_full, f_cruda)]
    except Exception: pass
    
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except Exception: pass
    try: df_target[8] = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
    except Exception: pass
    try: df_target[9] = df_raw.iloc[:, IDX_CSV_ESTADO].fillna("").astype(str)
    except Exception: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# FUNCIÓN 4: NOTAS CUIDADOR (MEDIOS INVASIVOS)
# =====================================================================
def procesar_medios_invasivos(ruta_archivo):
    print(f"  -> Procesando: Medios Invasivos")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    df_raw.columns = df_raw.columns.str.strip()

    IDX_CSV_FECHA = 1; IDX_CSV_PACIENTE = 3; IDX_CSV_TURNO = 14          
    IDX_CSV_PROFESIONAL = 33
    IDX_CSV_UBICACION = 37  # Columna AL 
    IDX_CSV_ESTADO = 38     # Columna AM 

    df_target = pd.DataFrame(index=df_raw.index, columns=range(11)).fillna("")
    df_target[1] = "MEDIOS INVASIVOS"
    
    try: df_target[0] = df_raw.iloc[:, IDX_CSV_PROFESIONAL].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    # --- BLINDAJE CONTRA EL ERROR DE MERGE ---
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, IDX_CSV_FECHA], errors='coerce', dayfirst=True)
        f_limpia = fechas_dt.dt.strftime('%d/%m/%Y').tolist()
        f_cruda = df_raw.iloc[:, IDX_CSV_FECHA].fillna("").astype(str).tolist()
        df_target[2] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(f_limpia, f_cruda)]
    except Exception: pass
    
    try: df_target[3] = df_raw.iloc[:, IDX_CSV_PACIENTE].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target[4] = df_raw.iloc[:, IDX_CSV_TURNO]
    except Exception: pass
    try: df_target[8] = df_raw.iloc[:, IDX_CSV_UBICACION].fillna("").astype(str)
    except Exception: pass
    try: df_target[9] = df_raw.iloc[:, IDX_CSV_ESTADO].fillna("").astype(str)
    except Exception: pass

    return df_target.fillna("").values.tolist()


# =====================================================================
# FUNCIÓN MAESTRA (DIRECTOR DE ORQUESTA)
# =====================================================================
def procesar_carpeta(carpeta_base):
    print(f"\n==================================================")
    print(f" INICIANDO EXTRACCIÓN EN CARPETA: {carpeta_base}")
    print(f"==================================================")
    
    archivos = {
        "ventilados": "Nota_Enfermeria_Ventilados.csv",
        "enfermeria": "Nota_Enfermeria.csv",
        "actividades": "Notas_Cuidador_Actividades.csv",
        "invasivos": "Notas_Cuidador_Invasivos.csv"
    }
    
    datos_completos = {"ventilados": [], "enfermeria": [], "actividades": [], "invasivos": []}

    ruta_v = os.path.join(carpeta_base, archivos["ventilados"])
    if os.path.exists(ruta_v): datos_completos["ventilados"] = procesar_nota_ventilados(ruta_v)
    else: print(f"  [X] No se encontró el archivo: {archivos['ventilados']}")

    ruta_e = os.path.join(carpeta_base, archivos["enfermeria"])
    if os.path.exists(ruta_e): datos_completos["enfermeria"] = procesar_nota_enfermeria(ruta_e)
    else: print(f"  [X] No se encontró el archivo: {archivos['enfermeria']}")

    ruta_a = os.path.join(carpeta_base, archivos["actividades"])
    if os.path.exists(ruta_a): datos_completos["actividades"] = procesar_cuidador_actividades(ruta_a)
    else: print(f"  [X] No se encontró el archivo: {archivos['actividades']}")

    ruta_i = os.path.join(carpeta_base, archivos["invasivos"])
    if os.path.exists(ruta_i): datos_completos["invasivos"] = procesar_medios_invasivos(ruta_i)
    else: print(f"  [X] No se encontró el archivo: {archivos['invasivos']}")
        
    print(f"==================================================\n")
    return datos_completos


# =====================================================================
# FUNCIÓN PARA CREAR EXCEL SEPARADOS
# =====================================================================
def exportar_a_excel(datos_completos, carpeta_origen):
    print("\n--- CREANDO ARCHIVOS EXCEL POR SERVICIO ---")
    
    fecha_carpeta = carpeta_origen.split(" ")[-1]
    carpeta_destino = f"Datos Procesados {fecha_carpeta}"
    os.makedirs(carpeta_destino, exist_ok=True)
    
    encabezados = [
        "CC PROFESIONAL", "SERVICIO", "FECHA", "CC PACIENTE", "TURNO", 
        "FECHA CREACION", "LIDER", "COORDINADOR", "GEOREFERENCIA", "ESTADO", "CRUCE"
    ]
    
    rutas_creadas = []

    for servicio, filas in datos_completos.items():
        if len(filas) > 0:
            df_final = pd.DataFrame(filas, columns=encabezados)
            nombre_archivo = f"{servicio.capitalize()}_Procesado_{fecha_carpeta}.xlsx"
            ruta_excel = os.path.join(carpeta_destino, nombre_archivo)
            
            df_final.to_excel(ruta_excel, index=False)
            rutas_creadas.append(ruta_excel)
            print(f"  ✓ {len(filas)} registros guardados en: {nombre_archivo}")
        else:
            print(f"  - No hay datos para crear Excel de: {servicio}")
            
    print(f"¡ÉXITO! Todos los archivos separados se guardaron en: {os.path.abspath(carpeta_destino)}")
    return rutas_creadas

if __name__ == "__main__":
    carpeta_prueba = "descargas control interno 2026-03-01" 
    if os.path.exists(carpeta_prueba):
        resultados = procesar_carpeta(carpeta_prueba)
        exportar_a_excel(resultados, carpeta_prueba)
    else:
        print("La carpeta de prueba no existe. ¡Pero la lógica está lista!")