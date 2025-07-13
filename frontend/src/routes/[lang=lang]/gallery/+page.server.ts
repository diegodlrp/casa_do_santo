import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

export const prerender = true;

export const load: PageServerLoad = async ({ locals: { LL } }) => {
    const locale = LL.locale();

    let title = '';
    let subtitle = '';
    let img = '';
    let error: string | null = null;

    try {
        // Fetch title data
        const titleResponse = await apiRequest(`/page_content/gallery_title_content/?lang=${locale}`);
        if (titleResponse) {
            title = titleResponse.title || '';
            subtitle = titleResponse.excerpt || '';
            img = titleResponse.image || '';
        } else {
            console.warn(`No title data found for locale: ${locale}`);
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