import time
from os import getenv

from flows.authentication.login import login_AD, login_cognito
from flows.pages.recomendaciones import procesar_pantalla_recomendaciones
from flows.pages.tableros import procesar_pantalla_tableros
from utils import *


def general_flow(driver, url, remoto=False, idp="AZURE", pantalla=False, timeout_seconds=60):
    driver.get(url)
    driver.maximize_window()

    filename = f"/tmp/{get_current_timestamp()}"

    print("Esperando a que cargue la página")
    time.sleep(8)

    print(f"Iniciando sesión a través de {idp}")

    # # INICIO DE SESIÓN
    # if idp == "AZURE":
    #     print("Cerrando la pestaña secundaria y cambio a la principal")
    tabs = driver.window_handles
    try:
        driver.switch_to.window(tabs[1])
        driver.close()
    except Exception as e:
        print("No se abrió otra pestaña")
        print(e)
        pass
    driver.switch_to.window(tabs[0])

    # Verificando si funciona AD
    funciona_AD = False
    try:
        funciona_AD = login_AD(driver, remoto)
    except Exception as e:
        print(e)
        print("Error de login con AD")
    login_cognito(driver, getenv("COGNITO_URL_DEV"))

    # PANTALLA DE INICIO
    print("Acceso al sistema")
    if pantalla:
        print("Guardando pantalla - ./Pantallas/4-Home")
        guardar_pantalla(driver, "./Pantallas/4-Home")

    # OBTENER LAS PANTALLAS PRINCIPALES
    cantidad_items = 0
    menu_items = {}

    login_loop = False

    start_time = time.time()
    elapsed_time = 0
    retry_loop = True
    while retry_loop:
        if len(driver.window_handles) > 2:
            login_loop = True
            break
        print("Extrayendo la cantidad de menús en Mayta")
        menu_items = combine_lists(["RECOMENDACIONES", "SEGUIMIENTO", "TABLEROS", "HISTORIAL", "CARGA_ARCHIVOS"],
                                   get_items(driver))
        cantidad_items = len(menu_items.keys())
        elapsed_time = time.time() - start_time
        retry_loop = (cantidad_items == 0 and elapsed_time < timeout_seconds)

    if login_loop:
        return -1, -1, -1, "ERROR_BUCLE", "ERROR"

    # Manejo cuándo se queda colgado mucho tiempo
    if cantidad_items == 0 and elapsed_time >= timeout_seconds:
        return -2, -2, -2, "ERROR_TIMEOUT", "ERROR_TIMEOUT"

    # PANTALLA DE RECOMENDACIONES
    print("Ingresando a la pantalla de recomendaciones")
    print(menu_items.keys())
    menu_items["RECOMENDACIONES"].click()

    if pantalla:
        print("Guardando pantalla - ./Pantallas/5-Recomendaciones")
        guardar_pantalla(driver, "./Pantallas/5-Recomendaciones")

    # Debe de devolver la cantidad de recomendaciones en total
    mensaje_recomendaciones, cantidad_recomendaciones = procesar_pantalla_recomendaciones(driver, filename)

    # PANTALLA DE TABLEROS
    print("Ingresando a la pantalla de tableros")
    menu_items["TABLEROS"].click()
    time.sleep(5)
    if pantalla:
        print("Guardando pantalla - ./Pantallas/8-Tableros")
        guardar_pantalla(driver, "./Pantallas/8-Tableros")

    # Debe de devolver la cantidad de tableros y la cantidad de iframes funcionales
    tableros_listados, iframes_funcionando = procesar_pantalla_tableros(driver, filename)

    # PANTALLA DE HISTORIAL
    print("Ingresando a la pantalla de historial")
    # menu_items["HISTORIAL"].click()
    driver.get(os.getenv("HISTORIAL_URL"))
    if pantalla:
        print("Guardando pantalla - ./Pantallas/9-Historial")
        guardar_pantalla(driver, "./Pantallas/9-Historial")

    print("Saliendo")
    driver.quit()

    print("Mensaje para codepipeline: ")
    print(f"Funciona auth con AD: {funciona_AD}")
    print(f"Recomendaciones: {mensaje_recomendaciones}")
    print(f"Tableros: {tableros_listados}, iframes funcionales: {iframes_funcionando}")
    log_final = read_file_contents(filename + ".log")
    print(log_final)
    ruta_s3 = upload_file_to_s3(getenv("BUCKET_NAME"), getenv("BUCKET_FOLDER"), filename, os.path.basename(filename))

    return cantidad_recomendaciones, tableros_listados, iframes_funcionando, ruta_s3, log_final
