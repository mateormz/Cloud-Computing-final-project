import boto3
from datetime import datetime
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    token_table_name = os.environ['TABLE_TOKENS']
    index_name = os.environ['INDEXGSI1_TOKENS']  # token-index
    token = event.get('token')
    tenant_id = event.get('tenant_id')

    if not all([token, tenant_id]):
        return {
            'statusCode': 400,
            'body': {'error': 'Token o tenant_id no proporcionado'}
        }

    table = dynamodb.Table(token_table_name)

    # Buscar el token usando el GSI
    response = table.query(
        IndexName=index_name,
        KeyConditionExpression=Key('token').eq(token)
    )

    if not response['Items']:
        return {
            'statusCode': 403,
            'body': {'error': 'Token inválido'}
        }

    token_data = response['Items'][0]
    expiration = token_data['expiration']
    user_id = token_data['user_id']  # Incluimos el user_id para contexto

    if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > expiration:
        return {
            'statusCode': 403,
            'body': {'error': 'Token expirado'}
        }

    return {
        'statusCode': 200,
        'body': {'message': 'Token válido', 'user_id': user_id}
    }