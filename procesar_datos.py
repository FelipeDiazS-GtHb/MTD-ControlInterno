import pandas as pd
import os

# =====================================================================
# CONFIGURACIÓN: CABECERAS Y DICCIONARIOS DE HOMOLOGACIÓN
# =====================================================================
HEADERS_ESTANDAR = ["CC PROFESIONAL", "SERVICIO", "FECHA", "CC PACIENTE", "TURNO", "FECHA CREACION", "LIDER", "COORDINADOR", "GEOREFERENCIA", "ESTADO", "CRUCE"]
HEADERS_INVASIVOS = ["CC PROFESIONAL", "FECHA", "CC PACIENTE", "JORNADA", "FECHA CREACION", "LIDER", "COORDINADOR", "GEOREFERENCIA", "ESTADO"]
HEADERS_RUTERO = ["FECHA", "DOCUMENTO PROFESIONAL", "PROFESIONAL", "ASUNTO", "DOCUMENTO PACIENTE", "PACIENTE", "TIPO", "ESTADO"]

HOMOLOGACION_TIPO = {
    "CUIDADOR 10 HORAS": "CUIDADOR 10 HORAS",
    "CUIDADOR 12 HORAS DÃ\x8dA": "CUIDADOR 12 HORAS DÍA",
    "CUIDADOR 12 HORAS DÍA": "CUIDADOR 12 HORAS DÍA",
    "CUIDADOR 12 HORAS NOCHE": "CUIDADOR 12 HORAS NOCHE",
    "CUIDADOR 6 HORAS": "CUIDADOR 6 HORAS",
    "CUIDADOR 8 HORAS": "CUIDADOR 8 HORAS",
    "CUIDADOR 9 HORAS": "CUIDADOR 9 HORAS",
    "ENFERMERÃ\x8dA 12 HORAS DÃ\x8dA": "ENFERMERÍA 12 HORAS DÍA",
    "ENFERMERÍA 12 HORAS DÍA": "ENFERMERÍA 12 HORAS DÍA",
    "ENFERMERIA 12 HORAS NOCHE": "ENFERMERIA 12 HORAS NOCHE",
    "ENFERMERÃ\x8dA 6 HORAS": "ENFERMERÍA 6 HORAS",
    "ENFERMERÍA 6 HORAS": "ENFERMERÍA 6 HORAS",
    "ENFERMERÃ\x8dA 8 HORAS": "ENFERMERÍA 8 HORAS",
    "ENFERMERÍA 8 HORAS": "ENFERMERÍA 8 HORAS",
    "ENTRENAMIENTO 12 HORAS DIA": "ENTRENAMIENTO 12 HORAS DIA",
    "ENTRENAMIENTO 12 HORAS NOCHE": "ENTRENAMIENTO 12 HORAS NOCHE",
    "ENTRENAMIENTO 8 HORAS": "ENTRENAMIENTO 8 HORAS",
    "INYECCION O INFUSION DE MEDICAMENTOS": "INYECCION O INFUSION DE MEDICAMENTOS",
    "MEDICINA GENERAL": "MEDICINA GENERAL",
    "NUTRICION": "NUTRICION",
    "PSICOLOGIA": "PSICOLOGIA",
    "TERAPIA FISICA": "TERAPIA FISICA",
    "TERAPIA FONOAUDIOLOGICA": "TERAPIA FONOAUDIOLOGICA",
    "TERAPIA OCUPACIONAL": "TERAPIA OCUPACIONAL",
    "TERAPIA RESPIRATORIA": "TERAPIA RESPIRATORIA",
    "VALORACION TERAPIA FISICA": "VALORACION TERAPIA FISICA",
    "VALORACION TERAPIA RESPIRATORIA": "VALORACION TERAPIA RESPIRATORIA",
    "VIDEOCONSULTA": "VIDEOCONSULTA"
}

