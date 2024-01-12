import traceback

import boto3
import requests

from aws import cargar_envs


def shorten_url(long_url):
    access_token = 'YOUR_BITLY_ACCESS_TOKEN'
    api_url = 'https://api-ssl.bitly.com/v4/shorten'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'long_url': long_url
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        short_url = data['id']
        return short_url
    else:
        # Handle error case
        print('URL shortening failed.')
        return None

def get_s3_object_url(bucket_and_path):
    print(bucket_and_path)
    try:
        # Split the bucket name and object path
        bucket, path = bucket_and_path.split('/', 1)

        # Create the S3 client
        s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'),region_name='us-west-2')

        # Generate the object URL
        object_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': path}
        )

        return object_url
    except Exception as e:
        traceback.print_exc()
        return None


def s3_test(objeto):
    cargar_envs()
    return get_s3_object_url(objeto)


if __name__ == '__main__':
    # antamina-aa-dev-stagging-bucket/finance/stc/remotetesting/2023-06-14_21-04-37_299.log
    # mayta-logs/workflow-1/2023-06-12_10-57-12_981.log
    print(s3_test("mayta-logs/workflow-1/2023-06-12_10-57-12_981.log"))
