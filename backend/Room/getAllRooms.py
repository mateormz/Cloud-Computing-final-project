import boto3
from boto3.dynamodb.conditions import Key
import json
import os

def lambda_handler(event, context):
    try:
        # Validación de token
        token = event['headers'].get('Authorization')
        if not token:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Token no proporcionado'})
            }

        function_name = f"{os.environ['SERVICE_NAME']}-{os.environ['STAGE']}-hotel_validateUserToken"

        payload_string = json.dumps({
            "body": {
                "token": token,
                "tenant_id": "global"  # No filtramos por tenant
            }
        })

        lambda_client = boto3.client('lambda')
        invoke_response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=payload_string
        )
        response = json.loads(invoke_response['Payload'].read())

        if response['statusCode'] != 200:
            return {
                'statusCode': response['statusCode'],
                'body': response['body']
            }

        # Token válido, proceder con la operación
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['TABLE_ROOMS']
        table = dynamodb.Table(table_name)
        index_name = os.environ['INDEXGSI1_ROOMS']

        # Consulta usando el índice GSI
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key('availability').eq('disponible')
        )

        return {
            'statusCode': 200,
            'body': {'rooms': response.get('Items', [])}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': 'Error interno del servidor', 'details': str(e)}
        }
