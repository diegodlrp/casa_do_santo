

import { redirect, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { apiRequest } from '$lib/services/apiService';

export const load: PageServerLoad = async ({ params, locals: { LL } }) => {
    const locale = LL.locale();
    console.log("locale", locale);
    // params.uuid comes from the [uuid] dynamic route segment
    const uuid = params.uuid;
    let checkToken;
    let main_guest_id;
    let main_guest_name = "";
    let main_guest_vat = "";
    let main_guest_email = "";
    let check_in_date = "";
    let check_out_date = "";
    let special_request = "";
    let reservation_id;
    try {
        // 1. Attempt the API call. 
        // If the token is invalid (404, 410, 400), apiRequest should throw.
        checkToken = await apiRequest(`/api-reservation/check-token/${uuid}`);
 
        // 2. EXPLICIT CHECK: If the API succeeded (2xx) but the status field in the JSON is "invalid", redirect.
        // This handles the case where Django returns 200 OK with an error payload.
        if (checkToken && checkToken.status === "invalid") {
            console.error("Token status is 'invalid' in payload, redirecting.");
            throw redirect(302, '/' + locale); // Throwing the redirect is the correct SvelteKit way
        }
        reservation_id = checkToken.reservation_id;
        const reservation = await apiRequest('/reservations/'+reservation_id)
        console.log("reservation",reservation)
        
        if (reservation){
            check_in_date = reservation.check_in_date;
            check_out_date = reservation.check_out_date;
            special_request = reservation.special_request;
            main_guest_id = reservation.main_guest
            const main_guest = await apiRequest('/guests/'+main_guest_id)
            console.log("main_guest",main_guest)

            if (main_guest){
                main_guest_name = main_guest.name;
                main_guest_vat = main_guest.vat;
                main_guest_email = main_guest.email;
            } else {
                console.warn(`No main guest data found for locale: ${locale}`);
            }
        } else {
            console.warn(`No reservation data found for locale: ${locale}`);
        }
        

    } catch (error) {
        // 3. If an error was thrown (due to 4xx status or network issue), redirect.
        console.error("Token validation failed, redirecting:", error);
        
        // Use a 303 status for post-action redirects, or 302/307 for temporary changes.
        // Since this is a check, 302 is fine, but 303 is often clearer for navigation.
        throw redirect(302, '/' + locale);
    }

    // This data is passed directly to your +page.svelte as the 'data' prop
    return {
        uuid: uuid,
        main_guest_id,
        main_guest_name,
        main_guest_vat,
        main_guest_email,
        check_in_date,
        check_out_date,
        special_request,
        reservation_id
        // You would typically fetch the existing reservation data here too,
        // but for this example, we only return the UUID.
    };
};