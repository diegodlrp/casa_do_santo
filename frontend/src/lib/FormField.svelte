<script lang="ts">
    // Define the shape of an option object for clarity
    type SelectOption = {
        value: string;
        label: string;
    };

    export let id: string;
    export let label: string;
    export let value: string | boolean;
    export let errors: string[] | undefined = undefined;
    export let type = "text";
    export let required = false;
    export let optional = false;

    // ADD THIS LINE: Prop to receive the dropdown options
    export let options: SelectOption[] | undefined = undefined;
</script>

<div>
    {#if type === "checkbox"}
        <div class="flex items-center space-x-2 h-full">
            <input
                {id}
                type="checkbox" bind:checked={value}
                class="h-4 w-4 border-gray-300 rounded focus:ring-indigo-500"
            />
            <label for={id} class="block text-sm font-medium">{@html label}</label>
        </div>
    {:else if type === "textarea"}
        <label for={id} class="block text-sm font-medium mb-1">
            {@html label}
            {#if optional}
                <span class="text-gray-400">(Opcional)</span>
            {/if}
        </label>
        <textarea
            {id}
            {required}
            bind:value
            rows="4"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        ></textarea>
    
    {:else if type === "select"}
        <label for={id} class="block text-sm font-medium mb-1">
            {@html label}
            {#if optional}
                <span class="text-gray-400">(Opcional)</span>
            {/if}
        </label>
        <select
            {id}
            {required}
            bind:value
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
            <option value="" disabled selected>Seleccione una opción</option>
            
            {#if options}
                {#each options as option}
                    <option value={option.value}>{option.label}</option>
                {/each}
            {/if}
        </select>

    {:else} <label for={id} class="block text-sm font-medium mb-1">
            {@html label}
            {#if optional}
                <span class="text-gray-400">(Opcional)</span>
            {/if}
        </label>
        <input
            {id}
            type={type} {required}
            bind:value
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
    {/if}

    {#if errors}
        <p class="mt-1 text-sm text-red-600">{errors[0]}</p>
    {/if}
</div>