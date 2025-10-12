// import {authStore} from './authService';

// BASE URL for API calls
const API_BASE_URL = 'https://casadosantoadmin.casacam.net'
// const api_key = 'xroo15zj.7DOgvspDouwAgSlk9bq4zK5R14ujlq1X.'
// const api_key="api-test1111"
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
        // console.log("response-type", response.type)
        const contentType = response.headers.get("Content-Type");
        // console.log("Content-Type:", contentType);
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
