# Archivo: main.py
from descargas import ejecutar_descargas
from procesar_datos import procesar_carpeta, exportar_a_excel


def imprimir_resumen_excel(rutas_creadas):
    print("\n--- RESUMEN QA DE EXPORTACIÓN ---")

    if not rutas_creadas:
        print("  [ERROR] No se generó ningún archivo Excel.")
        return

    for ruta in rutas_creadas:
        print(f"  [OK] {ruta}")


def iniciar_bot():
    print("=========================================")
    print("      BOT DE EXTRACCIÓN Y LIMPIEZA       ")
    print("=========================================")

    # 1. Pedimos los datos al usuario
    usuario = input("Usuario (Documento): ").strip()
    password = input("Contraseña: ").strip()
    anio = int(input("Año (Ej: 2026): ").strip())
    mes = int(input("Mes (Ej: 3): ").strip())

    # 2. Descargamos y validamos.
    # Si Rutero falla, ejecutar_descargas detiene el flujo.
    resumen_descargas = ejecutar_descargas(usuario, password, anio, mes)
    carpeta_descargas = resumen_descargas["carpeta"]

    if not resumen_descargas["ok"]:
        raise RuntimeError("La descarga no pasó QA. No se ejecutará el procesamiento.")

    # 3. Procesamos solo después de validar Rutero.
    print("\n--- INICIANDO PROCESAMIENTO DE DATOS ---")
    datos_limpios = procesar_carpeta(carpeta_descargas)

    # 4. Exportamos los Excel depurados.
    rutas_creadas = exportar_a_excel(datos_limpios, carpeta_descargas)
    imprimir_resumen_excel(rutas_creadas)

    print("\n=========================================")
    print("      ¡TODO EL FLUJO HA TERMINADO!       ")
    print("=========================================")


if __name__ == "__main__":
    try:
        iniciar_bot()

    except KeyboardInterrupt:
        print("\nProceso cancelado por el usuario.")

    except Exception as e:
        print("\n=========================================")
        print("       EL FLUJO SE DETUVO POR ERROR      ")
        print("=========================================")
        print(f"Detalle: {e}")