<script lang="ts">
    export let title: string;
    export let subtitle: string;
    export let img: string;
</script>

<div class="relative overflow-hidden z-900">
    <div
        class="inset-0 bg-cover bg-center relative overflow-hidden w-[100%] h-[200px] text-gray-200"
        style="background-image: url({img});"
    >
        <div class="absolute w-full h-full bg-[color:var(--color-bg-dark)]/80">
            <h2 class="text-center">{@html title}</h2>
            <h3 class="text-center">{@html subtitle}</h3>
        </div>
    </div>
</div>
