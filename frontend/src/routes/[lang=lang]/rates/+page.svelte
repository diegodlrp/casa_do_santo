<script lang="ts">
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";

    export let data: PageData;

    // Destructure the data directly
    $: title_title = data.title_title;
    $: title_subtitle = data.title_subtitle;
    $: title_img = data.title_img;
    $: percentage_true = data.percentage_true;
    $: percentage_false = data.percentage_false;
    $: rate_data = data.rate_data;
    $: error = data.error;
</script>

<Title title={title_title} subtitle={title_subtitle} img={title_img} />
<div
    class="relative w-[100%] min-h-[calc(100vh-20px)] overflow-hidden"
>
    {#if rate_data.length > 0}
        <div class="min-h-[24px]"></div>
        <div
            class="max-w-3xl mx-auto p-6 bg-[color:var(--color-bg-dark)]/90 shadow-lg rounded-lg bg-cover bg-center"
            style="background-image: url('/svg/core_bg.svg'); opacity: 1;"
        >
            <h2 class="text-3xl font-bold text-center mb-6">
                Tarifas
            </h2>
            <table
                class="min-w-full divide-y divide-[color:var(--color-text-caption)] shadow-sm rounded-lg"
            >
                <thead class="text-[color:var(--color-text)]">
                    <tr>
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                            >Fecha inicio</th
                        >
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                            >Fecha fin</th
                        >
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                            >precio</th
                        >
                    </tr>
                </thead>
                <tbody
                    class="divide-y divide-[color:var(--color-text-caption)] text-[color:var(--color-text)]"
                >
                    {#each rate_data as rate}
                        <tr>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                                >{rate.start_date}</td
                            >
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">{rate.end_date}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">{rate.price}€</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}

    {#if percentage_true.length > 0}
        <div class="min-h-[24px]"></div>
        <div
            class="max-w-3xl mx-auto p-6 bg-[color:var(--color-bg-dark)]/90 shadow-lg rounded-lg bg-cover bg-center"
            style="background-image: url('/svg/core_bg.svg'); opacity: 1;"
        >
            <h2 class="text-3xl font-bold text-center mb-6">
                Descuento en porcentage
            </h2>
            <table
                class="min-w-full divide-y divide-[color:var(--color-text-caption)] shadow-sm rounded-lg"
            >
                <thead class="text-[color:var(--color-text)]">
                    <tr>
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                            >Nº Dias</th
                        >
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                            >Descuento</th
                        >
                    </tr>
                </thead>
                <tbody
                    class="divide-y divide-[color:var(--color-text-caption)] text-[color:var(--color-text)]"
                >
                    {#each percentage_true as discount}
                        <tr>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                                >{discount.days_number}</td
                            >
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">{discount.discount}%</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}

    {#if percentage_false.length > 0}
        <div class="min-h-[24px]"></div>
        <div
            class="max-w-3xl mx-auto p-6 bg-[color:var(--color-bg-dark)]/90 shadow-lg rounded-lg bg-cover bg-center"
            style="background-image: url('/svg/core_bg.svg'); opacity: 1;"
        >
            <h2 class="text-3xl font-bold text-center mb-6">Descuento Fijo</h2>
            <table
                class="min-w-full divide-y divide-[color:var(--color-text-caption)] shadow-sm rounded-lg"
            >
                <thead class="text-[color:var(--color-text)]">
                    <tr>
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                            >Nº Dias</th
                        >
                        <th
                            scope="col"
                            class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                            >Descuento</th
                        >
                    </tr>
                </thead>
                <tbody
                    class="divide-y divide-[color:var(--color-text-caption)] text-[color:var(--color-text)]"
                >
                    {#each percentage_false as discount}
                        <tr>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                                >{discount.days_number}</td
                            >
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">{discount.discount}€</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
    <div class="min-h-[24px]"></div>
</div>
