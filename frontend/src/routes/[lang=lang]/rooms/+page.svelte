<script lang="ts">
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";
    import ReservationForm from "$lib/ReservationForm.svelte";

    export let data: PageData;

    // Destructure the data directly
    const {
        title,
        content,
        img,
        rooms_data,
        title_title,
        title_subtitle,
        title_img,
        form_title,
        form_subtitle,
        form_img,
        error,
    } = data;
    console.log("data", data);
</script>

<Title title={title_title} subtitle={title_subtitle} img={title_img} />
<!-- ROOMS PAGE CONTENT -->
<div class="min-h-[calc(100vh-264px)] sm:min-h-[calc(100vh-280px)]">aaa</div>
<!-- END -->
<!-- ROOMS LIST -->
<div id="rooms_list">
    {#each rooms_data as room, index}
        <div
            class="relative w-[100%] h-[calc(100vh-84px)] sm:h-[calc(100vh-100px)] overflow-hidden"
        >
            <!-- background img -->
            <div
                class="h-[calc(100%+450px)] w-full bg-cover bg-center absolute -top-[450px] -scale-x-100"
                data-translatey="400"
                data-when="span"
                data-from="0"
                data-to="1"
                data-easing="linear"
                style="background-image: url({room.image}); opacity: 1; transform: translate3d(0px, 270px, 0px) rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale3d(1, 1, 1);"
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
                        class="bg-cover bg-center absolute h-full right-0"
                    />

                    <h2 class="text-center m-[30px]">{@html room.title}</h2>

                    <h3 class="text-center text-[27px]">{@html room.excerpt}</h3>

                    <div class="text-base text-white leading-[31px] font-montserrat text-center">{@html room.content}</div>

                    <a href="gallery" type="submit" class="core_button absolute">'more_photos'</a>
                </div>
            </div>

        </div>
    {/each}
</div>
<!-- END -->
<!-- ROOMS Reservation Form -->
<div id="home_page_reservation_form">
    <ReservationForm
        title={form_title}
        subtitle={form_subtitle}
        img={form_img}
    />
</div>
<!-- END -->
