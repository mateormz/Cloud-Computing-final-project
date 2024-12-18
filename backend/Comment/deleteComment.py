import boto3
import os
import json

def lambda_handler(event, context):
    try:
        # Validación de token
        token = event['headers'].get('Authorization')
        if not token:
            return {
                'statusCode': 400,
                'body': {'error': 'Token no proporcionado'}
            }

        # Validación del token usando otra Lambda
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

        # Conexión a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['TABLE_COMMENTS']
        table = dynamodb.Table(table_name)

        # Recuperar parámetros
        tenant_id = event['path']['tenant_id']
        comment_id = event['path']['comment_id']

        # Validar existencia del comentario antes de eliminar
        get_response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'comment_id': comment_id
            }
        )
        if 'Item' not in get_response:
            return {
                'statusCode': 404,
                'body': {'error': 'El comentario no existe'}
            }

        # Eliminar el comentario
        table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'comment_id': comment_id
            }
        )

        return {
            'statusCode': 200,
            'body': {
                'message': 'Comentario eliminado exitosamente'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno del servidor',
                'details': str(e)
            }
        }
