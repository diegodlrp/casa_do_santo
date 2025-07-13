import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

export const prerender = true;

export const load: PageServerLoad = async ({ locals: { LL } }) => {
    const locale = LL.locale();

    let title = '';
    let content = '';
    let img = '';

    let rooms_data: any[] = [];
    
    let title_title = '';
    let title_subtitle = '';
    let title_img = '';

    let form_title = '';
    let form_subtitle = '';
    let form_img = '';

    let error: string | null = null;

    try {
        // Fetch title data
        const titleResponse = await apiRequest(`/page_content/contact_title_content/?lang=${locale}`);
        if (titleResponse) {
            title_title = titleResponse.title || '';
            title_subtitle = titleResponse.excerpt || '';
            title_img = titleResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
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
        title,
        subtitle,
        img,
        error
    }
}