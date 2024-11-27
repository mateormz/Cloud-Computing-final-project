module.exports.deleteReservation = async (event) => {
    try {
        const token = event.headers.Authorization;
        if (!token) {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'Token no proporcionado' })
            };
        }

        const { tenant_id, reservation_id } = event.pathParameters;

        const functionName = `${process.env.SERVICE_NAME_USER}-${process.env.STAGE}-hotel_validateUserToken`;
        const payload = {
            body: { token, tenant_id }
        };

        const tokenResponse = await lambda.invoke({
            FunctionName: functionName,
            InvocationType: 'RequestResponse',
            Payload: JSON.stringify(payload),
        }).promise();

        const responseBody = JSON.parse(tokenResponse.Payload);
        if (responseBody.statusCode !== 200) {
            return {
                statusCode: responseBody.statusCode,
                body: responseBody.body
            };
        }

        const params = {
            TableName: process.env.TABLE_RESERVATIONS,
            Key: { tenant_id, reservation_id }
        };

        await dynamoDb.delete(params).promise();

        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Reserva eliminada con éxito' })
        };
    } catch (error) {
        console.error('Error en deleteReservation:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error interno del servidor', details: error.message })
        };
    }
};
