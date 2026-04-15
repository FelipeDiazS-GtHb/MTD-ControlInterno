# Archivo: main.py
from descargas import ejecutar_descargas
from procesar_datos import procesar_carpeta, exportar_a_excel

def iniciar_bot():
    print("=========================================")
    print("      BOT DE EXTRACCIÓN Y LIMPIEZA       ")
    print("=========================================")
    
    # 1. Pedimos los datos al usuario
    usuario = input("Usuario (Documento): ")
    password = input("Contraseña: ")
    anio = int(input("Año (Ej: 2026): "))
    mes = int(input("Mes (Ej: 3): "))
    
    # 2. Mandamos a descargar (le pasamos los datos y nos devuelve la carpeta)
    carpeta_descargas = ejecutar_descargas(usuario, password, anio, mes)
    
    # 3. Mandamos a procesar la carpeta que nos acaban de devolver
    print("\n--- INICIANDO PROCESAMIENTO DE DATOS ---")
    datos_limpios = procesar_carpeta(carpeta_descargas)
    
    # 4. Mandamos a exportar los Excel
    rutas_creadas = exportar_a_excel(datos_limpios, carpeta_descargas)
    
    print("\n=========================================")
    print("      ¡TODO EL FLUJO HA TERMINADO!       ")
    print("=========================================")

if __name__ == "__main__":
    try:
        iniciar_bot()
    except KeyboardInterrupt:
        print("\nProceso cancelado por el usuario.")