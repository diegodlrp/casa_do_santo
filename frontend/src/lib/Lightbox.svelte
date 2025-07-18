<script lang="ts">
	import { createEventDispatcher, onMount, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';

	let { images, current_index } = $props<{
		images: { alt: string; src: string }[];
		current_index: number;
	}>();

	const dispatch = createEventDispatcher();

	let current_image = $derived(images[current_index]);

	function close() {
		dispatch('close');
	}

	function next() {
		current_index = (current_index + 1) % images.length;
	}

	function prev() {
		current_index = (current_index - 1 + images.length) % images.length;
	}

	// Keyboard navigation
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') close();
		if (event.key === 'ArrowRight') next();
		if (event.key === 'ArrowLeft') prev();
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);
	});

	onDestroy(() => {
		window.removeEventListener('keydown', handleKeydown);
	});
</script>

<svelte:window on:keydown={handleKeydown} />

<div
	class="mt-16 fixed inset-0 bg-[#40392Fe0] z-[950] text-white flex items-center justify-center"
	transition:fade={{ duration: 300 }}
	role="dialog"
	aria-modal="true"
	tabindex="-1"
>
	<button
		class="absolute top-4 right-4 text-white text-5xl font-bold z-50 hover:text-[#c8a655]"
		aria-label="Close"
		onclick={close}>&times;</button
	>

	<div class="relative w-full h-full flex items-center justify-center">
		<button
			class="absolute left-4 top-1/2 -translate-y-1/2 text-white hover:text-[#c8a655] bg-[#40392Fe0] bg-opacity-40 rounded-full p-2 text-4xl hover:bg-opacity-70 transition-all z-50"
			aria-label="Previous image"
			onclick={prev}>&#10094;</button
		>

		<div class="relative max-w-[90vw] max-h-[85vh] flex flex-col items-center">
			{#key current_image.src}
				<img
					src={current_image.src}
					alt={current_image.alt}
					class="block max-w-full max-h-full object-contain rounded-lg shadow-2xl"
					in:fade={{ duration: 200, delay: 100 }}
				/>
			{/key}
			<!-- <p class="text-white text-center mt-4 text-lg font-light tracking-wide">
				{current_image.alt}
			</p> -->
		</div>

		<button
			class="absolute right-4 top-1/2 -translate-y-1/2 text-white hover:text-[#c8a655] bg-[#40392Fe0] bg-opacity-40 rounded-full p-2 text-4xl hover:bg-opacity-70 transition-all z-50"
			aria-label="Next image"
			onclick={next}>&#10095;</button
		>
	</div>
</div>
