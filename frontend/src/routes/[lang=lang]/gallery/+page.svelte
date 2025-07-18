<script lang="ts">
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";
    import Lightbox from "$lib/Lightbox.svelte";

    export let data: PageData;
    let selected_index: number | null = null;

    // Destructure the data directly
    const { title, subtitle, img, img_data, error } = data;

    function openLightbox(index: number) {
		selected_index = index;
	}

	function closeLightbox() {
		selected_index = null;
	}
</script>

<Title {title} {subtitle} {img} />
<div class="py-12 px-4 z-950">
    <div class="container mx-auto">
        {#if img_data.length > 0}
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {#each img_data as image, i}
                    <div
                        class="group relative overflow-hidden shadow-lg cursor-pointer bg-amber-50
                        {i % 7 === 0 ? 'md:col-span-2 md:row-span-2' : ''}
                        {i % 9 === 0 ? 'lg:col-span-1 lg:row-span-2' : ''}"
                        onclick={() => openLightbox(i)}
                        role="button"
                        tabindex="0"
                        onkeypress={(e) => e.key === "Enter" && openLightbox(i)}
                    >
                    <img
                    src={image.src}
                    alt={image.alt}
                    class="w-full h-full object-cover transition-transform duration-500 ease-in-out group-hover:scale-110"
                    loading="lazy"
                />
                </div>
                {/each}
            </div>
        {/if}
    </div>
</div>
{#if selected_index !== null}
	<Lightbox images={img_data} current_index={selected_index} on:close={closeLightbox} />
{/if}
