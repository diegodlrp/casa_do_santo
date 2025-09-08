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
    let content = '';

    let carrousel_title = '';
    let carrousel_subtitle = '';
    let carrousel_img = '';

    let carrousel_data: any[] = [];

    let carrousel_activity_title = '';
    let carrousel_activity_subtitle = '';
    let carrousel_activity_img = '';

    let logo_map_img = '';

    let carrousel_activity_data: any[] = [];

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
            content = locationResponse.content || '';
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

        // Fetch carrousel data
        const carrouselActivityResponse = await apiRequest(`/page_content/carrusel-actividades/?lang=${locale}`);
        if (carrouselActivityResponse){
            carrousel_activity_title = carrouselActivityResponse.title || '';
            carrousel_activity_subtitle = carrouselActivityResponse.excerpt || '';
            carrousel_activity_img = carrouselActivityResponse.image || '';
        }else {
            console.warn(`No carrousel data found for locale: ${locale}`);
        }

        // Fetch carrousel data
        const carrouselDataActivityResponse = await apiRequest(`/tags/actividades/page_content/?lang=${locale}`);
        if (carrouselDataActivityResponse){
            carrousel_activity_data = carrouselDataActivityResponse;
        }else {
            console.warn(`No carrousel data form data found for locale: ${locale}`);
        }

        // Fetch basic data
        const basicDataActivityResponse = await apiRequest(`/basedata/?lang=${locale}`);
        if (basicDataActivityResponse){
           logo_map_img = basicDataActivityResponse[0]["logo"];
        }else {
            console.warn(`No carrousel data form data found for locale: ${locale}`);
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
        content,
        carrousel_title,
        carrousel_subtitle,
        carrousel_img,
        carrousel_data,
        carrousel_activity_title,
        carrousel_activity_subtitle,
        carrousel_activity_img,
        carrousel_activity_data,
        logo_map_img,
        error
    }
}
