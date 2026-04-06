import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def conectar_google_sheets(url_sheet):
    """Establece la conexión con la API de Google Sheets."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Reemplaza 'tus_credenciales.json' con el nombre de tu archivo descargado de Google Cloud
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
    client = gspread.authorize(creds)
    return client.open_by_url(url_sheet)

def procesar_y_subir(archivo_path, hoja_objetivo, sheet_doc):
    """Lee el CSV, lo limpia y lo sube a la pestaña indicada."""
    if not os.path.exists(archivo_path):
        print(f"× Archivo no encontrado: {archivo_path}")
        return

    print(f"-> Procesando {archivo_path} para la hoja '{hoja_objetivo}'...")
    
    # Leer el CSV (ajustar el separador si es necesario, usualmente ';' en estos reportes)
    try:
        df = pd.read_csv(archivo_path, sep=';', encoding='utf-8')
    except:
        df = pd.read_csv(archivo_path, sep=',', encoding='utf-8') # Intento con coma si falla

    # Limpieza básica: quitar valores nulos para que no den error en Sheets
    df = df.fillna("")

    # Convertir el DataFrame a una lista de listas (formato que entiende gspread)
    datos_a_subir = df.values.tolist()

    if datos_a_subir:
        try:
            worksheet = sheet_doc.worksheet(hoja_objetivo)
            # append_rows añade al final. USER_ENTERED permite que Sheets reconozca fechas y números
            worksheet.append_rows(datos_a_subir, value_input_option='USER_ENTERED')
            print(f"   ✓ ¡Datos subidos con éxito a {hoja_objetivo}!")
        except gspread.exceptions.WorksheetNotFound:
            print(f"   × Error: No se encontró la pestaña '{hoja_objetivo}' en el Sheet.")
    else:
        print(f"   ! El archivo {archivo_path} estaba vacío.")

def ejecutar_limpieza_y_carga(carpeta_soportes, url_google_sheet):
    """Función maestra para coordinar las subidas."""
    
    # 1. Conectar al documento
    print("\n[INFO] Conectando a Google Sheets...")
    documento = conectar_google_sheets(url_google_sheet)

    # 2. Definir mapeo de archivos según lo que descargamos en el paso anterior
    # Ajustamos los nombres de los archivos según el 'nombre_log' del script previo
    mapeo = {
        "Reporte Notas.csv": "NOTA ENFERMERIA VENTILADOS",
        "Reporte Formularios A.csv": "NOTAS CUIDADOR ACTIVIDADES BASICAS",
        "Reporte Formularios B.csv": "MEDIOS INVASIVOS"
    }

    for nombre_archivo, nombre_hoja in mapeo.items():
        ruta_completa = os.path.join(carpeta_soportes, nombre_archivo)
        
        # Si el nombre del archivo es variable (porque trae fecha), buscamos por patrón:
        # Aquí una lógica para encontrar el archivo si el nombre no es exacto
        archivos_en_carpeta = os.listdir(carpeta_soportes)
        archivo_encontrado = None
        
        if "Notas" in nombre_archivo:
            archivo_encontrado = next((f for f in archivos_en_carpeta if "Formulario" in f and "60" in f), None)
        elif "Formularios A" in nombre_archivo:
            archivo_encontrado = next((f for f in archivos_en_carpeta if "Formulario" in f and "2" in f), None)
        elif "Formularios B" in nombre_archivo:
            archivo_encontrado = next((f for f in archivos_en_carpeta if "Formulario" in f and "3" in f), None)

        if archivo_encontrado:
            procesar_y_subir(os.path.join(carpeta_soportes, archivo_encontrado), nombre_hoja, documento)
        else:
            print(f"× No se pudo localizar el archivo para {nombre_hoja}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Estos datos idealmente vendrán del input del usuario o del script de Playwright
    mi_carpeta = "descargas control interno 2026-03-31" # Ejemplo
    mi_url_sheet = input("Pega aquí el URL de tu Google Sheet: ")
    
    ejecutar_limpieza_y_carga(mi_carpeta, mi_url_sheet)