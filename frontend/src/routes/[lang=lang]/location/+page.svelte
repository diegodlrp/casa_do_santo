<script lang="ts">
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";
    import ReservationForm from "$lib/ReservationForm.svelte";
    import Carrousel from "$lib/Carrousel.svelte";

    export let data: PageData;

    // Destructure the data directly
    $: title_title = data.title_title;
    $: title_subtitle = data.title_subtitle;
    $: title_img = data.title_img;
    $: title = data.title;
    $: subtitle = data.subtitle;
    $: img = data.img;
    $: carrousel_title = data.carrousel_title;
    $: carrousel_subtitle = data.carrousel_subtitle;
    $: carrousel_img = data.carrousel_img;
    $: carrousel_data = data.carrousel_data;
    $: form_title = data.form_title;
    $: form_subtitle = data.form_subtitle;
    $: form_img = data.form_img;
</script>

<Title title={title_title} subtitle={title_subtitle} img={title_img} />
<div
    class="relative w-[100%] min-h-[calc(100vh-20px)] sm:h-[calc(100vh-36px)] overflow-hidden"
></div>

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
        <h2 class="text-center ">{@html carrousel_title}</h2>
        <h3 class="text-center">{@html carrousel_subtitle}</h3>
        <Carrousel data={carrousel_data} />
    </div>
</div>

<ReservationForm title={form_title} subtitle={form_subtitle} img={form_img} />
