<script lang="ts">
	import RiPhoneLine from "svelte-remixicon/RiPhoneLine.svelte";
	import RiMailLine from "svelte-remixicon/RiMailLine.svelte";
	import RiMapPin2Line from "svelte-remixicon/RiMapPin2Line.svelte";
	import type { PageData } from "./$types";
	import ReservationForm from "$lib/ReservationForm.svelte";
	import Services from "$lib/Services.svelte";
	import { onMount } from "svelte";

	export let data: PageData;

	// Destructure the data directly
	const { img, address, email, phone, about_us_img, form_img, error } = data;

	$: title = data.title;
	$: page_content_title = data.page_content_title;
	$: page_content_subtitle = data.page_content_subtitle;
	$: page_img = data.page_img;
	$: services_content_title = data.services_content_title;
	$: services_content_subtitle = data.services_content_subtitle;
	$: services_data = data.services_data;
	$: rules_content_title = data.rules_content_title;
	$: rules_content_subtitle = data.rules_content_subtitle;
	$: rules_data = data.rules_data;
	$: page_content = data.page_content;
	$: about_us_title = data.about_us_title;
	$: about_us_subtitle = data.about_us_subtitle;
	$: about_us_content = data.about_us_content;
	$: form_title = data.form_title;
	$: form_subtitle = data.form_subtitle;
	$: form_content = data.form_content;
	$: logo_map_img = data.logo_map_img;
	let mapDiv: HTMLDivElement;

	onMount(() => {
		// Replace with your real Casa do Santo coordinates
		const location = { lat: 42.8568341, lng: -8.5884587 };

		const map = new google.maps.Map(mapDiv, {
			zoom: 10,
			center: location,
			mapTypeId: google.maps.MapTypeId.HYBRID, // satellite by default
			disableDefaultUI: false, // keep default controls
			zoomControl: true, // force zoom buttons
			mapTypeControl: true, // allow switching (optional)
		});
		const icon = {
			url: logo_map_img, // The image URL
			scaledSize: new google.maps.Size(40, 40), // The size of the icon in pixels
		};

		new google.maps.Marker({
			position: location,
			map,
			title: "Casa do Santo",
			icon: icon,
		});
	});
</script>

<!-- HOME PAGE TITLE -->
<div
	id="home_page_title"
	class="relative h-[calc(100vh-4rem)] sm:h-[calc(100vh-5rem)] overflow-hidden"
>
	<div
		class="absolute inset-0 bg-cover bg-center"
		style="background-image: url({img});"
	>	
		<!-- Address/email info -->
		<div class="start_info flex items-center gap-8 flex-row">
			<div class="flex justify-between items-center w-full">
				<div class="pl-4">
					<span
						class="email_icon flex items-center gap-x-1 text-white"
					>
						<RiMapPin2Line />
						{address}
					</span>
				</div>

				<div class="pr-4 flex gap-x-8">
					<a
						href="mailto:{email}"
						class="email_icon flex items-center gap-x-1 text-white"
					>
						<RiMailLine />
						{email}
					</a>
				</div>
			</div>
		</div>
	</div>

	<div
		class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center z-20"
	>
		<h1
			class="text-white text-5xl md:text-7xl font-bold text-shadow-lg leading-tight"
		>
			{@html title}
		</h1>
		<br />
		<a
			href="#home_page_content"
			class="mt-8 inline-block text-white text-3xl animate-bounce"
		>
			&#8659;
		</a>
	</div>
</div>
<!-- END -->

<!-- HOME PAGE CONTENT -->
<div
	id="home_page_content"
	class=" relative w-full bg-cover bg-center text-[color:var(--color-text)]"
	style="background-image: url({page_img}); opacity: 1;"
>
	<div
		class="w-[100%] h-[100%] pt-[36px] pb-[100px] bg-[color:var(--color-bg-light)]/80"
	>
		
		<div class="min-h-[64px]"></div>
		<div class="p-0 sm:p-4 w-full">
			<div class="container max-w-6xl ">
				<div class="mt-8 md:mt-16"></div> 
		
				<header class="text-center mb-10 space-y-4 max-w-4xl mx-auto">
					<h2 class="text-xl sm:text-2xl font-normal">
						{@html page_content_title}
					</h2>
					<h3 class="text-3xl sm:text-4xl">
						<span class="text_dark">
							{@html page_content_subtitle}
						</span>
					</h3>
				</header>
		
				<main class="text_dark text-lg leading-relaxed space-y-4 text-center">
					{@html page_content} 
				</main>
			</div>
		</div>
	</div>
</div>
<!-- END -->

<!-- HOME About Us -->
<div
	id="home_page_about_us"
	class="bg-cover bg-center"
	style="background-image: url({about_us_img}); opacity: 1;"
>
	<div class="relative py-0 md:py-0 bg-[color:var(--color-bg-dark)]/80">
		<div class="flex flex-col md:flex-row">
			<div class="w-full md:w-1/3">
				<img src={about_us_img} alt="about_us" class="w-full" />
			</div>

			<div class="w-full md:w-2/3 bg-cover bg-center">
				<div class="relative h-[100%]">
					<div class="px-0 sm:px-10 md:px-16 lg:px-[65px] py-0 xl:mt-[160px] lg:mt-[90px] md:mt-[40px]">
						<img
							src="/svg/core_bg.svg"
							alt="core_bg"
							class="bg-cover bg-center absolute h-full right-0"
						/>
						<div>
							<h2 class="text-center m-[30px]">
								{@html about_us_title}
							</h2>

							<h3 class="text-center text-[27px]">
								{@html about_us_subtitle}
							</h3>
						</div>
					</div>

					<div
						class="text-base text-white leading-[31px] font-montserrat text-center pl-4 pr-4 xl:mb-[160px] lg:mb-[90px] mb-[40px]"
					>
						{@html about_us_content}
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="bg-[color:var(--color-bg-dark)] flex">
		<!-- <a class="text-[color:var(--color-text)]" href="https://maps.app.goo.gl/fZhtSQQbJkm6LbXh6">Consulta nuestra ubicación</a> -->

		<div class="relative w-[100%] h-[450px] overflow-hidden">
			<div bind:this={mapDiv} class="w-full h-full"></div>
		</div>
	</div>
</div>
<!-- END -->
<div class="bg-[color:var(--color-bg-dark)]">
	<Services
		title={services_content_title}
		subtitle={services_content_subtitle}
		data={services_data}
	/>
	<Services
		title={rules_content_title}
		subtitle={rules_content_subtitle}
		data={rules_data}
	/>
	<div class="min-h-[64px]"></div>
</div>
<!-- HOME Reservation FormT -->
<div id="home_page_reservation_form">
	<ReservationForm
		title={form_title}
		subtitle={form_subtitle}
		img={form_img}
		content={form_content}
	/>
</div>
<!-- END -->
