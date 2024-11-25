import boto3
import json
import os

def lambda_handler(event, context):
    try:
        # Log del evento recibido
        print("Evento recibido:", json.dumps(event))

        # Proteger el Lambda con validación de token
        token = event['headers'].get('Authorization')
        print("Token recibido en Authorization Header:", token)

        if not token:
            print("Error: Token no proporcionado.")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Token no proporcionado'})
            }

        function_name = f"{os.environ['SERVICE_NAME']}-{os.environ['STAGE']}-hotel_validateUserToken"
        print("Nombre de la función de validación de token:", function_name)

        # Preparar payload para la función de validación de token
        tenant_id = event.get('body', {}).get('tenant_id')
        payload_string = json.dumps({
            "body": {
                "token": token,
                "tenant_id": tenant_id
            }
        })
        print("Payload enviado a validateUserToken:", payload_string)

        # Invocar la función de validación de token
        lambda_client = boto3.client('lambda')
        invoke_response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=payload_string
        )

        # Leer la respuesta de la función de validación
        response = json.loads(invoke_response['Payload'].read())
        print("Respuesta de validateUserToken:", response)

        if response['statusCode'] == 403:
            print("Error: Token inválido o expirado.")
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Acceso no autorizado - Token inválido o expirado'})
            }

        # Token válido, continuar con el proceso
        tenant_id = event.get('body', {}).get('tenant_id')
        user_id = event.get('body', {}).get('user_id')
        print("tenant_id:", tenant_id, "user_id:", user_id)

        if not tenant_id or not user_id:
            print("Error: Faltan campos requeridos tenant_id o user_id.")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Faltan campos requeridos: tenant_id o user_id'})
            }

        # Conectar con DynamoDB para obtener los datos del usuario
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['TABLE_NAME']
        print("Nombre de la tabla DynamoDB:", table_name)
        table = dynamodb.Table(table_name)

        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'user_id': user_id
            }
        )
        print("Respuesta de DynamoDB get_item:", response)

        if 'Item' not in response:
            print("Error: Usuario no encontrado en DynamoDB.")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Usuario no encontrado'})
            }

        user = response['Item']
        print("Usuario encontrado en DynamoDB:", user)

        # Eliminar información sensible
        if 'password_hash' in user:
            del user['password_hash']
            print("password_hash eliminado del resultado.")

        return {
            'statusCode': 200,
            'body': {'user': user}
        }

    except KeyError as e:
        print("Error KeyError:", str(e))
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Campo requerido no encontrado: {str(e)}'})
        }
    except Exception as e:
        print("Error inesperado:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error interno del servidor', 'details': str(e)})
        }
