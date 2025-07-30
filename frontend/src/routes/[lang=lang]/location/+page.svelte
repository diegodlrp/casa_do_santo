<script lang="ts">
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";

    export let data: PageData;

    // Destructure the data directly
    const {
		title,
        subtitle,
		img,
		error,
	} = data;

</script>
<Title title={title} subtitle={subtitle} img={img}/>
<div
            class="relative w-[100%] min-h-[calc(100vh-20px)] sm:h-[calc(100vh-36px)] overflow-hidden"
        >
</div>