# Archivo: procesar_datos.py
import os
import pandas as pd

# =====================================================================
# CONFIGURACIÓN: CABECERAS
# =====================================================================

HEADERS_ESTANDAR = [
    "CC PROFESIONAL",
    "SERVICIO",
    "FECHA",
    "CC PACIENTE",
    "TURNO",
    "FECHA CREACION",
    "LIDER",
    "COORDINADOR",
    "GEOREFERENCIA",
    "ESTADO",
    "CRUCE",
]

HEADERS_INVASIVOS = [
    "CC PROFESIONAL",
    "FECHA",
    "CC PACIENTE",
    "JORNADA",
    "FECHA CREACION",
    "LIDER",
    "COORDINADOR",
    "GEOREFERENCIA",
    "ESTADO",
]

HEADERS_RUTERO = [
    "FECHA",
    "DOCUMENTO PROFESIONAL",
    "PROFESIONAL",
    "ASUNTO",
    "DOCUMENTO PACIENTE",
    "PACIENTE",
    "TIPO",
    "ESTADO",
]


# =====================================================================
# HOMOLOGACIÓN RUTERO
# =====================================================================

def normalizar_tipo_rutero(valor):
    """
    Normaliza el texto del tipo de servicio.
    También intenta corregir textos dañados tipo:
    ENFERMERÃA -> ENFERMERÍA
    DÃA -> DÍA
    """
    if pd.isna(valor):
        return ""

    texto = str(valor).strip()

    try:
        texto = texto.encode("latin1").decode("utf-8")
    except Exception:
        pass

    texto = texto.upper()
    texto = " ".join(texto.split())

    return texto


HOMOLOGACION_RUTERO = {
    # ==============================================================
    # SERVICIOS QUE SE CONSERVAN EN RUTERO
    # ==============================================================

    "CUIDADOR 10 HORAS": {
        "tipo_2": "CUIDADOR 10 HORAS",
        "codigo": 1,
    },
    "CUIDADOR 12 HORAS DÍA": {
        "tipo_2": "CUIDADOR 12 HORAS DÍA",
        "codigo": 1,
    },
    "CUIDADOR 12 HORAS NOCHE": {
        "tipo_2": "CUIDADOR 12 HORAS NOCHE",
        "codigo": 1,
    },
    "CUIDADOR 6 HORAS": {
        "tipo_2": "CUIDADOR 6 HORAS",
        "codigo": 1,
    },
    "CUIDADOR 8 HORAS": {
        "tipo_2": "CUIDADOR 8 HORAS",
        "codigo": 1,
    },
    "CUIDADOR 9 HORAS": {
        "tipo_2": "CUIDADOR 9 HORAS",
        "codigo": 1,
    },
    "ENFERMERÍA 12 HORAS DÍA": {
        "tipo_2": "ENFERMERÍA 12 HORAS DÍA",
        "codigo": 1,
    },
    "ENFERMERIA 12 HORAS NOCHE": {
        "tipo_2": "ENFERMERIA 12 HORAS NOCHE",
        "codigo": 1,
    },
    "ENFERMERÍA 6 HORAS": {
        "tipo_2": "ENFERMERÍA 6 HORAS",
        "codigo": 1,
    },
    "ENFERMERÍA 8 HORAS": {
        "tipo_2": "ENFERMERÍA 8 HORAS",
        "codigo": 1,
    },
    "ENTRENAMIENTO 12 HORAS DIA": {
        "tipo_2": "ENTRENAMIENTO 12 HORAS DIA",
        "codigo": 1,
    },
    "ENTRENAMIENTO 12 HORAS NOCHE": {
        "tipo_2": "ENTRENAMIENTO 12 HORAS NOCHE",
        "codigo": 1,
    },
    "ENTRENAMIENTO 8 HORAS": {
        "tipo_2": "ENTRENAMIENTO 8 HORAS",
        "codigo": 1,
    },

    # ==============================================================
    # SERVICIOS QUE SE ELIMINAN DE RUTERO
    # ==============================================================

    "INYECCION O INFUSION DE MEDICAMENTOS": {
        "tipo_2": "INYECCION O INFUSION DE MEDICAMENTOS",
        "codigo": 0,
    },
    "MEDICINA GENERAL": {
        "tipo_2": "MEDICINA GENERAL",
        "codigo": 0,
    },
    "NUTRICION": {
        "tipo_2": "NUTRICION",
        "codigo": 0,
    },
    "VIDEOCONSULTA": {
        "tipo_2": "VIDEOCONSULTA",
        "codigo": 0,
    },
    "TERAPIA FISICA": {
        "tipo_2": "TERAPIA FISICA",
        "codigo": 0,
    },
    "TRABAJO SOCIAL": {
        "tipo_2": "TRABAJO SOCIAL",
        "codigo": 0,
    },
    "TELECONSULTA": {
        "tipo_2": "TELECONSULTA",
        "codigo": 0,
    },
    "TERAPIA FONOAUDIOLOGICA": {
        "tipo_2": "TERAPIA FONOAUDIOLOGICA",
        "codigo": 0,
    },
    "TERAPIA RESPIRATORIA": {
        "tipo_2": "TERAPIA RESPIRATORIA",
        "codigo": 0,
    },
    "TERAPIA OCUPACIONAL": {
        "tipo_2": "TERAPIA OCUPACIONAL",
        "codigo": 0,
    },
    "VALORACION TERAPIA FISICA": {
        "tipo_2": "VALORACION TERAPIA FISICA",
        "codigo": 0,
    },
    "VALORACION TERAPIA RESPIRATORIA": {
        "tipo_2": "VALORACION TERAPIA RESPIRATORIA",
        "codigo": 0,
    },
    "MEDICINA ESPECIALIZADA FISIATRIA": {
        "tipo_2": "MEDICINA ESPECIALIZADA FISIATRIA",
        "codigo": 0,
    },
    "PSICOLOGIA": {
        "tipo_2": "PSICOLOGIA",
        "codigo": 0,
    },
}

