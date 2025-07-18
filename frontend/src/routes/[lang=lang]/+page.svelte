<script lang="ts">
	import RiPhoneLine from "svelte-remixicon/RiPhoneLine.svelte";
	import RiMailLine from "svelte-remixicon/RiMailLine.svelte";
	import RiMapPin2Line from "svelte-remixicon/RiMapPin2Line.svelte";
	import type { PageData } from "./$types";
    import ReservationForm from "$lib/ReservationForm.svelte";

	export let data: PageData;

	// Destructure the data directly
	const {
		title,
		img,
		address,
		email,
		phone,
		page_content_title,
		page_content_subtitle,
		page_content,
		about_us_title,
        about_us_subtitle,
        about_us_content,
        about_us_img,
		form_title,
		form_subtitle,
		form_img,
		error,
	} = data;

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
<div id="home_page_content" class="pt-[36px] pb-[100px] relative w-full">

		<div class=" min-h-[64px]"></div>
		<div>
			<div>
                <div>
                    <h1>{@html page_content_title}</h1><br>
                </div>
				
                <div>
                    <h2 >{@html page_content_subtitle}</h2><br>
                    <h4>{@html page_content}</h4>
                </div>
				
			</div>

			<!-- <ServicesComponent /> -->
		</div>
		<!-- <img
			src="/svg/main_bg_gray.svg"
			alt="background_room_core_left"
			class="absolute top-0 left-0 img_2 z-0 main_img rotate-180"
		/>

		<img
			src="/svg/main_bg_gray.svg"
			alt="background_room_core_right"
			class="absolute top-0 right-0 img_2 img_flip z-0 main_img rotate-180"
		/> -->

</div>
<!-- END -->

<!-- HOME About Us -->
<div id="home_page_about_us">
	<div>
		<div>
			<div>
				<img src={about_us_img} alt="about_us" class="w-full" />
			</div>

			<div>









				<div>
					<div>
						<div
						
						>
							<h1>
								{@html about_us_title}
							</h1>
							
								<h4
									
								>
									{@html about_us_subtitle}
								</h4>
							
						</div>
					</div>
	
					<div
						
					>
						<div >
							<p >
								{@html about_us_content}
							</p>
						</div>
					</div>
				</div>












			</div>
		</div>
	</div>
</div>
<!-- END -->

<!-- HOME Reservation FormT -->
<div id="home_page_reservation_form">
	<ReservationForm title={form_title} subtitle={form_subtitle} img={form_img}/>
</div>
<!-- END -->
