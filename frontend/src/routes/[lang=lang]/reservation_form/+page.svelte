<script lang="ts">
    import { LL } from "$i18n/i18n-svelte";
    import RiPhoneLine from "svelte-remixicon/RiPhoneLine.svelte";
    import RiMailLine from "svelte-remixicon/RiMailLine.svelte";
    import RiMapPin2Line from "svelte-remixicon/RiMapPin2Line.svelte";
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";
    import { onMount } from "svelte";

    export let data: PageData;

    // Destructure the data directly
    const { title_img, contact_img, form_img, error } = data;

    $: title_title = data.title_title;
    $: title_subtitle = data.title_subtitle;
    $: contact_title = data.contact_title;
    $: contact_content = data.contact_content;
    $: contact_phones = data.contact_phones;
    $: contact_email = data.contact_email;
    $: contact_address = data.contact_address;
    $: contact_address_link = data.contact_address_link;
    $: form_title = data.form_title;
    $: form_subtitle = data.form_subtitle;
    $: locale = data.locale;

    let name = "";
    let email = "";
    let message = "";
    let checkInDate = "";
    let checkOutDate = "";
    let n_adults = 1;
    let n_childs = 0;

    const maxGuests = 6;
    $: totalGuests = n_adults + n_childs;
    $: totalGuestsError =
        totalGuests > maxGuests
            ? `El número total de huéspedes (adultos + niños) no puede ser mayor de ${maxGuests}.`
            : null;


    let errors: { [key: string]: string[] | { [key: string]: string[] }[] } =
        {}; // Adjust type for nested errors
    let successMessage: string = "";
    let isLoading: boolean = false;

    const handleSubmit = async () => {
        successMessage = "";

        // VALIDATE
        if (totalGuestsError) {
            errors = { general: [totalGuestsError] };
            return; // Stop the form submission
        }

        isLoading = true;
        try {
            const response = await fetch(
            "https://casadosantoadmin.casacam.net/api-reservation/create-reservation/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",

                        // Add CSRF token header if needed (see previous email example notes)
                    },
                    mode: "cors",
                    // Send petition data as JSON
                    body: JSON.stringify({
                        name: name,
                        mail: email,
                        message: message,
                        checkInDate: checkInDate,
                        checkOutDate: checkOutDate,
                        n_adults: n_adults,
                        n_childs: n_childs,
                        language: locale,
                    }),
                    credentials: "omit",
                },
            );

            if (!response.ok) {
                const errorData = await response.json();
                errors = errorData;
                if (response.status === 409 && errorData.detail) {
                    errors.general = [errorData.detail];
                } else if (errorData.non_field_errors) {
                    errors.general = errorData.non_field_errors;
                } else {
                    errors.general = [
                        "Ocurrió un error inesperado al procesar la reserva. Por favor, inténtalo de nuevo.",
                    ];
                }
                console.error("API Error:", errorData);
            } else {
                const result = await response.json();
                successMessage = "¡Solicitud de reserva realizada con éxito!";
                console.log("Reservation successful:", result);
                errors = {};

                // ---------------------------------------------------
                // ✨ ADD THIS SECTION TO CLEAR THE FORM VALUES ✨
                // ---------------------------------------------------
                name = "";
                email = "";
                message = "";
                checkInDate = "";
                checkOutDate = "";
                n_adults = 1; 
                n_childs = 0;
            }
        } catch (error) {
            console.error("Network or other error:", error);
            errors.general = [
                "No se pudo conectar con el servidor. Por favor, revisa tu conexión a internet.",
            ];
        } finally {
            isLoading = false;
        }
    };

    onMount(() => {
        // Check if window is defined to ensure this code only runs in the browser
        if (typeof window !== "undefined") {
            const urlParams = new URLSearchParams(window.location.search);
            checkInDate = urlParams.get("checkInDate");
            checkOutDate = urlParams.get("checkOutDate");

            console.log("Value of myParam is:", checkInDate);
            console.log("Value of myParam is:", checkOutDate);
        }
    });
</script>