# =====================================================================
# UTILIDADES
# =====================================================================

def leer_csv_flexible(ruta_archivo):
    """
    Intenta leer el CSV con separador ';' y, si falla, con ','.
    """
    try:
        return pd.read_csv(ruta_archivo, sep=";", encoding="utf-8-sig", dtype=str)
    except Exception:
        return pd.read_csv(ruta_archivo, sep=",", encoding="utf-8-sig", dtype=str)


def formatear_fecha_columna(serie, formato_salida):
    """
    Convierte una columna de fechas a un formato específico.
    Si una fecha no se puede convertir, conserva el valor original.
    """
    fechas_dt = pd.to_datetime(serie, errors="coerce")

    return [
        limpia if pd.notna(limpia) and str(limpia) not in ("NaT", "nan", "") else cruda
        for limpia, cruda in zip(
            fechas_dt.dt.strftime(formato_salida).tolist(),
            serie.fillna("").astype(str).tolist(),
        )
    ]


def extraer_documento(serie):
    """
    Extrae solo los dígitos de una columna.
    """
    return serie.astype(str).str.extract(r"(\d+)", expand=False)


# =====================================================================
# FUNCIÓN 1: NOTA ENFERMERIA VENTILADOS
# =====================================================================

def procesar_nota_ventilados(ruta_archivo):
    print("  -> Procesando: Ventilados")

    df_raw = leer_csv_flexible(ruta_archivo)
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_ESTANDAR)

    df_target["SERVICIO"] = "VENTILADO"

    try:
        df_target["CC PROFESIONAL"] = extraer_documento(df_raw.iloc[:, 77])
    except Exception:
        pass

    try:
        df_target["FECHA"] = formatear_fecha_columna(df_raw.iloc[:, 1], "%d/%m/%Y")
    except Exception:
        pass

    try:
        df_target["CC PACIENTE"] = extraer_documento(df_raw.iloc[:, 3])
    except Exception:
        pass

    try:
        df_target["TURNO"] = df_raw.iloc[:, 21]
    except Exception:
        pass

    try:
        df_target["GEOREFERENCIA"] = df_raw.iloc[:, 78].fillna("").astype(str)
    except Exception:
        pass

    try:
        df_target["ESTADO"] = df_raw.iloc[:, 79].fillna("").astype(str)
    except Exception:
        pass

    return df_target.fillna("")


# =====================================================================
# FUNCIÓN 2: NOTA DE ENFERMERÍA NORMAL
# =====================================================================

def procesar_nota_enfermeria(ruta_archivo):
    print("  -> Procesando: Enfermería Normal")

    df_raw = leer_csv_flexible(ruta_archivo)
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_ESTANDAR)

    df_target["SERVICIO"] = "NOTA ENFERMERIA"

    try:
        df_target["CC PROFESIONAL"] = extraer_documento(df_raw.iloc[:, 44])
    except Exception:
        pass

    try:
        df_target["FECHA"] = formatear_fecha_columna(df_raw.iloc[:, 1], "%d/%m/%Y")
    except Exception:
        pass

    try:
        df_target["CC PACIENTE"] = extraer_documento(df_raw.iloc[:, 3])
    except Exception:
        pass

    try:
        df_target["TURNO"] = df_raw.iloc[:, 21]
    except Exception:
        pass

    try:
        df_target["GEOREFERENCIA"] = df_raw.iloc[:, 45].fillna("").astype(str)
    except Exception:
        pass

    try:
        df_target["ESTADO"] = df_raw.iloc[:, 46].fillna("").astype(str)
    except Exception:
        pass

    return df_target.fillna("")


