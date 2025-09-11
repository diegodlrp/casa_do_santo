<script lang="ts">
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";
    import Lightbox from "$lib/Lightbox.svelte";

    export let data: PageData;
    let selected_index: number | null = null;

    // Destructure the data directly
    $: title = data.title;
    $: subtitle = data.subtitle;
    $: img = data.img;
    $: img_data = data.img_data;
    $: error = data.error;

    function openLightbox(index: number) {
		selected_index = index;
	}

	function closeLightbox() {
		selected_index = null;
	}
</script>

<Title {title} {subtitle} {img} />
<div class="py-12 px-4 z-950 min-h-[calc(100vh-20px)]">
    <div class="container mx-auto">
        {#if img_data.length > 0}
            <div class="masonry-grid">
                {#each img_data as image, i}
                    <div
                        class="group relative overflow-hidden shadow-lg cursor-pointer bg-amber-50"
                        onclick={() => openLightbox(i)}
                        role="button"
                        tabindex="0"
                        onkeypress={(e) => e.key === "Enter" && openLightbox(i)}
                    >
                        <img
                            src={image.src}
                            alt={image.alt}
                            class="w-full h-auto object-cover transition-transform duration-500 ease-in-out group-hover:scale-110"
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


<style>
.masonry-grid {
    /* Use CSS columns for a masonry effect */
    column-count: 2; /* Default for small screens */
    column-gap: 1rem;
  }
  
  @media (min-width: 768px) {
    .masonry-grid {
      column-count: 3; /* For medium screens */
    }
  }
  
  @media (min-width: 1024px) {
    .masonry-grid {
      column-count: 4; /* For large screens */
    }
  }
  
  .masonry-grid > div {
    /* Prevent images from being cut off between columns */
    break-inside: avoid;
    margin-bottom: 1rem; /* This creates the vertical gap between images */
  }
  
  .masonry-grid img {
    /* Ensure images fill their container and maintain aspect ratio */
    width: 100%;
    height: auto;
  }
</style>