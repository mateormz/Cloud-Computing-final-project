import boto3
import hashlib
import uuid
from datetime import datetime, timedelta
import os
from boto3.dynamodb.conditions import Key

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['TABLE_NAME']
        token_table_name = os.environ['TABLE_TOKENS']
        index_name = os.environ['INDEXLSI1_USERS']  # tenant-email-index
        table = dynamodb.Table(table_name)
        token_table = dynamodb.Table(token_table_name)

        tenant_id = event['body']['tenant_id']
        email = event['body']['email']
        password = event['body']['password']

        if not all([tenant_id, email, password]):
            return {
                'statusCode': 400,
                'body': {'error': 'Faltan campos requeridos'}
            }

        hashed_password = hash_password(password)

        # Buscar al usuario por correo y tenant usando el LSI
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('email').eq(email)
        )

        if not response['Items'] or response['Items'][0]['password_hash'] != hashed_password:
            return {
                'statusCode': 403,
                'body': {'error': 'Credenciales inválidas'}
            }

        user = response['Items'][0]  # Obtener datos del usuario
        user_id = user['user_id']  # Identificar al usuario

        # Generar un token
        token = str(uuid.uuid4())
        expiration = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

        token_table.put_item(
            Item={
                'tenant_id': tenant_id,
                'token': token,
                'user_id': user_id,
                'expiration': expiration
            }
        )

        return {
            'statusCode': 200,
            'body': {'token': token, 'expires': expiration, 'user_id': user_id}
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': {'error': f'Campo requerido no encontrado: {str(e)}'}
        }
    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': {'error': 'Error interno del servidor', 'details': str(e)}
        }