# =====================================================================
# FUNCIÓN 3: NOTAS CUIDADOR (ACTIVIDADES BÁSICAS)
# =====================================================================

def procesar_cuidador_actividades(ruta_archivo):
    print("  -> Procesando: Actividades Básicas")

    df_raw = leer_csv_flexible(ruta_archivo)
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_ESTANDAR)

    df_target["SERVICIO"] = "CUIDADOR"

    try:
        df_target["CC PROFESIONAL"] = extraer_documento(df_raw.iloc[:, 35])
    except Exception:
        pass

    try:
        df_target["FECHA"] = formatear_fecha_columna(df_raw.iloc[:, 1], "%d/%m/%Y")
    except Exception:
        pass

    try:
        df_target["FECHA CREACION"] = formatear_fecha_columna(
            df_raw.iloc[:, 41],
            "%d/%m/%Y %H:%M",
        )
    except Exception:
        pass

    try:
        df_target["CC PACIENTE"] = extraer_documento(df_raw.iloc[:, 3])
    except Exception:
        pass

    try:
        df_target["TURNO"] = df_raw.iloc[:, 14]
    except Exception:
        pass

    try:
        df_target["GEOREFERENCIA"] = df_raw.iloc[:, 39].fillna("").astype(str)
    except Exception:
        pass

    try:
        df_target["ESTADO"] = df_raw.iloc[:, 40].fillna("").astype(str)
    except Exception:
        pass

    return df_target.fillna("")


# =====================================================================
# FUNCIÓN 4: NOTAS CUIDADOR (MEDIOS INVASIVOS)
# =====================================================================

def procesar_medios_invasivos(ruta_archivo):
    print("  -> Procesando: Medios Invasivos")

    df_raw = leer_csv_flexible(ruta_archivo)
    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_INVASIVOS)

    try:
        df_target["CC PROFESIONAL"] = extraer_documento(df_raw.iloc[:, 33])
    except Exception:
        pass

    try:
        df_target["FECHA"] = formatear_fecha_columna(df_raw.iloc[:, 1], "%d/%m/%Y")
    except Exception:
        pass

    try:
        df_target["FECHA CREACION"] = formatear_fecha_columna(
            df_raw.iloc[:, 39],
            "%d/%m/%Y %H:%M",
        )
    except Exception:
        pass

    try:
        df_target["CC PACIENTE"] = extraer_documento(df_raw.iloc[:, 3])
    except Exception:
        pass

    try:
        df_target["JORNADA"] = df_raw.iloc[:, 14]
    except Exception:
        pass

    try:
        df_target["GEOREFERENCIA"] = df_raw.iloc[:, 37].fillna("").astype(str)
    except Exception:
        pass

    try:
        df_target["ESTADO"] = df_raw.iloc[:, 38].fillna("").astype(str)
    except Exception:
        pass

    return df_target.fillna("")


# =====================================================================
# FUNCIÓN 5: REPORTE RUTERO
# =====================================================================

