import os

import remote_testing
import traceback

# from local_testing import test_local
from workflows.w2 import workflow_2


def lambda_handler(event, context, remote=True):
    grupo_wsp = event['groupName']
    client_id = event['clientId']
    print(f"Valores recibidos para notificación via WhatsApp: Grupo {grupo_wsp}, Cliente WhatsApp {client_id}")
    try:
        if remote:
            cantidad_recomendaciones, cantidad_recomendaciones_molienda, cantidad_recomendaciones_flotacion, ruta_s3_recomendaciones, ruta_s3_molienda, ruta_s3_flotacion = remote_testing.init_test_remoto()
        else:
            cantidad_recomendaciones, cantidad_recomendaciones_molienda, cantidad_recomendaciones_flotacion, ruta_s3_recomendaciones, ruta_s3_molienda, ruta_s3_flotacion = test_local(
                url="https://mldev.antamina.com/mayta/")
    except Exception as e:
        print(e)
        # Print the stack trace
        traceback.print_exc()
        return "Error"

    response = workflow_2(cantidad_recomendaciones, cantidad_recomendaciones_molienda,
                          cantidad_recomendaciones_flotacion, ruta_s3_recomendaciones, ruta_s3_molienda,
                          ruta_s3_flotacion, grupo_wsp, client_id)

    return response


if __name__ == '__main__':
    lambda_handler({"groupName": "Test multimedia", "clientId": "client-0"}, None, False)
