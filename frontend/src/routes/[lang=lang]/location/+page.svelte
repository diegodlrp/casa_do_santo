<script lang="ts">
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";
    import ReservationForm from "$lib/ReservationForm.svelte";
    import Carrousel from "$lib/Carrousel.svelte";
    import Services from "$lib/Services.svelte";
    import { onMount } from "svelte";

    import { setOptions, importLibrary } from "@googlemaps/js-api-loader";

    export let data: PageData;

    $: title_title = data.title_title;
    $: title_subtitle = data.title_subtitle;
    $: title_img = data.title_img;
    $: title = data.title;
    $: subtitle = data.subtitle;
    $: img = data.img;
    $: content = data.content;
    $: carrousel_title = data.carrousel_title;
    $: carrousel_subtitle = data.carrousel_subtitle;
    $: carrousel_img = data.carrousel_img;
    $: carrousel_data = data.carrousel_data;
    $: carrousel_activity_title = data.carrousel_activity_title;
    $: carrousel_activity_subtitle = data.carrousel_activity_subtitle;
    $: carrousel_activity_img = data.carrousel_activity_img;
    $: carrousel_activity_data = data.carrousel_activity_data;
    $: logo_map_img = data.logo_map_img;
    $: routes_content_title = data.routes_content_title;
    $: routes_content_subtitle = data.routes_content_subtitle;
    $: routes_data = data.routes_data;

    let mapDiv: HTMLDivElement;

    onMount(async () => {
        // 🔑 Configurar Google Maps
        setOptions({
            key: "AIzaSyATa5X8tqNoCati6u4Ki_LppgDsvSlvDF4",
        });

        // 📦 Cargar librerías necesarias
        const { Map } = await importLibrary("maps");
        const { Marker } = await importLibrary("marker");

        const location = { lat: 42.8568341, lng: -8.5884587 };

        const map = new Map(mapDiv, {
            center: location,
            zoom: 10,
            mapTypeId: "hybrid",
            disableDefaultUI: false,
            zoomControl: true,
            mapTypeControl: true,
        });

        // 📍 Marcador principal
        new Marker({
            position: location,
            map,
            title: "Casa do Santo",
            icon: {
                url: logo_map_img,
                scaledSize: new google.maps.Size(40, 40),
            },
        });

        // 📍 Marcadores dinámicos desde carrousel_data
        carrousel_data?.forEach((item) => {
            if (!item?.excerpt) return;

            const [latStr, lngStr] = item.excerpt.split(";");

            const lat = Number(latStr);
            const lng = Number(lngStr);

            if (isNaN(lat) || isNaN(lng)) {
                console.warn("Coordenadas inválidas:", item.excerpt);
                return;
            }

            new Marker({
                position: { lat, lng },
                map,
                title: item.title,
            });
        });
    });
</script>


<Title title={title_title} subtitle={title_subtitle} img={title_img} />
<div
    class="relative w-[100%] h-[calc(100vh-264px)] sm:h-[calc(100vh-280px)] overflow-hidden"
>
    <div bind:this={mapDiv} class="w-full h-full"></div>
</div>

<!-- start Location page content -->
<div class="pt-[36px] pb-[100px] relative w-full">
    <img
        src="/svg/core_bg_dark.svg"
        alt="core_bg"
        class="bg-cover bg-center absolute h-full right-0"
    />
    <div class="min-h-[64px]"></div>
    <div class="p-4 relative">
        <div class="container">
            <div>
                <h2 class="text-center m-[30px]">{@html title}</h2>
            </div>

            <div>
                <!-- <h3 class="text-center text-[27px]">
					<span class="text_dark">{@html subtitle}</span>
				</h3> -->

                <h4 class="text_dark text-center">{@html subtitle}</h4>
                <br />
                <p class="text_dark text-center">{@html content}</p>
            </div>
        </div>
    </div>
</div>

<!-- END -->
<div
    class="inset-0 bg-cover bg-center carrousel_core"
    style="background-image: url({carrousel_img});"
>
    <div class="w-full h-full bg-[color:var(--color-bg-dark)] pt-[30px]">
        <h2 class="text-center">{@html carrousel_title}</h2>
        <h3 class="text-center">{@html carrousel_subtitle}</h3>
        <Carrousel data={carrousel_data} dark={false} />
    </div>

    <div class="w-full h-full bg-[color:var(--color-bg-light)] pt-[30px]">
        <h2 class="text-center text-[color:var(--color-text-dark)]">
            {@html carrousel_activity_title}
        </h2>
        <h3 class="text-center text-[color:var(--color-text-dark)]">
            {@html carrousel_activity_subtitle}
        </h3>
        <Carrousel data={carrousel_activity_data} dark={true} />
    </div>

    <div class="bg-[color:var(--color-bg-dark)] border-b-2 border-[color:var(--color-text-caption)]">
        <Services
            title={routes_content_title}
            subtitle={routes_content_subtitle}
            data={routes_data}
        />
    </div>
</div>
