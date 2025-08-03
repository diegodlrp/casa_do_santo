import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

export const prerender = true;

export const entries = () => {
    return [
        { lang: 'es' },
        { lang: 'en' },
        { lang: 'gl' }
    ];
};

export const load: PageServerLoad = async ({ locals: { LL } }) => {
	const locale = LL.locale();
    console.log('La función de carga se está ejecutando');
	let title = '';
    let img = '';
    let address = '';
    let email = '';
    let phone = '';

    let page_content_title = '';
    let page_content_subtitle = '';
    let page_content = '';

    let about_us_title = '';
    let about_us_subtitle = '';
    let about_us_content = '';
    let about_us_img = '';

    let form_title = '';
    let form_subtitle = '';
    let form_img = '';
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
            page_content = contentResponse.content || '';
        } else {
            console.warn(`No page data found for locale: ${locale}`);
        }

        // Fetch about us data
        const aboutUsResponse = await apiRequest(`/page_content/aboutus_page_content/?lang=${locale}`);
        if (titleResponse) {
            about_us_title = aboutUsResponse.title || '';
            about_us_subtitle = aboutUsResponse.excerpt || '';
            about_us_content = aboutUsResponse.content || '';
            about_us_img = aboutUsResponse.image || '';
        } else {
            console.warn(`No about us data found for locale: ${locale}`);
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
        img,
        address,
        email,
        phone,
        page_content_title,
        page_content_subtitle,
        page_content,
        about_us_title,
        about_us_subtitle,
        about_us_content,
        about_us_img,
        form_title,
        form_subtitle,
        form_img,
        error
    };
}