def procesar_rutero(ruta_archivo):
    print("  -> Procesando: Reporte Rutero")

    df_raw = leer_csv_flexible(ruta_archivo)

    try:
        tipos_crudos = df_raw.iloc[:, 15].fillna("").astype(str).str.strip()
        tipos_normalizados = tipos_crudos.apply(normalizar_tipo_rutero)

        codigos = tipos_normalizados.map(
            lambda tipo: HOMOLOGACION_RUTERO.get(tipo, {}).get("codigo")
        )

        estados_normalizados = (
            df_raw.iloc[:, 19]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )

        filas_iniciales = len(df_raw)

        # Se eliminan:
        # 1. Filas homologadas con CODIGO = 0.
        # 2. Filas cuyo ESTADO sea INACTIVO.
        mascara_codigo_cero = codigos.eq(0)
        mascara_estado_inactivo = estados_normalizados.eq("INACTIVO")
        mascara_eliminar = mascara_codigo_cero | mascara_estado_inactivo

        df_raw = df_raw.loc[~mascara_eliminar].copy()
        tipos_normalizados = tipos_normalizados.loc[~mascara_eliminar].copy()

        filas_eliminadas_codigo_cero = int(mascara_codigo_cero.sum())
        filas_eliminadas_inactivo = int(mascara_estado_inactivo.sum())

        df_raw = df_raw.reset_index(drop=True)
        tipos_normalizados = tipos_normalizados.reset_index(drop=True)

        filas_finales = len(df_raw)
        filas_eliminadas_total = filas_iniciales - filas_finales

        print(
            f"     Rutero depurado: {filas_eliminadas_total} filas eliminadas. "
            f"CODIGO = 0: {filas_eliminadas_codigo_cero}. "
            f"ESTADO = INACTIVO: {filas_eliminadas_inactivo}. "
            f"Filas restantes: {filas_finales}"
        )

        tipos_no_homologados = sorted(
            tipo
            for tipo in tipos_normalizados.unique()
            if tipo and tipo not in HOMOLOGACION_RUTERO
        )

        if tipos_no_homologados:
            print("     [ADVERTENCIA] Tipos de Rutero sin homologación:")
            for tipo in tipos_no_homologados:
                print(f"       - {tipo}")

    except Exception as e:
        print(f"     [ADVERTENCIA] No se pudo aplicar depuración Rutero: {e}")
        tipos_normalizados = pd.Series([""] * len(df_raw))

    df_target = pd.DataFrame(index=df_raw.index, columns=HEADERS_RUTERO)

    try:
        df_target["FECHA"] = formatear_fecha_columna(df_raw.iloc[:, 17], "%d/%m/%Y")
    except Exception:
        pass

    try:
        df_target["DOCUMENTO PROFESIONAL"] = extraer_documento(df_raw.iloc[:, 13])
    except Exception:
        pass

    try:
        df_target["PROFESIONAL"] = df_raw.iloc[:, 14].fillna("").astype(str).str.strip()
    except Exception:
        pass

    try:
        df_target["ASUNTO"] = df_raw.iloc[:, 16].fillna("").astype(str).str.strip()
    except Exception:
        pass

    try:
        df_target["DOCUMENTO PACIENTE"] = extraer_documento(df_raw.iloc[:, 1])
    except Exception:
        pass

    try:
        c1 = df_raw.iloc[:, 2].fillna("").astype(str)
        c2 = df_raw.iloc[:, 3].fillna("").astype(str)
        c3 = df_raw.iloc[:, 4].fillna("").astype(str)

        df_target["PACIENTE"] = (
            c1 + " " + c2 + " " + c3
        ).str.replace(r"\s+", " ", regex=True).str.strip()
    except Exception:
        pass

    try:
        df_target["TIPO"] = tipos_normalizados.map(
            lambda tipo: HOMOLOGACION_RUTERO.get(tipo, {}).get("tipo_2", tipo)
        )
    except Exception:
        pass

    try:
        df_target["ESTADO"] = df_raw.iloc[:, 19].fillna("").astype(str).str.strip()
    except Exception:
        pass

    return df_target.fillna("")

# =====================================================================
# FUNCIÓN MAESTRA
# =====================================================================

def procesar_carpeta(carpeta_base):
    print("\n==================================================")
    print(f" INICIANDO EXTRACCIÓN EN CARPETA: {carpeta_base}")
    print("==================================================")

    archivos = {
        "ventilados": "Nota_Enfermeria_Ventilados.csv",
        "enfermeria": "Nota_Enfermeria.csv",
        "actividades": "Notas_Cuidador_Actividades.csv",
        "invasivos": "Notas_Cuidador_Invasivos.csv",
        "rutero": "Reporte_Rutero.csv",
    }

    datos_completos = {
        "ventilados": None,
        "enfermeria": None,
        "actividades": None,
        "invasivos": None,
        "rutero": None,
    }

    rutas = {
        clave: os.path.join(carpeta_base, archivo)
        for clave, archivo in archivos.items()
    }

    if os.path.exists(rutas["ventilados"]):
        datos_completos["ventilados"] = procesar_nota_ventilados(rutas["ventilados"])
    else:
        print(f"  [X] No se encontró: {archivos['ventilados']}")

    if os.path.exists(rutas["enfermeria"]):
        datos_completos["enfermeria"] = procesar_nota_enfermeria(rutas["enfermeria"])
    else:
        print(f"  [X] No se encontró: {archivos['enfermeria']}")

    if os.path.exists(rutas["actividades"]):
        datos_completos["actividades"] = procesar_cuidador_actividades(rutas["actividades"])
    else:
        print(f"  [X] No se encontró: {archivos['actividades']}")

    if os.path.exists(rutas["invasivos"]):
        datos_completos["invasivos"] = procesar_medios_invasivos(rutas["invasivos"])
    else:
        print(f"  [X] No se encontró: {archivos['invasivos']}")

    if os.path.exists(rutas["rutero"]):
        datos_completos["rutero"] = procesar_rutero(rutas["rutero"])
    else:
        print(f"  [X] No se encontró: {archivos['rutero']}")

    print("==================================================\n")

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

    print(
        "¡ÉXITO! Todos los archivos separados se guardaron en: "
        f"{os.path.abspath(carpeta_destino)}"
    )

    return rutas_creadas


if __name__ == "__main__":
    carpeta_prueba = "descargas control interno 2026-03-01"

    if os.path.exists(carpeta_prueba):
        resultados = procesar_carpeta(carpeta_prueba)
        exportar_a_excel(resultados, carpeta_prueba)
    else:
        print("La carpeta de prueba no existe. La lógica está lista.")