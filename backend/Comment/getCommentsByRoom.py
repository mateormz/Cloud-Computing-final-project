import boto3
from boto3.dynamodb.conditions import Key
import os
import json

def lambda_handler(event, context):
    try:
        # Validación de token
        token = event['headers'].get('Authorization')
        if not token:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Token no proporcionado'})
            }

        # Validación del token usando otra Lambda (sin cambios)
        function_name = f"{os.environ['SERVICE_NAME']}-{os.environ['STAGE']}-hotel_validateUserToken"
        payload_string = json.dumps({
            "body": {
                "token": token,
                "tenant_id": "global"
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

        # Consulta usando el índice LSI
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['TABLE_COMMENTS']
        table = dynamodb.Table(table_name)

        tenant_id = event['path']['tenant_id']
        room_id = event['path']['room_id']

        response = table.query(
            IndexName="tenant-room-index",
            KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('room_id').eq(room_id)
        )

        return {
            'statusCode': 200,
            'body': {'comments': response.get('Items', [])}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': 'Error interno del servidor', 'details': str(e)}
        }
