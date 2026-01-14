import type { PageServerLoad } from './$types'
import { apiRequest } from '$lib/services/apiService';

// export const prerender = true;

export const load: PageServerLoad = async ({ locals: { LL }, url, depends }) => {
    // Add this line to tell SvelteKit that this load function depends on the URL's search string.
    // This will cause the load function to re-run whenever the query parameters change.
    depends('url:search'); 

    const locale = LL.locale();
    const room = url.searchParams.get('room');

    let title = '';
    let subtitle = '';
    let img = '';

    let img_data: { alt: string; src: string }[] = [];

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
        if (room) {
            // Fetch image data
            const imageResponse = await apiRequest('/page_content/'+room+'/?lang=${locale}');
            if (imageResponse) {

                img_data = imageResponse.gallery_images.map((result: any) => ({
                    alt: result['caption'],
                    src: result['image_file']
                }));
            } else {
                console.warn(`No images `+room+` data found for locale: ${locale}`);
            }
        } else {
            // Fetch image data
            const imageResponse = await apiRequest('/images/');
            if (imageResponse) {
                img_data = imageResponse.map((result: any) => ({
                    alt: result['caption'],
                    src: result['image_file']
                }));
            } else {
                console.warn(`No images data found for locale: ${locale}`);
            }

        }


    } catch (e: any) {
        console.error('Error fetching data for page:', e);
        error = e; // Capture error message
    }

    return {
        title,
        subtitle,
        img,
        img_data,
        error
    }
}