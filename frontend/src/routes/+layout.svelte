<script lang="ts">
	import LL, { setLocale } from '$i18n/i18n-svelte'
	import Header from '$lib/Header.svelte'
	import type { LayoutData } from './$types'

	import '../styles/global.css'

	export let data: LayoutData
	// at the very top, set the locale before you access the store and before the actual rendering takes place
	setLocale(data.locale)

</script>

<Header />

<main>
	<slot />
</main>

