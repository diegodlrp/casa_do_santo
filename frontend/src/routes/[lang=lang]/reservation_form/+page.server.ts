import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

//export const prerender = true;

export const load: PageServerLoad = async ({ locals: { LL } }) => {
    const locale = LL.locale();
    
    let title_title = '';
    let title_subtitle = '';
    let title_img = '';

    let contact_title = '';
    let contact_content = '';
    let contact_img = '';

    let contact_phone = '';
    let contact_email = '';
    let contact_address = '';
    let contact_address_link = '';

    let form_title = '';
    let form_subtitle = '';
    let form_img = '';

    let error: string | null = null;

    try {
        // Fetch title data
        const titleResponse = await apiRequest(`/page_content/reservationcontact_title_content/?lang=${locale}`);
        if (titleResponse) {
            title_title = titleResponse.title || '';
            title_subtitle = titleResponse.excerpt || '';
            title_img = titleResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
        }

        // Fetch contact data
        const contactResponse = await apiRequest(`/page_content/reservationcontact_page_content/?lang=${locale}`)
        if (contactResponse){
            contact_title = contactResponse.title || '';
            contact_content = contactResponse.content || '';
            contact_img = contactResponse.image || '';

        } else {
            console.warn(`No contact data found for locale: ${locale}`);
        }

        // Fetch base data
        const baseResponse = await apiRequest(`/basedata/1/?lang=${locale}`)
        if (baseResponse){
            contact_phone = baseResponse.phone || '';
            contact_email = baseResponse.email || '';
            contact_address = baseResponse.address || '';
            contact_address_link = baseResponse.address_link || '';

        } else {
            console.warn(`No contact data found for locale: ${locale}`);
        }
        // Fetch reservation form data
        const reservationResponse = await apiRequest(`/page_content/reservationform_page_content/?lang=${locale}`);
        if (reservationResponse) {
            form_title = reservationResponse.title || '';
            form_subtitle = reservationResponse.excerpt || '';
            form_img = reservationResponse.image || '';
        } else {
            console.warn(`No reservation form data found for locale: ${locale}`);
        }
    }catch (e: any) {
        console.error('Error fetching data for page:', e);
        error = e; // Capture error message
    }

    return {
        title_title,
        title_subtitle,
        title_img,
        contact_title,
        contact_content,
        contact_img,
        contact_phone,
        contact_email,
        contact_address,
        contact_address_link,
        form_title,
        form_subtitle,
        form_img,
        locale,
        error
    }
}
