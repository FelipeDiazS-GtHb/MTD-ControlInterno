# Archivo: descargas.py
import os
import calendar
import sys
import csv
from typing import Any, Dict, List, Optional


# =====================================================================
# TRUCO MAESTRO PARA PYINSTALLER + PLAYWRIGHT (SOLO CHROMIUM)
# =====================================================================
if getattr(sys, "frozen", False):
    # En el .exe, buscará Chromium dentro del paquete generado por PyInstaller
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(sys._MEIPASS, "Navegador")
else:
    # Para ejecución normal en desarrollo
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "Navegador"
# =====================================================================


from playwright.sync_api import sync_playwright


DEFAULT_TIMEOUT_MS = 120_000          # 2 minutos para acciones normales
DOWNLOAD_TIMEOUT_MS = 600_000         # 10 minutos para descarga de reportes pesados
RUTERO_COLUMNAS_MINIMAS = 20          # El parser usa hasta la columna índice 19


REPORTES_ESPERADOS = {
    "Notas_Cuidador_Actividades": {
        "archivo": "Notas_Cuidador_Actividades.csv",
        "obligatorio": False,
        "min_columnas": 42,
    },
    "Notas_Cuidador_Invasivos": {
        "archivo": "Notas_Cuidador_Invasivos.csv",
        "obligatorio": False,
        "min_columnas": 40,
    },
    "Nota_Enfermeria": {
        "archivo": "Nota_Enfermeria.csv",
        "obligatorio": False,
        "min_columnas": 47,
    },
    "Nota_Enfermeria_Ventilados": {
        "archivo": "Nota_Enfermeria_Ventilados.csv",
        "obligatorio": False,
        "min_columnas": 80,
    },
    "Reporte_Rutero": {
        "archivo": "Reporte_Rutero.csv",
        "obligatorio": True,
        "min_columnas": RUTERO_COLUMNAS_MINIMAS,
    },
}


def esperar_pantalla_carga(page):
    page.wait_for_timeout(500)
    overlay = page.locator(".blockUI.blockOverlay")
    try:
        if overlay.is_visible():
            overlay.wait_for(state="hidden", timeout=DEFAULT_TIMEOUT_MS)
    except Exception:
        pass
    page.wait_for_timeout(500)


def ingresar_fecha(page, name_attr, fecha):
    campo = page.locator(f"input[name='{name_attr}']")
    campo.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
    campo.evaluate(f"el => el.value = '{fecha}'")
    campo.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
    campo.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
    try:
        page.evaluate(f"window.$('input[name=\"{name_attr}\"]').trigger('change')")
    except Exception:
        pass
    esperar_pantalla_carga(page)


def _detectar_columnas_csv(ruta_archivo: str) -> int:
    """
    Lee la primera fila útil del CSV y devuelve cuántas columnas detecta.
    Prueba primero ';' porque los reportes actuales suelen salir así, y luego ','.
    """
    if not os.path.exists(ruta_archivo) or os.path.getsize(ruta_archivo) == 0:
        return 0

    for separador in (";", ","):
        try:
            with open(ruta_archivo, "r", encoding="utf-8-sig", newline="") as archivo:
                lector = csv.reader(archivo, delimiter=separador)
                for fila in lector:
                    if fila and any(str(celda).strip() for celda in fila):
                        return len(fila)
        except Exception:
            continue

    return 0


