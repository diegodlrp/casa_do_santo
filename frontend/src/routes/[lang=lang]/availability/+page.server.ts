import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

//export const prerender = true;

export const entries = () => {
    return [
        { lang: 'es' },
        { lang: 'en' },
        { lang: 'gl' }
    ];
};

export const load: PageServerLoad = async ({ locals: { LL } }) => {
    const locale = LL.locale();
    let title = '';
    let img = '';
    let address = '';
    let email = '';
    let phone = '';

    let page_content_title = '';
    let page_content_subtitle = '';
    let page_img = '';
    let page_content = '';

    let form_title = '';
    let form_subtitle = '';
    let form_img = '';
    let form_content = '';
    let error: string | null = null;

    try {
        // Fetch title data
        const titleResponse = await apiRequest(`/page_content/home_title_content/?lang=${locale}`);
        if (titleResponse) {
            title = titleResponse.title || '';
            img = titleResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
        }

        // Fetch title data
        const contentResponse = await apiRequest(`/page_content/home_page_content/?lang=${locale}`);
        if (titleResponse) {
            page_content_title = contentResponse.title || '';
            page_content_subtitle = contentResponse.excerpt || '';
            page_img = contentResponse.image || '';
            page_content = contentResponse.content || '';
        } else {
            console.warn(`No page data found for locale: ${locale}`);
        }

        // Fetch reservation form data
        const reservationResponse = await apiRequest(`/page_content/reservationform_page_content/?lang=${locale}`);
        if (reservationResponse) {
            form_title = reservationResponse.title || '';
            form_subtitle = reservationResponse.excerpt || '';
            form_img = reservationResponse.image || '';
            form_content = reservationResponse.content || '';
        } else {
            console.warn(`No reservation form data found for locale: ${locale}`);
        }
    }catch (e: any) {
        console.error('Error fetching data for page:', e);
        error = e; // Capture error message
    }

    return {
        title,
        img,
        address,
        email,
        phone,
        page_content_title,
        page_content_subtitle,
        page_img,
        page_content,
        form_title,
        form_subtitle,
        form_img,
        form_content,
        error
    };
}
