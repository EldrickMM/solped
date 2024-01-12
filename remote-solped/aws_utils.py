import json
import os
import time

import boto3
import traceback

from utils import evaluate_and_return, get_peru_timestamp


def obtener_cliente_codepipeline_remoto(cuenta_aws_externa="400397654878"):
    # Asumir role de codepipeline en la cuenta de Tools
    sts = boto3.client('sts', region_name='us-east-1')

    # Por defecto se conecta a la cuenta aws de tools: 400397654878
    paramsSTS = {
        'RoleArn': f'arn:aws:iam::{cuenta_aws_externa}:role/codepipeline_comunnication_cross_account',
        'RoleSessionName': 'CrossAccountCredentials',
        'ExternalId': '123ABC',
        'DurationSeconds': 3600
    }

    assumeRoleStep1 = sts.assume_role(**paramsSTS)

    # Credenciales de acceso de la cuenta de Tools
    accessparams = {
        'aws_access_key_id': assumeRoleStep1['Credentials']['AccessKeyId'],
        'aws_secret_access_key': assumeRoleStep1['Credentials']['SecretAccessKey'],
        'aws_session_token': assumeRoleStep1['Credentials']['SessionToken']
    }

    # Crear cliente de codepipeline remoto
    codepipeline = boto3.client('codepipeline', **accessparams)

    return codepipeline


def pasa_prueba(codepipeline, job_id, cantidad_recomendaciones, cantidad_tableros, cantidad_iframes, ruta_s3,
                log_final):
    params = {
        'jobId': job_id,
        'outputVariables': {
            'Recomendaciones': f'Recomendaciones: {cantidad_recomendaciones}',
            'Tableros': f'Tableros: {cantidad_tableros}, iframes funcionando: {cantidad_iframes}',
            'RutaS3': f'{ruta_s3}',
            'LogFinal': f'{log_final}'
        }
    }

    codepipeline.put_job_success_result(**params)


def falla_prueba(codepipeline, job_id, message):
    params = {
        'jobId': job_id,
        'failureDetails': {
            'type': 'JobFailed',
            'message': message,
        }
    }

    codepipeline.put_job_failure_result(**params)


def get_s3_object_url(bucket_and_path):
    print(bucket_and_path)
    try:
        # Split the bucket name and object path
        bucket, path = bucket_and_path.split('/', 1)

        # Create the S3 client
        s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))

        # Generate the object URL
        object_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': path}
        )

        return object_url
    except Exception as e:
        traceback.print_exc()
        return None


def get_s3_uri(bucket_name):
    s3_uri = f"s3://{bucket_name}"
    return s3_uri

def invoke_error_handler_lambda(origin=None, whatsapp_groups=None, error_code=None, message=None):
    """
       Invoke an AWS Lambda function with a given payload.

       :param origin: Origin source for the event. Default is 'default_origin'.
       :type origin: str

       :param whatsapp_groups: List of WhatsApp group identifiers. Default is ['default_group'].
       :type whatsapp_groups: list

       :param error_code: Error code for the info section of the event. Default is 'default_error_code'.
       :type error_code: str

       :param message: Message for the info section of the event. Default is 'default_message'.
       :type message: str

       :return: Mensaje de éxito o fracaso al invocar la función Lambda.
       """

    # Read the Lambda function name from an environment variable
    lambda_function_name = os.environ.get('ERROR_HANDLER_LAMBDA_FUNCTION_NAME')

    if not lambda_function_name:
        raise EnvironmentError("The ERROR_HANDLER_LAMBDA_FUNCTION_NAME environment variable is not set.")
    session = boto3.session.Session()
    lambda_client = session.client('lambda')

    # Construct the event payload dynamically based on parameters
    event_payload = {
        "origin": origin if origin else "default_origin",
        "whatsapp_groups": whatsapp_groups if whatsapp_groups else ["default_group"],
        "info": {
            "error_code": str(error_code) if error_code else "default_error_code",
            "message": message if message else "default_message",
            "timestamp": get_peru_timestamp()
        }
    }

    # Converting dict to JSON string
    event_payload_str = json.dumps(event_payload)

    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='Event',  # Use 'Event' for async, 'RequestResponse' for sync
        Payload=event_payload_str.encode('utf-8')
    )

    # Read Lambda function response
    if response['StatusCode'] == 202:
        print('Lambda function invoked successfully.')
        return 'Lambda function invoked successfully.'
    else:
        print(f"Failed to invoke Lambda function. StatusCode: {response['StatusCode']}")
        return f"Failed to invoke Lambda function. StatusCode: {response['StatusCode']}"
