import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

//export const prerender = true;

export const load: PageServerLoad = async ({ locals: { LL } }) => {
    const locale = LL.locale();

    let title = '';
    let content = '';
    let img = '';

    let rooms_data: any[] = [];
    
    let title_title = '';
    let title_subtitle = '';
    let title_img = '';

    let error: string | null = null;

    try {
        // Fetch rooms page data
        const roomsResponse = await apiRequest(`/page_content/rooms_page_content/?lang=${locale}`);
        if (roomsResponse) {
            title = roomsResponse.title || '';
            content = roomsResponse.content || '';
            img = roomsResponse.image || '';
        } else {
            console.warn(`No room page data found for locale: ${locale}`);
        }

        // Fetch rooms data
        rooms_data = await apiRequest(`/tags/rooms/page_content/?lang=${locale}`);

        // Fetch title data
        const titleResponse = await apiRequest(`/page_content/rooms_title_content/?lang=${locale}`);
        if (titleResponse) {
            title_title = titleResponse.title || '';
            title_subtitle = titleResponse.excerpt || '';
            title_img = titleResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
        }


    }catch (e: any) {
        console.error('Error fetching data for page:', e);
        error = e; // Capture error message
    }

    return {
        title,
        content,
        img,
        rooms_data,
        title_title,
        title_subtitle,
        title_img,
        error
    }
}
