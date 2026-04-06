import os
import calendar
from playwright.sync_api import sync_playwright

def obtener_datos():
    print("--- AUTOMATIZACIÓN DE DESCARGAS ---")
    usuario = input("Usuario (Documento): ")
    password = input("Contraseña: ")
    
    anio = int(input("Año (Ej: 2026): "))
    mes = int(input("Mes (Ej: 3): "))
    
    _, ultimo_dia = calendar.monthrange(anio, mes)
    f_inicio = f"{anio}-{mes:02d}-01"
    f_fin = f"{anio}-{mes:02d}-{ultimo_dia}"
    
    carpeta = f"descargas control interno {f_inicio}"
    os.makedirs(carpeta, exist_ok=True)
    
    return usuario, password, f_inicio, f_fin, carpeta

def esperar_pantalla_carga(page):
    """Espera a que el bloqueador gris de jQuery (.blockUI) desaparezca."""
    page.wait_for_timeout(500) # Pequeño margen para que la web lance la animación
    overlay = page.locator(".blockUI.blockOverlay")
    try:
        if overlay.is_visible():
            # timeout=0 significa que esperará horas si es necesario
            overlay.wait_for(state="hidden", timeout=0) 
    except Exception:
        pass
    page.wait_for_timeout(500) # Margen de seguridad post-carga

def ingresar_fecha(page, name_attr, fecha):
    """Ingresa la fecha de forma segura y neutraliza el calendario visual."""
    campo = page.locator(f"input[name='{name_attr}']")
    campo.wait_for(state="visible")
    
    # 1. Inyectamos el valor directamente con JavaScript para no despertar al popup
    campo.evaluate(f"el => el.value = '{fecha}'")
    
    # 2. Disparamos los eventos nativos para que la página registre el cambio internamente
    campo.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
    campo.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
    
    # 3. Disparamos el evento de jQuery (Vital para que Salud Gestiona habilite la 2da fecha)
    try:
        page.evaluate(f"window.$('input[name=\"{name_attr}\"]').trigger('change')")
    except:
        pass
        
    # Esperamos a que la página procese el cambio y quite cualquier pantalla de carga
    esperar_pantalla_carga(page)

def descargar_reporte(page, tipo_rep, plantilla, nombre_archivo, f_inicio, f_fin, carpeta, prox=False):
    print(f"-> Procesando {nombre_archivo}...")
    
    # 1. Seleccionar opciones
    if tipo_rep:
        page.locator("#report_type").select_option(tipo_rep)
        esperar_pantalla_carga(page)
        
    if plantilla:
        page.locator("#template").select_option(plantilla)
        esperar_pantalla_carga(page)

    # 2. Llenar fechas usando el script anti-calendario
    ingresar_fecha(page, "from", f_inicio)
    ingresar_fecha(page, "to", f_fin)

    # 3. Marcar o desmarcar proximidad
    chk_prox = page.locator("#proximity")
    if prox:
        if chk_prox.is_visible() and not chk_prox.is_checked():
            chk_prox.check(force=True)
    else:
        if chk_prox.is_visible() and chk_prox.is_checked():
            chk_prox.uncheck(force=True)
            
    esperar_pantalla_carga(page)

    # 4. Generar y Descargar
    try:
        print("   Generando archivo (Paciencia, puede tardar)...")
        with page.expect_download(timeout=0) as download_info:
            page.get_by_role("button", name="Generar").click(force=True)
            
        descarga = download_info.value
        # Guardamos el archivo con el nombre que nosotros le dimos
        ruta_final = os.path.join(carpeta, f"{nombre_archivo}.csv")
        descarga.save_as(ruta_final)
        print(f"   ✓ Descarga exitosa: {nombre_archivo}.csv")
    except Exception as e:
        print(f"   × Error descargando {nombre_archivo}: {e}")
        
    esperar_pantalla_carga(page)

def iniciar():
    user, pwd, f_inicio, f_fin, carpeta = obtener_datos()
    
    with sync_playwright() as p:
        print("\n[Abriendo navegador...]")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(accept_downloads=True)
        
        # Eliminamos los límites de tiempo globales
        page.set_default_timeout(0)
        page.set_default_navigation_timeout(0)

        print(f"[Iniciando sesión como {user}...]")
        
        # --- CARGA COMPLETA Y SEGURA DEL LOGIN ---
        page.goto("https://saludgestiona.com/business/signin/MTAwNQ==", wait_until="networkidle")
        
        # Localizamos los campos
        campo_usuario = page.locator("input[placeholder*='Documento']")
        campo_pass = page.locator("input[placeholder*='Contraseña']")
        btn_ingresar = page.get_by_role("button", name="Ingresar")

        # ESPERA EXPLÍCITA: No avanzar hasta que la caja de texto exista y esté lista
        campo_usuario.wait_for(state="visible")
        page.wait_for_timeout(1000) # Respiro simulando comportamiento humano

        campo_usuario.fill(user)
        page.wait_for_timeout(300)
        campo_pass.fill(pwd)
        page.wait_for_timeout(500)
        
        btn_ingresar.click()
        # ------------------------------------------

        print("   Esperando a que cargue el dashboard principal...")
        page.wait_for_load_state("networkidle")
        esperar_pantalla_carga(page)
        
        print("[Navegando a Módulo de Reportes...]")
        page.goto("https://saludgestiona.com/business/reports", wait_until="networkidle")
        esperar_pantalla_carga(page)

        # --- REGISTROS ---
        print("\n--- SECCIÓN: REGISTROS ---")
        btn_registros = page.locator("a[data-category='2']")
        btn_registros.wait_for(state="visible")
        btn_registros.click(force=True)
        esperar_pantalla_carga(page)

        descargar_reporte(page, "7", "2", "Notas_Cuidador_Actividades", f_inicio, f_fin, carpeta)
        descargar_reporte(page, "7", "3", "Notas_Cuidador_Invasivos", f_inicio, f_fin, carpeta)
        descargar_reporte(page, "9", "59", "Nota_Enfermeria", f_inicio, f_fin, carpeta, prox=True)
        descargar_reporte(page, "9", "60", "Nota_Enfermeria_Ventilados", f_inicio, f_fin, carpeta, prox=True)

        # --- RUTERO ---
        print("\n--- SECCIÓN: RUTERO ---")
        page.goto("https://saludgestiona.com/business/reports", wait_until="networkidle")
        esperar_pantalla_carga(page)
        
        btn_rutero = page.locator("a[data-category='6']")
        btn_rutero.wait_for(state="visible")
        btn_rutero.click(force=True)
        esperar_pantalla_carga(page)
        
        descargar_reporte(page, "4", None, "Reporte_Rutero", f_inicio, f_fin, carpeta)

        print(f"\n¡PROCESO FINALIZADO! Archivos guardados en: {os.path.abspath(carpeta)}")
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    try:
        iniciar()
    except KeyboardInterrupt:
        print("\nProceso cancelado por el usuario.")