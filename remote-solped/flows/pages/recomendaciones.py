from utils import *


def procesar_pantalla_recomendaciones(driver,filename):
    log_values_to_file(["1. PANTALLA DE RECOMENDACIONES", "1.1 Recomendaciones de molienda"], filename)
    # OBTENER LAS TABS DE LAS TABLAS DE LAS RECOMENDACIONES
    recomendacion_items = combine_lists(["MOLIENDA", "FLOTACION"], get_items(driver, "ant-tabs-tab"))
    texto_aleta_info = ""
    try:
        texto_aleta_info = get_message(driver,"core-alert_alert_message__imOra")
    except Exception:
        texto_aleta_info = "No apareció el mensaje de alerta"
    cantidad_recomendaciones = 0

    # TABLA DE RECOMENDACIONES DE MOLIENDA
    existen_recomendaciones_molienda = procesar_tabla_recomendaciones(driver, recomendacion_items, "MOLIENDA",filename,texto_aleta_info)

    log_values_to_file(["1.2 Recomendaciones de flotación"], filename)
    # TABLA DE RECOMENDACIONES DE FLOTACIÓN
    existen_recomendaciones_flotacion = procesar_tabla_recomendaciones(driver, recomendacion_items, "FLOTACION",filename,texto_aleta_info)

    if existen_recomendaciones_molienda or existen_recomendaciones_flotacion:
        cantidad_recomendaciones = extract_number(texto_aleta_info)
        if cantidad_recomendaciones is None:
            return f"0 - {texto_aleta_info}",0
        return f"{cantidad_recomendaciones}",cantidad_recomendaciones

    return f"{cantidad_recomendaciones} - {texto_aleta_info}", cantidad_recomendaciones


def procesar_tabla_recomendaciones(driver, recomendacion_items, proceso,filename, mensaje_error,pantalla=False):
    print(f"Recomendaciones de {proceso}")
    click_element(driver, recomendacion_items[proceso])
    bajar_pantalla(driver)
    if pantalla:
        print(f"Guardando pantalla - 6-{proceso}")
        guardar_pantalla(driver, f"./Pantallas/6-{proceso}")

    tablas = combine_lists(["MOLIENDA", "FLOTACION"], get_items(driver, "ant-table-tbody"))
    print(f"Guardando recomendaciones de {proceso}")
    try:
        datos_tabla_proceso = procesar_tabla(tablas[proceso])
        if len(datos_tabla_proceso) == 0:
            # TODO: Cambiar Error: Data Dispatch por el verdadero mensaje usando Selenium
            log_values_to_file([mensaje_error], filename)
            return False
        log_values_to_file(datos_tabla_proceso, filename)
        return True
    except KeyError:
        print(f"No existe la tabla de {proceso} en el HTML")
        return False