# =====================================================================
# FUNCIÓN 1: NOTA ENFERMERIA VENTILADOS
# =====================================================================
def procesar_nota_ventilados(ruta_archivo):
    print(f"  -> Procesando: Ventilados")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_ESTANDAR)
    df_target["SERVICIO"] = "VENTILADO"
    
    try: df_target["CC PROFESIONAL"] = df_raw.iloc[:, 77].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, 1], errors='coerce')
        df_target["FECHA"] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(fechas_dt.dt.strftime('%d/%m/%Y').tolist(), df_raw.iloc[:, 1].fillna("").astype(str).tolist())]
    except Exception: pass
    
    try: df_target["CC PACIENTE"] = df_raw.iloc[:, 3].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target["TURNO"] = df_raw.iloc[:, 21]
    except Exception: pass
    try: df_target["GEOREFERENCIA"] = df_raw.iloc[:, 78].fillna("").astype(str)
    except Exception: pass
    try: df_target["ESTADO"] = df_raw.iloc[:, 79].fillna("").astype(str)
    except Exception: pass

    return df_target.fillna("")

# =====================================================================
# FUNCIÓN 2: NOTA DE ENFERMERÍA NORMAL
# =====================================================================
def procesar_nota_enfermeria(ruta_archivo):
    print(f"  -> Procesando: Enfermería Normal")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_ESTANDAR)
    df_target["SERVICIO"] = "NOTA ENFERMERIA" 
    
    try: df_target["CC PROFESIONAL"] = df_raw.iloc[:, 44].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, 1], errors='coerce')
        df_target["FECHA"] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(fechas_dt.dt.strftime('%d/%m/%Y').tolist(), df_raw.iloc[:, 1].fillna("").astype(str).tolist())]
    except Exception: pass
    
    try: df_target["CC PACIENTE"] = df_raw.iloc[:, 3].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target["TURNO"] = df_raw.iloc[:, 21]
    except Exception: pass
    try: df_target["GEOREFERENCIA"] = df_raw.iloc[:, 45].fillna("").astype(str)
    except Exception: pass
    try: df_target["ESTADO"] = df_raw.iloc[:, 46].fillna("").astype(str)
    except Exception: pass

    return df_target.fillna("")

# =====================================================================
# FUNCIÓN 3: NOTAS CUIDADOR (ACTIVIDADES BÁSICAS)
# =====================================================================
def procesar_cuidador_actividades(ruta_archivo):
    print(f"  -> Procesando: Actividades Básicas")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_ESTANDAR)
    df_target["SERVICIO"] = "CUIDADOR" 
    
    try: df_target["CC PROFESIONAL"] = df_raw.iloc[:, 35].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, 1], errors='coerce')
        df_target["FECHA"] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(fechas_dt.dt.strftime('%d/%m/%Y').tolist(), df_raw.iloc[:, 1].fillna("").astype(str).tolist())]
    except Exception: pass

    try: 
        fechas_crea_dt = pd.to_datetime(df_raw.iloc[:, 41], errors='coerce')
        df_target["FECHA CREACION"] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(fechas_crea_dt.dt.strftime('%d/%m/%Y %H:%M').tolist(), df_raw.iloc[:, 41].fillna("").astype(str).tolist())]
    except Exception: pass
    
    try: df_target["CC PACIENTE"] = df_raw.iloc[:, 3].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target["TURNO"] = df_raw.iloc[:, 14]
    except Exception: pass
    try: df_target["GEOREFERENCIA"] = df_raw.iloc[:, 39].fillna("").astype(str) 
    except Exception: pass
    try: df_target["ESTADO"] = df_raw.iloc[:, 40].fillna("").astype(str) 
    except Exception: pass

    return df_target.fillna("")

# =====================================================================
# FUNCIÓN 4: NOTAS CUIDADOR (MEDIOS INVASIVOS)
# =====================================================================
def procesar_medios_invasivos(ruta_archivo):
    print(f"  -> Procesando: Medios Invasivos")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_INVASIVOS)
    
    try: df_target["CC PROFESIONAL"] = df_raw.iloc[:, 33].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, 1], errors='coerce')
        df_target["FECHA"] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(fechas_dt.dt.strftime('%d/%m/%Y').tolist(), df_raw.iloc[:, 1].fillna("").astype(str).tolist())]
    except Exception: pass

    try: 
        fechas_crea_dt = pd.to_datetime(df_raw.iloc[:, 39], errors='coerce')
        df_target["FECHA CREACION"] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(fechas_crea_dt.dt.strftime('%d/%m/%Y %H:%M').tolist(), df_raw.iloc[:, 39].fillna("").astype(str).tolist())]
    except Exception: pass
    
    try: df_target["CC PACIENTE"] = df_raw.iloc[:, 3].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass
    try: df_target["JORNADA"] = df_raw.iloc[:, 14]
    except Exception: pass
    try: df_target["GEOREFERENCIA"] = df_raw.iloc[:, 37].fillna("").astype(str) 
    except Exception: pass
    try: df_target["ESTADO"] = df_raw.iloc[:, 38].fillna("").astype(str) 
    except Exception: pass

    return df_target.fillna("")

