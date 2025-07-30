<script lang="ts">
    import { base } from "$app/paths";
    import { LL, locale } from "$i18n/i18n-svelte";
    import { goto } from "$app/navigation"; // Import the goto function

    export let title: string;
    export let subtitle: string;
    export let img: string;

    // Get today's date
    const today = new Date();

    let handleDateEnd;

    let dateInit = "";
    let dateEnd = "";
    let dateLimit = "";
    let dateMin = "";
    let n_people = 1;

    const handleSubmit = async () => {
        // Example: Simulate a successful submission after a delay
        await new Promise((resolve) => setTimeout(resolve, 500));

        goto(base + "/" + $locale + "/reservation_form");
    };

    function getFormattedDate(date: Date) {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, "0");
        const day = date.getDate().toString().padStart(2, "0");
        return `${year}-${month}-${day}`;
    }
</script>

<div class="relative overflow-hidden pt-0 mt-0">
    <div class="bg-cover bg-center" style="background-image: url({img});">
        <div class="w-full h-full bg-[color:var(--color-bg-light)]/80">
            <div class="h-16"></div>
            <div class="container form_bg pt-4 pb-4">
                <img
                src="/svg/core_bg.svg"
                alt="core_bg"
                class="bg-cover bg-center absolute h-full bottom-0 right-[30vh]"
            />
                <form
                    on:submit|preventDefault={handleSubmit}
                    class="reservation_form text-[color:var(--color-text)]"
                >
                    <h2>
                        {@html title}
                    </h2>
                    <p class="pl-5">
                        {@html subtitle}
                    </p>
                    <div
                        class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-4 items-end"
                    >
                        <div>
                            <label for="dateInit" class="text-sm"
                                >{$LL.arrival_date()}:</label
                            >
                            <input
                                bind:value={dateInit}
                                min={getFormattedDate(today)}
                                on:input={handleDateEnd}
                                type="date"
                                class="text-black ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none focus:ring-2 focus:ring-[#deb860]"
                            />
                        </div>
                        <div>
                            <label for="dateEnd" class="text-sm"
                                >{$LL.departure_date()}:</label
                            >
                            <input
                                bind:value={dateEnd}
                                min={dateMin}
                                max={dateLimit}
                                type="date"
                                placeholder="your name"
                                class="text-black ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none focus:ring-2 focus:ring-[#deb860]"
                            />
                        </div>
                        <div>
                            <label for="n_people" class="text-sm"
                                >{$LL.n_guest()}:</label
                            >
                            <input
                                bind:value={n_people}
                                type="number"
                                min="1"
                                max="6"
                                placeholder="your name"
                                class="text-black ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none focus:ring-2 focus:ring-[#deb860]"
                            />
                        </div>
                        <div>
                            <button
                                class="core_button w-full h-full min-h-[42px] mt-6 md:mt-0 font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform"
                            >
                            {$LL.check_availability()}
                            </button>
                        </div>
                    </div>
                </form>
            </div>
            <div class="h-16"></div>
        </div>
    </div>
</div>
