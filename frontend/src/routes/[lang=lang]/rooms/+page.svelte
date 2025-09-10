<script lang="ts">
    import type { PageData } from "./$types";
    import { LL } from "$i18n/i18n-svelte";
    import Title from "$lib/Title.svelte";
    import ReservationForm from "$lib/ReservationForm.svelte";

    export let data: PageData;

    // Destructure the data directly
    const {
        img,
        title_img,
        error,
    } = data;

    $: title = data.title;
    $: content = data.content;
    $: rooms_data = data.rooms_data;
    $: title_title = data.title_title;
    $: title_subtitle = data.title_subtitle;
    
</script>

<Title title={title_title} subtitle={title_subtitle} img={title_img} />
<!-- ROOMS PAGE CONTENT -->
<div class="min-h-[calc(100vh-264px)] sm:min-h-[calc(100vh-280px)]">
    <div class=" min-h-[64px]"></div>

    <div class="p-4 relative z-10 rounded-4xl">
        <div class="container home_main_container">
            <div class="home_main_text text-center">
                <h2 class="pt-3 pb-4">{@html title}</h2>

                <br />

                <h4>{@html content}</h4>

                <br />
            </div>

            <div
                class="relative pt-16 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center z-20"
            >
                <a href="#rooms_list" class="mt-8 inline-block text-3xl animate-bounce">
                    &#8659;
                </a>
            </div>
        </div>
    </div>



    <div class=" min-h-[64px]"></div>
</div>
<!-- END -->
<!-- ROOMS LIST -->
<div id="rooms_list">
    {#each rooms_data as room, index}
        <div
            class="relative w-[100%] h-[calc(100vh-84px)] sm:h-[calc(100vh-100px)] overflow-hidden"
        >
            <!-- background img -->
            <div
                class="h-[calc(100%+450px)] w-full bg-cover bg-center absolute -top-[450px]"
                data-translatey="400"
                data-when="span"
                data-from="0"
                data-to="1"
                data-easing="linear"
                style="background-image: url({room.image}); opacity: 1; "
            ></div>

            <!-- text -->
            <div
                class="absolute h-[100%] bg-[color:var(--color-bg-dark)]/80 xl:w-[30%]"
                class:room_bg={index % 2 === 1}
				class:room_bg_right={index % 2 === 0}
            >
                <div class="py-0 px-[65px] mt-[160px]">
                    <img
                        src="/svg/core_bg.svg"
                        alt="core_bg"
                        class="bg-cover bg-center absolute h-full "
                    />

                    <h2 class="text-center m-[30px]">{@html room.title}</h2>
                    
                    <h3 class="text-center text-[27px]">{@html room.excerpt}</h3>

                    <div class="text-base text-white leading-[31px] font-montserrat text-center">{@html room.content}</div>

                    <a
        href="gallery?room={room.slug}"
        type="submit"
        class="core_button left-1/2 -translate-x-1/2 px-6 py-2 mt-[30px] absolute hover:scale-105 active:scale-95 transition"
    >
        {$LL.more_photos()}
    </a>
                </div>
            </div>

        </div>
    {/each}
</div>
<!-- END -->
<!-- ROOMS Reservation Form -->

<!-- END -->