def validar_archivo_descargado(
    ruta_archivo: str,
    nombre_archivo: str,
    min_columnas: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Valida existencia, tamaño y estructura mínima del CSV descargado.
    """
    resultado = {
        "nombre": nombre_archivo,
        "ruta": ruta_archivo,
        "existe": os.path.exists(ruta_archivo),
        "bytes": 0,
        "columnas_detectadas": 0,
        "ok": False,
        "error": None,
    }

    if not resultado["existe"]:
        resultado["error"] = "El archivo no existe después de la descarga."
        return resultado

    resultado["bytes"] = os.path.getsize(ruta_archivo)

    if resultado["bytes"] <= 0:
        resultado["error"] = "El archivo existe, pero está vacío."
        return resultado

    columnas = _detectar_columnas_csv(ruta_archivo)
    resultado["columnas_detectadas"] = columnas

    if min_columnas is not None and columnas < min_columnas:
        resultado["error"] = (
            f"Estructura inválida: se detectaron {columnas} columnas, "
            f"pero se esperaban al menos {min_columnas}."
        )
        return resultado

    resultado["ok"] = True
    return resultado


def descargar_reporte(page, tipo_rep, plantilla, nombre_archivo, f_inicio, f_fin, carpeta):
    """
    Descarga un reporte y devuelve un resultado estructurado.
    Ya no oculta errores: el llamador decide si el flujo debe continuar o detenerse.
    """
    print(f"-> Procesando {nombre_archivo}...")

    config_reporte = REPORTES_ESPERADOS.get(nombre_archivo, {})
    ruta_final = os.path.join(carpeta, f"{nombre_archivo}.csv")

    resultado = {
        "nombre": nombre_archivo,
        "archivo": f"{nombre_archivo}.csv",
        "ruta": ruta_final,
        "ok": False,
        "bytes": 0,
        "columnas_detectadas": 0,
        "error": None,
        "obligatorio": bool(config_reporte.get("obligatorio", False)),
    }

    try:
        if tipo_rep:
            page.locator("#report_type").select_option(tipo_rep, timeout=DEFAULT_TIMEOUT_MS)
            esperar_pantalla_carga(page)

        if plantilla:
            page.locator("#template").select_option(plantilla, timeout=DEFAULT_TIMEOUT_MS)
            esperar_pantalla_carga(page)

        ingresar_fecha(page, "from", f_inicio)
        ingresar_fecha(page, "to", f_fin)

        page.wait_for_timeout(500)

        chk_prox = page.locator("#proximity")
        try:
            if chk_prox.is_visible(timeout=5_000) and not chk_prox.is_checked():
                chk_prox.check(force=True, timeout=DEFAULT_TIMEOUT_MS)
                print("   [INFO] Checkbox de proximidad marcado.")
        except Exception:
            pass

        esperar_pantalla_carga(page)

        print("   Generando archivo. Puede tardar varios minutos...")

        with page.expect_download(timeout=DOWNLOAD_TIMEOUT_MS) as download_info:
            page.get_by_role("button", name="Generar").click(
                force=True,
                timeout=DEFAULT_TIMEOUT_MS,
            )

        descarga = download_info.value
        descarga.save_as(ruta_final)

        validacion = validar_archivo_descargado(
            ruta_final,
            nombre_archivo,
            min_columnas=config_reporte.get("min_columnas"),
        )

        resultado.update({
            "ok": validacion["ok"],
            "bytes": validacion["bytes"],
            "columnas_detectadas": validacion["columnas_detectadas"],
            "error": validacion["error"],
        })

        if resultado["ok"]:
            print(
                f"   ✓ Descarga exitosa: {nombre_archivo}.csv "
                f"({resultado['bytes']} bytes, "
                f"{resultado['columnas_detectadas']} columnas)"
            )
        else:
            print(
                f"   × Descarga inválida: {nombre_archivo}.csv -> "
                f"{resultado['error']}"
            )

    except Exception as e:
        resultado["error"] = str(e)
        print(f"   × Error descargando {nombre_archivo}: {e}")

    finally:
        try:
            esperar_pantalla_carga(page)
        except Exception:
            pass

    return resultado


def validar_rutero_obligatorio(resultado_rutero: Dict[str, Any]) -> None:
    """
    Rutero es crítico. Si falla, el procesamiento posterior no debe ejecutarse.
    """
    if resultado_rutero.get("ok"):
        return

    detalle = resultado_rutero.get("error") or "Error no especificado."
    ruta = resultado_rutero.get("ruta") or "Ruta no disponible."

    raise RuntimeError(
        "No se puede continuar porque Reporte_Rutero.csv es obligatorio y falló.\n"
        f"Ruta esperada: {ruta}\n"
        f"Detalle: {detalle}"
    )


def construir_resumen_descargas(
    carpeta: str,
    descargas: List[Dict[str, Any]],
) -> Dict[str, Any]:
    archivos_ok = [d for d in descargas if d.get("ok")]
    archivos_error = [d for d in descargas if not d.get("ok")]
    obligatorios_error = [d for d in archivos_error if d.get("obligatorio")]

    return {
        "carpeta": carpeta,
        "carpeta_absoluta": os.path.abspath(carpeta),
        "descargas": descargas,
        "archivos_ok": archivos_ok,
        "archivos_error": archivos_error,
        "obligatorios_error": obligatorios_error,
        "ok": len(obligatorios_error) == 0,
    }


def imprimir_resumen_descargas(resumen: Dict[str, Any]) -> None:
    print("\n--- RESUMEN QA DE DESCARGAS ---")
    print(f"Carpeta: {resumen['carpeta_absoluta']}")

    for item in resumen["descargas"]:
        estado = "OK" if item.get("ok") else "ERROR"
        obligatorio = "OBLIGATORIO" if item.get("obligatorio") else "opcional"

        print(
            f"  [{estado}] {item.get('archivo')} | {obligatorio} | "
            f"bytes={item.get('bytes', 0)} | "
            f"columnas={item.get('columnas_detectadas', 0)}"
        )

        if item.get("error"):
            print(f"       Detalle: {item['error']}")

    if resumen["ok"]:
        print("Resultado QA descarga: APROBADO para procesamiento.")
    else:
        print("Resultado QA descarga: BLOQUEADO. Hay archivos obligatorios con error.")


def ejecutar_descargas(usuario, password, anio, mes):
    """
    Ejecuta login, descarga reportes y devuelve un resumen estructurado.
    """
    _, ultimo_dia = calendar.monthrange(anio, mes)

    f_inicio = f"{anio}-{mes:02d}-01"
    f_fin = f"{anio}-{mes:02d}-{ultimo_dia}"

    carpeta = f"descargas control interno {f_inicio}"
    os.makedirs(carpeta, exist_ok=True)

    descargas: List[Dict[str, Any]] = []
    browser = None

    with sync_playwright() as p:
        try:
            print("\n[Abriendo navegador...]")

            browser = p.chromium.launch(headless=False)
            page = browser.new_page(accept_downloads=True)

            page.set_default_timeout(DEFAULT_TIMEOUT_MS)
            page.set_default_navigation_timeout(DEFAULT_TIMEOUT_MS)

            print(f"[Iniciando sesión como {usuario}...]")

            page.goto(
                "https://dev.saludgestiona.com/business/signin/MTAwNQ==",  #https://saludgestiona.com/business/signin/MTAwNQ==
                wait_until="networkidle",
            )

            page.locator("input[placeholder*='Documento']").fill(usuario)
            page.locator("input[placeholder*='Contraseña']").fill(password)
            page.get_by_role("button", name="Ingresar").click()

            page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT_MS)
            esperar_pantalla_carga(page)

            page.goto(
                "https://dev.saludgestiona.com/business/reports",
                wait_until="networkidle",
            )
            esperar_pantalla_carga(page)

            print("\n--- SECCIÓN: REGISTROS ---")

            page.locator("a[data-category='2']").click(
                force=True,
                timeout=DEFAULT_TIMEOUT_MS,
            )
            esperar_pantalla_carga(page)

            descargas.append(
                descargar_reporte(
                    page,
                    "7",
                    "2",
                    "Notas_Cuidador_Actividades",
                    f_inicio,
                    f_fin,
                    carpeta,
                )
            )

            descargas.append(
                descargar_reporte(
                    page,
                    "7",
                    "3",
                    "Notas_Cuidador_Invasivos",
                    f_inicio,
                    f_fin,
                    carpeta,
                )
            )

            descargas.append(
                descargar_reporte(
                    page,
                    "9",
                    "59",
                    "Nota_Enfermeria",
                    f_inicio,
                    f_fin,
                    carpeta,
                )
            )

            descargas.append(
                descargar_reporte(
                    page,
                    "9",
                    "60",
                    "Nota_Enfermeria_Ventilados",
                    f_inicio,
                    f_fin,
                    carpeta,
                )
            )

            print("\n--- SECCIÓN: RUTERO ---")

            page.goto(
                "https://saludgestiona.com/business/reports",
                wait_until="networkidle",
            )
            esperar_pantalla_carga(page)

            page.locator("a[data-category='6']").click(
                force=True,
                timeout=DEFAULT_TIMEOUT_MS,
            )
            esperar_pantalla_carga(page)

            resultado_rutero = descargar_reporte(
                page,
                "4",
                None,
                "Reporte_Rutero",
                f_inicio,
                f_fin,
                carpeta,
            )
            descargas.append(resultado_rutero)

            # Acción crítica después de Rutero:
            # validar antes de permitir procesamiento.
            validar_rutero_obligatorio(resultado_rutero)

            resumen = construir_resumen_descargas(carpeta, descargas)
            imprimir_resumen_descargas(resumen)

            print(f"\n¡DESCARGAS FINALIZADAS! Archivos en: {os.path.abspath(carpeta)}")

            return resumen

        finally:
            if browser is not None:
                browser.close()