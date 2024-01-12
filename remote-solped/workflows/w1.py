from aws_utils import falla_prueba, pasa_prueba
from utils import compare_options


def workflow_1(codepipeline, job_id, job_data, cantidad_recomendaciones, cantidad_tableros, cantidad_iframes, ruta_s3,
               log_final):
    # Captura los datos enviados en User Parameters en la acción de Lambda
    user_parameters = None
    try:
        user_parameters = job_data['actionConfiguration']['configuration']['UserParameters']
    except KeyError:
        user_parameters = None
    opcion_recomendaciones, opcion_tableros = str(user_parameters).split(
        ",") if user_parameters and ',' in user_parameters else ("", "")
    opciones_disponibles = ["OPTIONAL", "RESTRICTED"]

    if cantidad_recomendaciones < 0:
        message = f"La prueba falló, ocurrió un error durante la carga de las recomendaciones"
        falla_prueba(codepipeline, job_id, message)
        response = {
            'statusCode': 200,
            'message': 'Workflow 1 ejecutado'
        }
        return response

    if cantidad_tableros > cantidad_iframes:
        if not opcion_tableros:
            pasa_prueba(codepipeline, job_id, cantidad_recomendaciones, cantidad_tableros, cantidad_iframes, ruta_s3,
                        log_final)
        elif compare_options(opcion_tableros, opciones_disponibles, 0):
            pasa_prueba(codepipeline, job_id, cantidad_recomendaciones, cantidad_tableros, cantidad_iframes, ruta_s3,
                        log_final)
        elif compare_options(opcion_tableros, opciones_disponibles, 1):
            message = f"La prueba falló, no todos los tableros están funcionando: Tableros totales {cantidad_tableros},funcionando {cantidad_iframes}. Revisar logs en: {ruta_s3}"
            falla_prueba(codepipeline, job_id, message)
        else:
            pasa_prueba(codepipeline, job_id, cantidad_recomendaciones, cantidad_tableros, cantidad_iframes, ruta_s3,
                        log_final)

    response = {
        'statusCode': 200,
        'message': 'Workflow 1 ejecutado'
    }

    return response
