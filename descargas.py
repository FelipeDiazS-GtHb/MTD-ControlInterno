# Archivo: descargas.py
import os
import calendar
import sys  
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# Si el código se está ejecutando como un .exe (frozen)
if getattr(sys, 'frozen', False):
    # Obligamos a Playwright a buscar el navegador dentro del .exe temporal
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = os.path.join(sys._MEIPASS, 'playwright', 'driver', 'package', '.local-browsers')
# =====================================================================

def esperar_pantalla_carga(page):
    page.wait_for_timeout(500) 
    overlay = page.locator(".blockUI.blockOverlay")
    try:
        if overlay.is_visible(): overlay.wait_for(state="hidden", timeout=0) 
    except Exception: pass
    page.wait_for_timeout(500) 

def ingresar_fecha(page, name_attr, fecha):
    campo = page.locator(f"input[name='{name_attr}']")
    campo.wait_for(state="visible")
    campo.evaluate(f"el => el.value = '{fecha}'")
    campo.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
    campo.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
    try: page.evaluate(f"window.$('input[name=\"{name_attr}\"]').trigger('change')")
    except: pass
    esperar_pantalla_carga(page)

def descargar_reporte(page, tipo_rep, plantilla, nombre_archivo, f_inicio, f_fin, carpeta):
    print(f"-> Procesando {nombre_archivo}...")
    if tipo_rep:
        page.locator("#report_type").select_option(tipo_rep)
        esperar_pantalla_carga(page)
    if plantilla:
        page.locator("#template").select_option(plantilla)
        esperar_pantalla_carga(page)

    ingresar_fecha(page, "from", f_inicio)
    ingresar_fecha(page, "to", f_fin)

    page.wait_for_timeout(500) 
    chk_prox = page.locator("#proximity")
    try:
        if chk_prox.is_visible() and not chk_prox.is_checked():
            chk_prox.check(force=True)
            print("   [INFO] Checkbox de proximidad marcado.")
    except Exception: pass
            
    esperar_pantalla_carga(page)

    try:
        print("   Generando archivo (Paciencia, puede tardar)...")
        with page.expect_download(timeout=0) as download_info:
            page.get_by_role("button", name="Generar").click(force=True)
        descarga = download_info.value
        ruta_final = os.path.join(carpeta, f"{nombre_archivo}.csv")
        descarga.save_as(ruta_final)
        print(f"   ✓ Descarga exitosa: {nombre_archivo}.csv")
    except Exception as e:
        print(f"   × Error descargando {nombre_archivo}: {e}")
    esperar_pantalla_carga(page)

def ejecutar_descargas(usuario, password, anio, mes):
    """Esta es la función principal que será llamada desde afuera"""
    _, ultimo_dia = calendar.monthrange(anio, mes)
    f_inicio = f"{anio}-{mes:02d}-01"
    f_fin = f"{anio}-{mes:02d}-{ultimo_dia}"
    
    carpeta = f"descargas control interno {f_inicio}"
    os.makedirs(carpeta, exist_ok=True)

    with sync_playwright() as p:
        print("\n[Abriendo navegador...]")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(accept_downloads=True)
        
        page.set_default_timeout(0)
        page.set_default_navigation_timeout(0)

        print(f"[Iniciando sesión como {usuario}...]")
        page.goto("https://saludgestiona.com/business/signin/MTAwNQ==", wait_until="networkidle")
        
        page.locator("input[placeholder*='Documento']").fill(usuario)
        page.locator("input[placeholder*='Contraseña']").fill(password)
        page.get_by_role("button", name="Ingresar").click()

        page.wait_for_load_state("networkidle")
        esperar_pantalla_carga(page)
        
        page.goto("https://saludgestiona.com/business/reports", wait_until="networkidle")
        esperar_pantalla_carga(page)

        print("\n--- SECCIÓN: REGISTROS ---")
        page.locator("a[data-category='2']").click(force=True)
        esperar_pantalla_carga(page)

        descargar_reporte(page, "7", "2", "Notas_Cuidador_Actividades", f_inicio, f_fin, carpeta)
        descargar_reporte(page, "7", "3", "Notas_Cuidador_Invasivos", f_inicio, f_fin, carpeta)
        descargar_reporte(page, "9", "59", "Nota_Enfermeria", f_inicio, f_fin, carpeta)
        descargar_reporte(page, "9", "60", "Nota_Enfermeria_Ventilados", f_inicio, f_fin, carpeta)

        print("\n--- SECCIÓN: RUTERO ---")
        page.goto("https://saludgestiona.com/business/reports", wait_until="networkidle")
        esperar_pantalla_carga(page)
        
        page.locator("a[data-category='6']").click(force=True)
        esperar_pantalla_carga(page)
        
        descargar_reporte(page, "4", None, "Reporte_Rutero", f_inicio, f_fin, carpeta)

        print(f"\n¡DESCARGAS FINALIZADAS! Archivos en: {os.path.abspath(carpeta)}")
        browser.close()
        
    # Devolvemos el nombre de la carpeta para que el procesador sepa dónde buscar
    return carpeta