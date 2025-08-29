import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

//export const prerender = true;

export const load: PageServerLoad = async ({ locals: { LL } }) => {
    const locale = LL.locale();

    let title_title = '';
    let title_subtitle = '';
    let title_img = '';

    let percentage_true: any[] = [];
    let percentage_false: any[] = [];

    let rate_data: any[] = [];

    let error: string | null = null;
    const titleResponse = await apiRequest(`/calendar/available-dates/`);
    try {
        // Fetch title data
        const titleResponse = await apiRequest(`/page_content/rates_title_content/?lang=${locale}`);
        if (titleResponse) {
            title_title = titleResponse.title || '';
            title_subtitle = titleResponse.excerpt || '';
            title_img = titleResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
        }

        const discountResponse = await apiRequest(`/discount/?lang=${locale}`);
        if (discountResponse) {
            percentage_true = discountResponse["percentage_true"]
            percentage_false = discountResponse["percentage_false"]
        } else {
            console.warn(`No discountResponse data found for locale: ${locale}`);
        }

        rate_data = await apiRequest(`/calendar/price-data-ranges/`);
        

    } catch (e: any) {
        console.error('Error fetching data for page:', e);
        error = e; // Capture error message
    }

    return {
        title_title,
        title_subtitle,
        title_img,
        percentage_true,
        percentage_false,
        rate_data,
        error
    }
}
