import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

//export const prerender = true;

export const load: PageServerLoad = async ({ locals: { LL } }) => {
    const locale = LL.locale();

    let title_title = '';
    let title_subtitle = '';
    let title_img = '';

    let title = '';
    let subtitle = '';
    let img = '';

    let carrousel_title = '';
    let carrousel_subtitle = '';
    let carrousel_img = '';

    let carrousel_data: any[] = [];

    let form_title = '';
    let form_subtitle = '';
    let form_img = '';

    let error: string | null = null;

    try {
        // Fetch title data
        const titleResponse = await apiRequest(`/page_content/location_title_content/?lang=${locale}`);
        if (titleResponse) {
            title_title = titleResponse.title || '';
            title_subtitle = titleResponse.excerpt || '';
            title_img = titleResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
        }

        // Fetch locations data
        const locationResponse = await apiRequest(`/page_content/location_page_content/?lang=${locale}`);
        if (locationResponse) {
            title = locationResponse.title || '';
            subtitle = locationResponse.excerpt || '';
            img = locationResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
        }

        // Fetch carrousel data
        const carrouselResponse = await apiRequest(`/page_content/locationcarrousel_page_content/?lang=${locale}`);
        if (carrouselResponse){
            carrousel_title = carrouselResponse.title || '';
            carrousel_subtitle = carrouselResponse.excerpt || '';
            carrousel_img = carrouselResponse.image || '';
        }else {
            console.warn(`No carrousel data found for locale: ${locale}`);
        }

        // Fetch carrousel data
        const carrouselDataResponse = await apiRequest(`/tags/locations/page_content/?lang=${locale}`);
        if (carrouselDataResponse){
            carrousel_data = carrouselDataResponse;
        }else {
            console.warn(`No carrousel data form data found for locale: ${locale}`);
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
        title,
        subtitle,
        img,
        carrousel_title,
        carrousel_subtitle,
        carrousel_img,
        carrousel_data,
        form_title,
        form_subtitle,
        form_img,
        error
    }
}
