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

    let handleDateEnd;

    let dateInit = "";
    let dateEnd = "";
    let dateLimit = "";
    let dateMin = "";
    let n_people = 1;
    let selectedDate = "";

    const handleSubmit = async () => {
        // Example: Simulate a successful submission after a delay
        await new Promise((resolve) => setTimeout(resolve, 500));
        goto(base + "/" + $locale + "/reservation_form?checkInDate="+checkInDate+"&checkOutDate="+checkOutDate);
    };

    function getFormattedDate(date: Date) {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, "0");
        const day = date.getDate().toString().padStart(2, "0");
        return `${year}-${month}-${day}`;
    }

    let checkInDate = "";
    let checkOutDate = "";

    onMount(async () => {
        const checkInInput = document.getElementById("check_in_date");
        const checkOutInput = document.getElementById("check_out_date");
        const titleResponse = await apiRequest(`/calendar/available-dates/`);
        console.log("titleResponse", titleResponse);
        if (checkInInput && checkOutInput) {
            flatpickr(checkInInput, {
                mode: "range",
                dateFormat: "Y-m-d", // Format for your Django backend
                minDate: "today", // Prevent picking past dates
                inline: true,
                altInput: true,
                disable: titleResponse, // Display user-friendly date in input
                altFormat: "F j, Y", // User-friendly format (e.g., July 31, 2025)
                onChange: function (selectedDates, dateStr, instance) {
                    if (selectedDates.length === 2) {
                        // This condition checks if both start and end are selected
                        checkInDate = instance.formatDate(
                            selectedDates[0],
                            "Y-m-d",
                        );
                        checkOutDate = instance.formatDate(
                            selectedDates[1],
                            "Y-m-d",
                        );
                    } else {
                        checkInDate =
                            selectedDates.length > 0
                                ? instance.formatDate(selectedDates[0], "Y-m-d")
                                : "";
                        checkOutDate = "";
                    }
                },
            });

            // const checkOutInstance = flatpickr(checkOutInput, {
            //     dateFormat: "Y-m-d",
            //     minDate: "today", // Initial min date
            //     inline: true,
            //     altInput: true,
            //     disable: titleResponse,
            //     altFormat: "F j, Y",
            //     onClose: function (selectedDates, dateStr, instance) {
            //         // When the check-out calendar is closed, update checkOutDate
            //         if (selectedDates.length > 0) {
            //             checkOutDate = dateStr;
            //         } else {
            //             checkOutDate = "";
            //         }
            //     },
            // });
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
                        <div class="flex flex-col items-center  w-[34%]">
                            <div>
                                
                            </div>
                            <div
                                id="inline-calendar-container"
                                class="date-picker-container"
                            >
                                <input
                                    type="text"
                                    id="check_in_date"
                                    placeholder="Select check-in date"
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
                                >
                                    {$LL.reservation_request()}
                                </button>
                            </div>
                        </div>
                        <p class=" w-[33%]">aqui vamos aponer el precio calculado</p>
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
