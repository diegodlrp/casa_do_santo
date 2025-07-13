<script lang="ts">
	import RiPhoneLine from "svelte-remixicon/RiPhoneLine.svelte";
	import RiMailLine from "svelte-remixicon/RiMailLine.svelte";
	import RiMapPin2Line from "svelte-remixicon/RiMapPin2Line.svelte";
	// import LL from '$i18n/i18n-svelte'
	import type { PageData } from "./$types";

	export let data: PageData;

	// Destructure the data directly
	const {
		title,
		img,
		address,
		email,
		phone,
		htitle,
		hsubtitle,
		hcontent,
		form_title,
		form_subtitle,
		form_img,
		error,
	} = data;
	console.log("data", data);
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
		<!-- <div class="start_info flex items-center gap-8 flex-row">
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
						href="tel:{phone}"
						class="tel_icon flex items-center gap-x-1 text-white"
					>
						<RiPhoneLine />
						{phone}
					</a>
					<a
						href="mailto:{email}"
						class="email_icon flex items-center gap-x-1 text-white"
					>
						<RiMailLine />
						{email}
					</a>
				</div>
			</div>
		</div> -->
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
<div id="home_page_content">home_page_content</div>
<!-- END -->
<div>about_us</div>
<!-- END -->
<div>reservation_form</div>
<!-- END -->
