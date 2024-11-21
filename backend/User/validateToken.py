import boto3
from datetime import datetime
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    token_table_name = os.environ['TABLE_TOKEN_NAME']
    index_name = os.environ['INDEXGSI1_TOKENS']  # token-index
    token = event.get('token')

    if not token:
        return {
            'statusCode': 400,
            'body': {'error': 'Token no proporcionado'}
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

    if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > expiration:
        return {
            'statusCode': 403,
            'body': {'error': 'Token expirado'}
        }

    return {
        'statusCode': 200,
        'body': {'message': 'Token válido'}
    }