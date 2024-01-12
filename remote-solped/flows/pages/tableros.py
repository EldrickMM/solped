import time

from selenium.webdriver.common.by import By

from utils import extract_texts, log_values_to_file, click_tablero_and_log_text, generate_unique_numbers, \
    count_boolean_values, guardar_pantalla


def procesar_pantalla_tableros(driver,filename):
    main_content = driver.find_element(By.CSS_SELECTOR, ".ant-layout-content")
    titles = extract_texts(main_content)
    print(titles)
    log_values_to_file(["2. PANTALLA DE TABLEROS","2.1 Listado de tableros"], filename)

    log_values_to_file(titles, filename)

    # TABLEROS = ["KPI",
    #             "KPI_Alertas",
    #             "KPI_Pipelines",
    #             "Metas_Operativas",
    #             "Seguimiento_de_Impacto",
    #             "Análisis_de_rechazos",
    #             "KPI_Implementacion",
    #             "Trazabilidad_de_material",
    #             "Métricas_de_modelos", ]

    TABLEROS = titles

    log_values_to_file(["2.2 Verificación de tableros"], filename)
    # tableros_random = generate_unique_numbers(3, len(TABLEROS)-1)

    # Probando con KPI Implementación
    # print("Probando con KPI Implementación")
    # click_tablero_and_log_text(driver, 6, TABLEROS, filename)

    funcionan_iframes = []
    for i in range(len(TABLEROS)):
        funciona_iframe = click_tablero_and_log_text(driver, i, TABLEROS, filename)
        funcionan_iframes.append(funciona_iframe)

    return len(titles), count_boolean_values(funcionan_iframes,True)
