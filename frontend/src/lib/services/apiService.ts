// import {authStore} from './authService';

// BASE URL for API calls
const API_BASE_URL = 'https://admin.casadosanto.es'

/**
 * Make an authenticated API request
 */

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
    try {
        // Authorization: 
        // Make the API request
        const headers = {
            'Content-Type': 'application/json',
        };

        // Make the API request
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {

            headers,
            mode: 'cors',
        });

        const contentType = response.headers.get("Content-Type");
        const responseText = await response.text();

        if (response.ok) { // Check if the request was successful (status code in the range 200-299)
            try {
                const data = JSON.parse(responseText);

                // Now you can work with the 'data' object
                return data
            } catch (error) {
                console.error("Error parsing JSON:", error);
            }
        } else {
            console.error("Error en la respuesta de la API:", response.status, responseText);
        }

    } catch (error) {
        console.error("Error en la solicitud de la API:", error);
    }
}

export async function apiPost(endpoint: string, body,) {
    try {
        // Authorization: 
        // Make the API request
        const headers = {
            'Content-Type': 'application/json',
        };

        // Make the API request
        const response = await fetch(`${API_BASE_URL}${endpoint}`,
            {
                method: "POST",
                headers,
                mode: "cors",
                credentials: "omit",
                body: JSON.stringify(body),
            },
        );

        return response
    } catch (error){
        console.error("Network or Fetch Error:", error);
        throw new Error("Failed to connect to the API. Please check your network connection.");

    }
}