<Title title={title_title} subtitle={title_subtitle} img={title_img} />
<div class="min-h-[calc(100vh-264px)] sm:min-h-[calc(100vh-280px)]">
    <div
        id="contact_form"
        class="bg-cover bg-center items-center"
        style="background-image: url({contact_img});"
    >
        <div
            class="relative pt-[36px] pb-[100px] min-h-[80vh] overflow-hidden w-full h-full bg-[color:var(--color-bg-light)]/80"
        >
            <div class="p-4 relative z-10 rounded-4xl">
                <div class="container form_bg">
                    {#if successMessage}
                        <div
                            role="alert"
                            class="bg-green-100 border-l-4 border-green-500 text-green-700 p-8 mb-4 text-center"
                        >
                            <p>{successMessage.toUpperCase()}</p>
                        </div>
                    {/if}

                    {#if errors.general}
                        <div
                            role="alert"
                            class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4"
                        >
                            {#each errors.general as error}
                                <p>{error}</p>
                            {/each}
                        </div>
                    {/if}

                    <div
                        class="flex w-full justify-center items-center flex-row"
                    >
                        <!-- start -->
                        <div class="flex-col justify-between p4 w-[55%]">
                            <div class="pb-4">
                                <h2>
                                    {@html contact_title}
                                </h2>
                                <p class="pr-4 text-[color:var(--color-text)]">
                                    {@html contact_content}
                                </p>
                            </div>

                            <div class="text-[color:var(--color-text)]">
                                {#each contact_phones as phone}
                                    <div
                                        class="flex felx-row items-center space-x-2"
                                    >
                                        <RiPhoneLine />
                                        <a href="tel:{phone.number}"
                                            >{phone.number}</a
                                        >
                                    </div>
                                {/each}
                                <div
                                    class="flex felx-row items-center space-x-2"
                                >
                                    <RiMailLine />
                                    <a href="mailto:{contact_email}"
                                        >{contact_email}</a
                                    >
                                </div>
                                <div
                                    class="flex felx-row items-center space-x-2"
                                >
                                    <RiMapPin2Line />
                                    <a href={contact_address_link}
                                        >{contact_address}</a
                                    >
                                </div>
                            </div>
                        </div>
                        <!-- end -->
                        <!-- start -->
                        <div class="w-[55%]">
                            <form
                                onsubmit={handleSubmit}
                                class="flex flex-col space-y-4 w-[80%] text-[color:var(--color-text)]"
                            >
                                <!-- START name -->
                                <div>
                                    <label for="name" class="text-sm"
                                        >{$LL.name()}</label
                                    >
                                </div>
                                <div>
                                    <input
                                        bind:value={name}
                                        type="text"
                                        placeholder={$LL.your_name()}
                                        class="text-[color:var(--color-text)] ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none"
                                        required
                                    />
                                </div>
                                <!-- END name -->
                                <!-- START email -->
                                <div>
                                    <label for="email" class="text-sm"
                                        >{$LL.mail()}:</label
                                    >
                                </div>
                                <div>
                                    <input
                                        bind:value={email}
                                        type="email"
                                        placeholder={$LL.your_email()}
                                        class="text-[color:var(--color-text)] ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none"
                                        required
                                    />
                                </div>
                                <!-- END email -->

                                <div>
                                    <label
                                        for="check_in_date"
                                        class="block text-sm font-medium mb-1"
                                        >Fecha de Entrada</label
                                    >
                                    <input
                                        type="date"
                                        id="check_in_date"
                                        bind:value={checkInDate}
                                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                        required
                                        disabled
                                    />
                                </div>

                                <div>
                                    <label
                                        for="check_in_date"
                                        class="block text-sm font-medium mb-1"
                                        >Fecha de Entrada</label
                                    >
                                    <input
                                        type="date"
                                        id="check_in_date"
                                        bind:value={checkOutDate}
                                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                        required
                                        disabled
                                    />
                                </div>
                                <!-- START N Guest -->
                                <div>
                                    <label
                                        for="n_adults"
                                        class="block text-sm font-medium mb-1"
                                        >Nº de adultos</label
                                    >
                                    <input
                                        type="number"
                                        id="n_adults"
                                        bind:value={n_adults}
                                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                        required
                                        min="1"
                                        max="6"
                                    />
                                </div>
                                <div>
                                    <label
                                        for="n_childs"
                                        class="block text-sm font-medium mb-1"
                                        >Nº de niños</label
                                    >
                                    <input
                                        type="number"
                                        id="n_childs"
                                        bind:value={n_childs}
                                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                        required
                                        max="5"
                                    />
                                </div>
                                <!-- START message -->
                                <div>
                                    <label for="message" class="text-sm"
                                        >{$LL.message()}</label
                                    >
                                </div>
                                <div>
                                    <textarea
                                        bind:value={message}
                                        placeholder={$LL.write_your_message()}
                                        rows="4"
                                        class="text-[color:var(--color-text)] ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none"
                                        required
                                    ></textarea>
                                </div>
                                <!-- END message -->
                                <!-- START checkbox -->
                                <!-- <div class="flex items-center">
                                    <input
                                        id="checked-checkbox"
                                        type="checkbox"
                                        value=""
                                        class="w-4 h-4"
                                        required
                                    />
                                    <label
                                        for="checked-checkbox"
                                        class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                                        >{"accept"}
                                        <a
                                            href="/privacy"
                                            class="text-[#c8a655]"
                                            >{"privacy_politic"}</a
                                        > 
                                    </label>
                                </div>-->
                                <!-- END checkbox -->
                                <!-- START button -->
                                <button
                                    class="core_button font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform mt-[30px]"
                                    disabled={isLoading}
                                >
                                    {#if isLoading}
                                        Enviando...
                                    {:else}
                                        {$LL.send_message()}{/if}
                                </button>
                                <!-- END button -->
                            </form>
                        </div>
                        <!-- end -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
