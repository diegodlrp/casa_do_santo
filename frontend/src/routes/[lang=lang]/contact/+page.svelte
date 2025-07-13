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
aaa