<script lang="ts">
    import { base } from "$app/paths";
    import { LL, locale } from "$i18n/i18n-svelte";
    import { goto } from "$app/navigation"; // Import the goto function

    import { onMount } from "svelte";
    import flatpickr from "flatpickr";
    import "flatpickr/dist/flatpickr.min.css"; // Import the CSS
    import { apiRequest } from "./services/apiService";

    export let title: string;
    export let subtitle: string;
    export let img: string;
    export let content: string;

    // Get today's date
    const today = new Date();

    let isButtonDisabled = true;

    const handleSubmit = async () => {
        // Example: Simulate a successful submission after a delay
        await new Promise((resolve) => setTimeout(resolve, 500));
        goto(
            base +
                "/" +
                $locale +
                "/reservation_form?checkInDate=" +
                checkInDate +
                "&checkOutDate=" +
                checkOutDate,
        );
    };

    let checkInDate = "";
    let checkOutDate = "";
    let n_days = 0;
    let base_price = 0;
    let total_price = 0;

    let percentage_true: any[] = [];
    let percentage_false: any[] = [];

    let fix_discount = 0;
    let fix_discount_days = 0;
    let variant_discount = 0;
    let variant_discount_days = 0;

    onMount(async () => {
        const checkInInput = document.getElementById("check_in_date");
        const checkOutInput = document.getElementById("check_out_date");
        const titleResponse = await apiRequest(`/calendar/available-dates/`);
        console.log("titleResponse", titleResponse);
        const discountResponse = await apiRequest(`/discount/?lang=${locale}`);
        console.log("discountResponse", discountResponse);
        percentage_true = discountResponse["percentage_true"];
        percentage_false = discountResponse["percentage_false"];
        if (checkInInput && checkOutInput) {
            flatpickr(checkInInput, {
    mode: "range",
    dateFormat: "Y-m-d", // Format for your Django backend
    minDate: "today", // Prevent picking past dates
    inline: true,
    // altInput: true,
    // disable: titleResponse, // Display user-friendly date in input
    altFormat: "F j, Y", // User-friendly format (e.g., July 31, 2025)
    onChange: function (selectedDates, dateStr, instance) {
        if (selectedDates.length === 2) {
            // This condition checks if both start and end are selected
            console.log("selectedDates", selectedDates);
            checkInDate = instance.formatDate(
                selectedDates[0],
                "Y-m-d",
            );
            checkOutDate = instance.formatDate(
                selectedDates[1],
                "Y-m-d",
            );
            let differenceInTime =
                selectedDates[1].getTime() -
                selectedDates[0].getTime();
            n_days = differenceInTime / (1000 * 3600 * 24);

            if (n_days >= 3) {
                isButtonDisabled = false;
                base_price = 233 * n_days;
                variant_discount_days = 0;

                percentage_true.forEach((item) => {
                    console.log("item", item);
                    if (
                        n_days >= item.days_number &&
                        item.days_number > variant_discount_days
                    ) {
                        variant_discount_days = item.days_number;
                        variant_discount = item.discount;
                    }
                    console.log(percentage_true);
                });
                fix_discount_days = 0;
                percentage_false.forEach((item) => {
                    if (
                        n_days >= item.days_number &&
                        item.days_number > fix_discount_days
                    ) {
                        fix_discount_days = item.days_number;
                        fix_discount = item.discount;
                    }
                    console.log(percentage_true);
                });

                total_price = base_price - fix_discount;
                total_price =
                    (total_price * (100 - variant_discount)) / 100;
            } else {
                alert($LL.nights_warrning());
                isButtonDisabled = true;
            }

            console.info("checkOutDate", checkOutDate);
        } else {
            isButtonDisabled = true;
            checkInDate =
                selectedDates.length > 0
                    ? instance.formatDate(selectedDates[0], "Y-m-d")
                    : "";
            checkOutDate = "";
            n_days = 0;
            base_price = 0;
            total_price = 0;
            fix_discount = 0;
            variant_discount = 0;
            variant_discount_days = 0;
            fix_discount_days = 0;
        }

        // --- ADD THIS LINE ---
        // This clears the input field after the dates are selected and processed.
        instance.input.value = "";
    },
});
        }
    });
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
                    <div class="flex flex-row">
                        <p class="pl-5 w-[33%]">
                            {@html content}
                        </p>
                        <div class="flex flex-col items-center w-[34%]">
                            <div></div>
                            <div
                                id="inline-calendar-container"
                                class="date-picker-container"
                            >
                                <input
                                    type="text"
                                    id="check_in_date"
                                    placeholder=""
                                />

                                <!-- <label for="check_out_date">Check-out Date:</label> -->
                                <input
                                    type="text"
                                    id="check_out_date"
                                    placeholder="Select check-out date"
                                    class="hidden"
                                />
                            </div>
                            <div class="mt-[30px]">
                                <button
                                    class="core_button w-full h-full min-h-[42px] mt-6 md:mt-0 font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform"
                                    class:button_dissabled={isButtonDisabled ===
                                        true}
                                    disabled={isButtonDisabled}
                                >
                                    {$LL.reservation_request()}
                                </button>
                            </div>
                        </div>
                        <div class="w-[33%] h-[100%]">
                            <div
                                class="font-bold uppercase text-[color:var(--color-text-caption)]"
                            >
                                <table class="w-80% h-[100%]">
                                    <tbody>
                                        <tr>
                                            <td>{$LL.n_nights()}:</td>
                                            <td class="text-right">{n_days}</td>
                                        </tr>
                                        <tr>
                                            <td>{$LL.price()}:</td>
                                            <td class="text-right"
                                                >{base_price} €</td
                                            >
                                        </tr>
                                        <tr>
                                            <td class="text-top"
                                                >{$LL.discounts()}:</td
                                            >
                                            <td class="text-right"
                                                >{#if fix_discount > 0}{fix_discount_days}
                                                    {$LL.nights()}
                                                    {fix_discount} €<br />{/if}
                                                {#if variant_discount > 0}{variant_discount_days}
                                                    {$LL.nights()}
                                                    {variant_discount}%<br
                                                    />{/if}</td
                                            >
                                        </tr>
                                        <tr
                                            class="mt-14 mb-5 border-b border-[color:var(--color-text-caption)] relative"
                                        ></tr>
                                        <tr>
                                            <td class="text-top"
                                                >{$LL.final_price()}:</td
                                            >
                                            <td class="text-right"
                                                >{total_price} €</td
                                            >
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            <div class="h-16"></div>
        </div>
    </div>
</div>

<style>
    /* Your other component-specific styles here */

    /* Custom styles for disabled dates - using :global() for Flatpickr elements */
    :global(.flatpickr-day.flatpickr-disabled),
    :global(.flatpickr-day.flatpickr-disabled:hover),
    :global(.flatpickr-day.flatpickr-disabled.inRange) {
        background-color: #ffcccc !important; /* A light red for unavailable */
        color: #660000 !important; /* Darker red text */
        cursor: not-allowed; /* Indicate it's not clickable */
        opacity: 0.7; /* Make it slightly transparent */
        /* It's often necessary to explicitly override Flatpickr's default border/box-shadow */
        border: none !important;
        box-shadow: none !important;
    }

    /* Styles for disabled dates that might also be selected (e.g., if a range includes disabled days) */
    :global(.flatpickr-day.flatpickr-disabled.selected) {
        background-color: #ff9999 !important; /* Slightly darker red */
        color: white !important;
    }

    /* Optional: If you have dates that are 'out of month' but also disabled */
    :global(.flatpickr-day.next-month.flatpickr-disabled),
    :global(.flatpickr-day.prev-month.flatpickr-disabled) {
        color: rgba(
            102,
            0,
            0,
            0.5
        ) !important; /* Faded red for disabled days in adjacent months */
    }

    /* Ensure the calendar container itself has a background if needed */
    :global(.flatpickr-calendar) {
        background-color: #fff; /* Ensure white background for calendar */
    }

    /* Your existing .calendar-wrapper, .date-display-inputs, etc. styles */
</style>
