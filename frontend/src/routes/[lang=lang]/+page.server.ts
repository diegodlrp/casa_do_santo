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

    let services_content_title = '';
    let services_content_subtitle = '';
    let services_data: any[] = [];
 

    let rules_content_title = '';
    let rules_content_subtitle = '';
    let rules_data: any[] = [];

    let about_us_title = '';
    let about_us_subtitle = '';
    let about_us_content = '';
    let about_us_img = '';

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

        // Fetch services data
        const servicesResponse = await apiRequest(`/page_content/services_page_content/?lang=${locale}`);
        if (servicesResponse) {
            services_content_title = servicesResponse.title;
            services_content_subtitle = servicesResponse.excerpt;
            services_data = await apiRequest(`/tags/services/page_content/?lang=${locale}`);

        } else {
            console.warn(`No service data found for locale: ${locale}`)
        }

        // Fetch rules data
        const rulesResponse = await apiRequest(`/page_content/rules_page_content/?lang=${locale}`);
        if (rulesResponse) {
            rules_content_title = rulesResponse.title;
            rules_content_subtitle = rulesResponse.excerpt;
            rules_data = await apiRequest(`/tags/rules/page_content/?lang=${locale}`);

        } else {
            console.warn(`No rules data found for locale: ${locale}`)
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
        services_content_title,
        services_content_subtitle,
        services_data,
        rules_content_title,
        rules_content_subtitle,
        rules_data,
        about_us_title,
        about_us_subtitle,
        about_us_content,
        about_us_img,
        form_title,
        form_subtitle,
        form_img,
        form_content,
        error
    };
}
