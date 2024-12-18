import axios from "axios";

const USER_API = 'https://o8i8j2n3vj.execute-api.us-east-1.amazonaws.com/dev/user';
const ROOM_API = 'https://y3z1dcl3bi.execute-api.us-east-1.amazonaws.com/dev';
const COMMENT_API = 'https://euoupdyd66.execute-api.us-east-1.amazonaws.com/dev';
const SERVICE_API = 'https://oxyokl9fcj.execute-api.us-east-1.amazonaws.com/dev';
const HOTEL_API = 'https://uz3dmwro1a.execute-api.us-east-1.amazonaws.com/dev';
const RESERVATION_API = 'https://xilves4en1.execute-api.us-east-1.amazonaws.com/dev';
const PAYMENT_API = 'https://djx90q4q18.execute-api.us-east-1.amazonaws.com/dev';

// USER

export const fetchLogin = async(tenant_id, email, password) => {
    const response = await axios.post(`${USER_API}/login`, { tenant_id, email, password });
    return response.data;
}

export const fetchRegister = async (tenant_id, nombre, email, password) => {
    const response = await axios.post(`${USER_API}/register`, { tenant_id, nombre, email, password });
    return response.data;
};

export const fetchGetUser = async (tenant_id, user_id) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const data = { tenant_id, user_id };

        const response = await axios.post(`${USER_API}/getUser`, data, config);

        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener los datos del usuario:", error);
        throw error;
    }
};

// ROOMS

export const fetchRoomsByTenant = async (tenant_id) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const response = await axios.get(`${ROOM_API}/rooms/${tenant_id}`, config);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener las habitaciones:", error);
        throw error;
    }
};

export const fetchRoomById = async (tenant_id, room_id) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const response = await axios.get(`${ROOM_API}/room/${tenant_id}/${room_id}`, config);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener los detalles de la habitación:", error);
        throw error;
    }
};

// COMMENTS

export const fetchCommentsByRoom = async (tenant_id, room_id) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const response = await axios.get(`${COMMENT_API}/comments/${tenant_id}/${room_id}`, config);
        console.log(response.data);
        return response.data.body.comments;
    } catch (error) {
        console.error("Error al obtener los comentarios:", error);
        throw error;
    }
};

export const fetchCreateComment = async (tenant_id, user_id, room_id, comment_text) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const data = { tenant_id, user_id, room_id, comment_text };
        const response = await axios.post(`${COMMENT_API}/comment/create`, data, config);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al crear el comentario:", error);
        throw error;
    }
};

// SERVICES

export const fetchServicesByTenant = async (tenant_id) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const response = await axios.get(`${SERVICE_API}/services/getByTenant/${tenant_id}`, config);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener los servicios del tenant:", error);
        throw error;
    }
};

// HOTEL

export const fetchHotelByTenant = async (tenant_id) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const response = await axios.get(`${HOTEL_API}/hotels/tenant/${tenant_id}`, config);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener la información de los hoteles:", error);
        throw error;
    }
};

export const fetchAllHotels = async () => {
    try {
        const response = await axios.get(`${HOTEL_API}/hotels`);

        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener los hoteles:", error);
        throw error;
    }
};

export const fetchHotelsByLocation = async (hotel_location) => {
    try {
        const response = await axios.get(`${HOTEL_API}/hotels/location`, {
            params: {
                hotel_location
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener los hoteles por ubicación:", error);
        throw error;
    }
};

// RESERVATION

export const fetchCreateReservation = async (tenant_id, user_id, room_id, service_ids, start_date, end_date) => {
    try {
        const token = localStorage.getItem('token');

        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };

        const data = {
            tenant_id,
            user_id,
            room_id,
            service_ids, // arreglo de ids de servicios
            start_date,
            end_date
        };

        console.log('Datos enviados a la API:', data);  // Verifica que los datos sean correctos

        const response = await axios.post(`${RESERVATION_API}/reservation/create`, data, config);
        
        // Log para depurar la respuesta
        console.log('Respuesta de la API:', response.data);

        return response.data;
    } catch (error) {
        console.error("Error al crear la reserva:", error);
        throw error;
    }
};

export const fetchReservationsByUser = async (tenant_id, user_id) => {
    try {
        const token = localStorage.getItem('token'); // Obtén el token del localStorage
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = {
            headers: {
                Authorization: token, // Token en las cabeceras
            },
        };

        const url = `${RESERVATION_API}/reservations/${tenant_id}/${user_id}`;
        console.log("URL de la solicitud:", url);

        const response = await axios.get(url, config);
        console.log("Respuesta del API:", response.data);

        return response.data; // Retorna los datos de las reservas
    } catch (error) {
        console.error("Error al obtener las reservas:", error);
        throw error;
    }
};

// PAYMENT

export const fetchCreatePayment = async (tenant_id, user_id, reservation_id) => {
    try {
        const token = localStorage.getItem('token');
        
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };

        const data = {
            tenant_id,
            user_id,
            reservation_id
        };

        const response = await axios.post(`${PAYMENT_API}/payment/create`, data, config);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al crear el pago:", error);
        throw error;
    }
};

export const fetchPaymentsByUser = async (tenant_id, user_id) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token no disponible');
        }

        const config = { headers: { Authorization: token } };
        const response = await axios.get(`${PAYMENT_API}/payments/${tenant_id}/${user_id}`, config);

        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error al obtener los pagos del usuario:", error);
        throw error;
    }
};
