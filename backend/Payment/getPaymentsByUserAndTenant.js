const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

exports.getPaymentByUserAndTenantId = async (event) => {
    try {
        const tenant_id = event.pathParameters.tenant_id;
        const user_id = event.pathParameters.user_id;

        // Validación de token
        const token = event.headers?.Authorization;
        if (!token) {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'Token no proporcionado' }),
            };
        }

        // Validar token
        const validateTokenResponse = await validateToken(token, tenant_id);
        if (validateTokenResponse.statusCode !== 200) {
            return validateTokenResponse;
        }

        // Consultar pagos por tenant_id y user_id usando el GSI "tenant-user-id-index"
        const params = {
            TableName: process.env.TABLE_PAYMENTS,
            IndexName: 'tenant-user-id-index',  // Usamos el GSI creado en el serverless.yml
            KeyConditionExpression: "tenant_id = :tenant_id and user_id = :user_id",
            ExpressionAttributeValues: {
                ":tenant_id": tenant_id,
                ":user_id": user_id,
            },
        };

        const result = await dynamoDb.query(params).promise();

        return {
            statusCode: 200,
            body: JSON.stringify({ payments: result.Items }),
        };

    } catch (error) {
        console.error('Error en getPaymentByUserAndTenantId:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error interno del servidor', details: error.message }),
        };
    }
};