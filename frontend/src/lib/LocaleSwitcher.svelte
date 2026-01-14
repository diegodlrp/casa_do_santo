<script lang="ts">
    import { browser } from "$app/environment";
    import { invalidateAll, goto } from "$app/navigation"; // Import goto
    import { page } from "$app/stores";
    import { LL, setLocale, locale } from "$i18n/i18n-svelte";
    import type { Locales } from "$i18n/i18n-types";
    import { locales } from "$i18n/i18n-util";
    import { loadLocaleAsync } from "$i18n/i18n-util.async";
    import { replaceLocaleInUrl } from "../utils.js"; // Adjust path as needed

    // This function handles the actual locale switching logic
    // It's robust and already handles history state and invalidation.
    const switchLocale = async (
        newLocale: Locales,
        updateHistoryState = true,
    ) => {
        if (!newLocale || $locale === newLocale) return;

        // load new dictionary from server
        await loadLocaleAsync(newLocale);

        // select locale
        setLocale(newLocale);

        const newUrl = replaceLocaleInUrl($page.url, newLocale);

        if (updateHistoryState) {
            await goto(newUrl);
        } 
        invalidateAll();
        

        // update `lang` attribute on <html>
        if (browser) {
            document.querySelector("html")!.setAttribute("lang", newLocale);
        }
		selectedLocale = "" // This makes the title display again
    };

    // --- Language Switcher Logic (using <select>) ---
    // This variable will hold the currently selected locale in the <select>
	let selectedLocale: Locales | "" = $locale || "";

    // Reactively update selectedLocale when $locale changes (e.g., from initial load or popstate)
    $: selectedLocale = "";
	
    // This function is called when the <select> value changes
    const handleSelectChange = async (event: Event) => {
        const target = event.target as HTMLSelectElement;
        const newLocale = target.value as Locales;
        await switchLocale(newLocale, true); // Trigger full switch including navigation
    };

    // --- Browser History (PopState) Handling ---
    // This is for when the user clicks the browser's back/forward buttons
    const handlePopStateEvent = async ({ state }: PopStateEvent) => {
        if (state && state.locale) {
            // Don't update history state again here, as browser already handled it
            await switchLocale(state.locale as Locales, false);
        }
    };

    // --- Initial Load/Page Parameter Change Handling ---
    // This logic runs when the component mounts or when $page.params.lang changes
    $: if (browser && $page.params.lang && $page.params.lang !== $locale) {
        const langFromUrl = $page.params.lang as Locales;
        // Don't update history state here, as this is usually after a navigation or initial load
        switchLocale(langFromUrl, false);
        // Ensure history state also includes locale for future popstate events
        history.replaceState(
            { ...history.state, locale: langFromUrl },
            "",
            replaceLocaleInUrl($page.url, langFromUrl),
        );
    }
</script>

<svelte:window on:popstate={handlePopStateEvent} />

<div>
 
    <select
        class="nav-link"
        on:change={handleSelectChange}
        bind:value={selectedLocale}
    >
		<option hidden selected value="">{$LL.language()}</option>
        {#each locales as l}
            <option value={l}>
                {l.toUpperCase()} </option>
        {/each}
    </select>
</div>

