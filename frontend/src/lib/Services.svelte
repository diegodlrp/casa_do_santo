<script lang="ts">
    export let title: string;
    export let subtitle: string;
    export let data: any[] = [];
</script>

<div class="text-[color:var(--color-text)]">
    <div class="pt-12">
        <h2 class="text-center m-[30px]">{@html title}</h2>
        <h3 class="text-center m-[27px]">{@html subtitle}</h3>
    </div>
    <div
        class="container w-full grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
    >
        <!-- cards -->
        {#each data as service}
            <div class="p-5 cursor-pointer rounded-md">
                <div class="flex flex-row items-center gap-5">
                    <img
                        class="inline h-10 w-10"
                        src={service.image}
                        alt={service.slug}
                    />
                    <p class="md:text-lg font-bold border-b-2 border-[color:var(--color-text-caption)]">
                        {service.title}
                    </p>
                </div>
                <p>
                    {service.content}
                </p>
            </div>
        {/each}
    </div>
</div>