# =====================================================================
# FUNCIÓN 5: REPORTE RUTERO (NUEVO)
# =====================================================================
def procesar_rutero(ruta_archivo):
    print(f"  -> Procesando: Reporte Rutero")
    try: df_raw = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8-sig', dtype=str)
    except: df_raw = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig', dtype=str)
    
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_RUTERO)
    
    try: 
        fechas_dt = pd.to_datetime(df_raw.iloc[:, 17], errors='coerce')
        df_target["FECHA"] = [l if pd.notna(l) and str(l) not in ('NaT', 'nan', '') else c for l, c in zip(fechas_dt.dt.strftime('%d/%m/%Y').tolist(), df_raw.iloc[:, 17].fillna("").astype(str).tolist())]
    except Exception: pass

    try: df_target["DOCUMENTO PROFESIONAL"] = df_raw.iloc[:, 13].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass

    try: df_target["PROFESIONAL"] = df_raw.iloc[:, 14].fillna("").astype(str).str.strip()
    except Exception: pass

    try: df_target["ASUNTO"] = df_raw.iloc[:, 16].fillna("").astype(str).str.strip()
    except Exception: pass

    try: df_target["DOCUMENTO PACIENTE"] = df_raw.iloc[:, 1].astype(str).str.extract(r'(\d+)', expand=False)
    except Exception: pass

    try: 
        c1 = df_raw.iloc[:, 2].fillna("").astype(str)
        c2 = df_raw.iloc[:, 3].fillna("").astype(str)
        c3 = df_raw.iloc[:, 4].fillna("").astype(str)
        df_target["PACIENTE"] = (c1 + " " + c2 + " " + c3).str.replace(r'\s+', ' ', regex=True).str.strip()
    except Exception: pass

    try: 
        tipos_crudos = df_raw.iloc[:, 15].fillna("").astype(str).str.strip()
        df_target["TIPO"] = tipos_crudos.map(HOMOLOGACION_TIPO).fillna(tipos_crudos)
    except Exception: pass

    try: df_target["ESTADO"] = df_raw.iloc[:, 19].fillna("").astype(str).str.strip()
    except Exception: pass

    return df_target.fillna("")

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
        "invasivos": "Notas_Cuidador_Invasivos.csv",
        "rutero": "Reporte_Rutero.csv"
    }
    
    datos_completos = {"ventilados": None, "enfermeria": None, "actividades": None, "invasivos": None, "rutero": None}

    rutas = {k: os.path.join(carpeta_base, v) for k, v in archivos.items()}

    if os.path.exists(rutas["ventilados"]): datos_completos["ventilados"] = procesar_nota_ventilados(rutas["ventilados"])
    else: print(f"  [X] No se encontró: {archivos['ventilados']}")

    if os.path.exists(rutas["enfermeria"]): datos_completos["enfermeria"] = procesar_nota_enfermeria(rutas["enfermeria"])
    else: print(f"  [X] No se encontró: {archivos['enfermeria']}")

    if os.path.exists(rutas["actividades"]): datos_completos["actividades"] = procesar_cuidador_actividades(rutas["actividades"])
    else: print(f"  [X] No se encontró: {archivos['actividades']}")

    if os.path.exists(rutas["invasivos"]): datos_completos["invasivos"] = procesar_medios_invasivos(rutas["invasivos"])
    else: print(f"  [X] No se encontró: {archivos['invasivos']}")

    if os.path.exists(rutas["rutero"]): datos_completos["rutero"] = procesar_rutero(rutas["rutero"])
    else: print(f"  [X] No se encontró: {archivos['rutero']}")
        
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
    
    rutas_creadas = []

    for servicio, df_final in datos_completos.items():
        if df_final is not None and not df_final.empty:
            nombre_archivo = f"{servicio.capitalize()}_Procesado_{fecha_carpeta}.xlsx"
            ruta_excel = os.path.join(carpeta_destino, nombre_archivo)
            
            df_final.to_excel(ruta_excel, index=False)
            rutas_creadas.append(ruta_excel)
            print(f"  ✓ {len(df_final)} registros guardados en: {nombre_archivo}")
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