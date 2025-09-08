<script lang="ts">
    import ReservationForm from "$lib/ReservationForm.svelte";
	import type { PageData } from "./$types";

	export let data: PageData;

    $: form_title = data.form_title;
    $: form_subtitle = data.form_subtitle;
    $: form_img = data.form_img;
    $: form_content = data.form_content;

</script>

<!-- HOME Reservation FormT -->
<div id="home_page_reservation_form h-[calc(100vh-16px)] sm:h-[calc(100vh-20px)]">
	<ReservationForm
		title={form_title}
		subtitle={form_subtitle}
		img={form_img}
		content={form_content}
	/>

	<div class="min-h-[64px]"></div>
</div>
<!-- END -->