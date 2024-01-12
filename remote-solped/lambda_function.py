import os

import remote_testing
from aws_utils import obtener_cliente_codepipeline_remoto, get_s3_object_url, falla_prueba, get_s3_uri, \
    invoke_error_handler_lambda
from workflows.w1 import workflow_1
import traceback


def lambda_handler(event, context):
    try:
        global cantidad_recomendaciones, cantidad_tableros, cantidad_iframes, ruta_s3
        codepipeline = obtener_cliente_codepipeline_remoto(os.getenv("CROSS_ACCOUNT_AWS_ID","400397654878"))
        job_data = event['CodePipeline.job']['data']
        job_id = event['CodePipeline.job']['id']

        cantidad_recomendaciones, cantidad_tableros, cantidad_iframes, ruta_s3, log_final = remote_testing.init_test_remoto()
        if cantidad_recomendaciones == -1:
            raise Exception("Error en el bucle de login")
        elif cantidad_recomendaciones == -2:
            raise Exception("Error en el timeout del monitoreo (login)")

        ruta_s3 = get_s3_uri(ruta_s3)
    except Exception as e:
        print(e)
        error_message = str(e)
        falla_prueba(codepipeline, job_id, f"Error con selenium: {error_message}")
        traceback.print_exc()
        ERROR_WHATSAPP_GROUPS = [x.strip("' ") for x in os.environ.get('ERROR_WHATSAPP_GROUPS').split(',')]
        print("Grupos de WhatsApp recibidos para notificación de error")
        print(ERROR_WHATSAPP_GROUPS)
        invoke_error_handler_lambda(origin="Lambda de monitoreo de recomendaciones: aa-remote-recommendations-check",
                                    whatsapp_groups=ERROR_WHATSAPP_GROUPS, error_code="500", message=error_message)
        return {
            "statusCode": 500,
            "body": error_message,
            "notification": f"Se invocó a la función central de notificación de errores"
        }

    response = workflow_1(codepipeline, job_id, job_data, cantidad_recomendaciones, cantidad_tableros, cantidad_iframes,
                          ruta_s3, log_final)

    return response


if __name__ == '__main__':
    lambda_handler(None, None)
