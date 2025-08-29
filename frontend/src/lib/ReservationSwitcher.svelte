<script lang="ts">
    import { base } from '$app/paths';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import LL, { locale } from '$i18n/i18n-svelte';

    let selectedUrl = 'reservation_form';
    
    function navigate() {
        const url = `${base}/${$locale}/${selectedUrl}`;
        goto(url);
    }
</script>

<div>
    <select
        class="nav-link"
        bind:value={selectedUrl}
        on:change={navigate}
    >   
        <option hidden selected value="reservation_form">{$LL.book()}</option>
        <option value="reservation_form">{$LL.book()}</option>
        <option value="rates">{$LL.rates()}</option>
    </select>
</div>