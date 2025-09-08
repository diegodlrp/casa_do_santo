<script lang="ts">
    import { onDestroy } from "svelte";
    import Swiper from "swiper";
    import { Navigation, Pagination } from 'swiper/modules';
    import "swiper/css";
    import "swiper/css/navigation";
    import "swiper/css/pagination";

    export let data: any[] = [];

    let swiperInstance: Swiper | undefined;
    let swiperContainer: HTMLDivElement | undefined;

    $: if (swiperContainer) {
        swiperInstance = new Swiper(swiperContainer, {
            modules: [Navigation, Pagination],
            slidesPerView: 4,
            spaceBetween: 10,
            loop: true,
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            breakpoints: {
                // Extra small devices (phones, less than 600px)
                320: {
                    slidesPerView: 1,
                    spaceBetween: 10,
                },
                // Small devices (tablets, 600px and up)
                640: {
                    slidesPerView: 2,
                    spaceBetween: 20,
                },
                // Medium devices (laptops, 992px and up)
                992: {
                    slidesPerView: 3,
                    spaceBetween: 30,
                },
                // Large devices (desktops, 1200px and up)
                1200: {
                    slidesPerView: 4,
                    spaceBetween: 40,
                },
                // You can add even larger breakpoints if needed
            },
        });
    }

    onDestroy(() => {
        if (swiperInstance) {
            swiperInstance.destroy(true, true); // Recommended to pass arguments
        }
    });
</script>

<div class="swiper w-[100%] h-[100%] pt-32" bind:this={swiperContainer}>
    <ul class="swiper-wrapper p-5 pt-32">
        {#each data as location}
            <li
                class="swiper-slide h-auto cursor-pointer rounded-md hover:shadow-2xl hover:-translate-y-1 duration-300"
            >
                <div>
                    <div>
                        <img
                            class="w-[calc(100% -2rem)] h-42 absolute -top-5 left-1/2 transform -translate-x-1/2 -translate-y-1/2 duration-200 shadow-1xl rounded border border-[color:var(--color-text-caption)]"
                            src={location.image}
                            alt={location.slug}
                        />
                        <h2 class="pt-[30px] text-[color:var(--color-text-caption)] text-center">{@html location.title}</h2>
                        <p class="text-[color:var(--color-text)] text-center">{@html location.content}</p>
                    </div>
                </div>
            </li>
        {/each}
    </ul>

    <div class="swiper-pagination"></div>
    <div class="swiper-button-prev"></div>
    <div class="swiper-button-next"></div>
</div>
