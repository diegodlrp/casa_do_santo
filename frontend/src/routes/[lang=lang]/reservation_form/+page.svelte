<script lang="ts">
  import { invalidateAll } from "$app/navigation";
  import { page } from "$app/stores";
  import { onMount } from "svelte";

  // Define a type for an individual guest
  interface Guest {
    name: string;
    last_name: string;
    vat: string;
    adult: boolean;
  }

  // Define a type for the main form data
  interface FormData {
    guest_first_name: string; // Keep for the primary guest (or make primary guest part of guests array)
    guest_last_name: string;
    guest_email: string;
    guest_phone: string;
    guest_vat: string;
    guest_adult: boolean;
    check_in_date: string;
    check_out_date: string;
    special_requests: string;
    // New: Array to hold additional guests
    additional_guests: Guest[];
  }

  // Initial form data
  let formData: FormData = {
    guest_first_name: "",
    guest_last_name: "",
    guest_email: "",
    guest_phone: "",
    guest_vat: "",
    guest_adult: true,
    check_in_date: "",
    check_out_date: "",
    special_requests: "",
    additional_guests: [], // Start with no additional guests
  };

  let errors: { [key: string]: string[] | { [key: string]: string[] }[] } = {}; // Adjust type for nested errors
  let successMessage: string = "";
  let isLoading: boolean = false;

  // Set minimum date for check-in to today
  let today: string;
  onMount(() => {
    const d = new Date();
    const year = d.getFullYear();
    const month = (d.getMonth() + 1).toString().padStart(2, "0");
    const day = d.getDate().toString().padStart(2, "0");
    today = `${year}-${month}-${day}`;
    // formData.check_in_date = $page.url.searchParams.get('check_in');
    // formData.check_out_date = $page.url.searchParams.get('check_out');
    if (
      !formData.check_in_date ||
      new Date(formData.check_in_date) < new Date(today)
    ) {
      formData.check_in_date = today;
    }
    updateMinCheckoutDate();
  });

  function updateMinCheckoutDate() {
    if (formData.check_in_date) {
      const checkIn = new Date(formData.check_in_date);
      checkIn.setDate(checkIn.getDate() + 1);
      const year = checkIn.getFullYear();
      const month = (checkIn.getMonth() + 1).toString().padStart(2, "0");
      const day = checkIn.getDate().toString().padStart(2, "0");
      const minCheckout = `${year}-${month}-${day}`;

      if (
        !formData.check_out_date ||
        new Date(formData.check_out_date) < new Date(minCheckout)
      ) {
        formData.check_out_date = minCheckout;
      }
    }
  }

  // Function to add a new empty guest field
  function addGuest() {
    formData.additional_guests = [
      ...formData.additional_guests,
      { name: "", last_name: "", vat: "", adult: false },
    ];
    // Clear any previous general errors related to guest count if they were there
    if (
      errors.general &&
      errors.general.includes(
        "Debe haber al menos un huésped principal y un huésped por cada formulario adicional.",
      )
    ) {
      delete errors.general;
    }
  }

  // Function to remove a guest field
  function removeGuest(index: number) {
    formData.additional_guests = formData.additional_guests.filter(
      (_, i) => i !== index,
    );
  }

  // --- Validation ---
  function validateGuest(
    guest: Guest,
    index: number,
  ): { [key: string]: string[] } {
    const guestErrors: { [key: string]: string[] } = {};
    if (!guest.name.trim()) {
      guestErrors.first_name = ["El nombre es requerido."];
    }
    if (!guest.last_name.trim()) {
      guestErrors.last_name = ["El apellido es requerido."];
    }
    if (!guest.vat.trim()) {
      guestErrors.last_name = ["El DNI es requerido."];
    }
    return guestErrors;
  }

  function validateForm(): boolean {
    errors = {}; // Clear previous errors
    let isValid = true;

    // Validate Primary Guest
    if (!formData.guest_first_name.trim()) {
      errors.guest_first_name = ["El nombre es requerido."];
      isValid = false;
    }
    if (!formData.guest_last_name.trim()) {
      errors.guest_last_name = ["El apellido es requerido."];
      isValid = false;
    }
    if (
      !formData.guest_email.trim() ||
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.guest_email)
    ) {
      errors.guest_email = ["Por favor, introduce un email válido."];
      isValid = false;
    }

    // Validate Dates
    if (!formData.check_in_date) {
      errors.check_in_date = ["La fecha de entrada es requerida."];
      isValid = false;
    }
    if (!formData.check_out_date) {
      errors.check_out_date = ["La fecha de salida es requerida."];
      isValid = false;
    }
    if (formData.check_in_date && formData.check_out_date) {
      const checkIn = new Date(formData.check_in_date);
      const checkOut = new Date(formData.check_out_date);
      if (checkOut <= checkIn) {
        errors.check_out_date = [
          "La fecha de salida debe ser posterior a la de entrada.",
        ];
        isValid = false;
      }
    }

    // Validate Additional Guests
    const additionalGuestErrors: { [key: string]: string[] }[] = [];
    formData.additional_guests.forEach((guest, index) => {
      const guestErrors = validateGuest(guest, index);
      if (Object.keys(guestErrors).length > 0) {
        additionalGuestErrors[index] = guestErrors;
        isValid = false;
      }
    });
    if (additionalGuestErrors.length > 0) {
      errors.additional_guests = additionalGuestErrors;
    }

    // Ensure total adults match expected if you were to count additional guests as adults
    // You might need to adjust num_adults calculation based on how many "adults" the form represents in total.
    // For now, assuming num_adults is for the total count, and additional_guests are just more people.
    let totalGuests = 1; // Primary guest
    totalGuests += formData.additional_guests.length; // Add number of additional guests

    // If you want to enforce num_adults to be at least (1 + number of additional_guests)

    return isValid;
  }

  async function handleSubmit() {
    successMessage = "";
    if (!validateForm()) {
      return;
    }

    isLoading = true;
    try {
      // Prepare data for API: Combine primary guest and additional guests
      const reservationData = {
        ...formData,
        // Create an array of all guests for the backend
        guests_details: [
          // {
          //   first_name: formData.guest_first_name,
          //   last_name: formData.guest_last_name,
          //   email: formData.guest_email,
          //   phone: formData.guest_phone,
          //   vat: formData.guest_vat
          // },
          ...formData.additional_guests.map((guest) => ({
            first_name: guest.name,
            last_name: guest.last_name,
            vat: guest.vat,
            adult: guest.adult,
            email: "",
            phone: "",
          })),
        ],
        // Remove individual guest fields if your backend expects only the 'guests_details' array
        // guest_first_name: undefined,
        // guest_last_name: undefined,
        // guest_email: undefined,
        // guest_phone: undefined,
      };

      const response = await fetch("http://127.0.0.1:8000/reservations/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "", // Ensure CSRF token is sent
        },
        body: JSON.stringify(reservationData),
      });

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
        successMessage = "¡Reserva realizada con éxito!";
        console.log("Reservation successful:", result);
        // Reset form
        formData = {
          guest_first_name: "",
          guest_last_name: "",
          guest_email: "",
          guest_phone: "",
          check_in_date: today,
          check_out_date: new Date(
            new Date(today).setDate(new Date(today).getDate() + 1),
          )
            .toISOString()
            .split("T")[0],
          special_requests: "",
          additional_guests: [],
        };
        errors = {};
        // invalidateAll(); // Uncomment if you need to invalidate SvelteKit load functions
      }
    } catch (error) {
      console.error("Network or other error:", error);
      errors.general = [
        "No se pudo conectar con el servidor. Por favor, revisa tu conexión a internet.",
      ];
    } finally {
      isLoading = false;
    }
  }

  // Helper function to get CSRF token from cookies
  function getCookie(name: string) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
</script>

<div class="min-h-[calc(100vh-20px)] text-[color:var(--color-text)]">
  <div class="min-h-[24px]"></div>
  <div
    class="max-w-3xl mx-auto p-6 bg-[color:var(--color-bg-dark)]/90 shadow-lg rounded-lg bg-cover bg-center"
    style="background-image: url('/svg/core_bg.svg'); opacity: 1;"
  >
    <h2 class="text-3xl font-bold text-center mb-6 text-gray-800">
      Formulario de Reserva
    </h2>

    {#if successMessage}
      <div
        role="alert"
        class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-4"
      >
        <p>{successMessage}</p>
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

    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      <fieldset class="border border-gray-300 p-4 rounded-md">
        <legend class="text-lg font-semibold px-2"
          >Datos del Huésped Principal</legend
        >
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <div>
            <label for="first_name" class="block text-sm font-medium mb-1"
              >Nombre</label
            >
            <input
              type="text"
              id="first_name"
              bind:value={formData.guest_first_name}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.guest_first_name}
              <p class="mt-1 text-sm text-red-600">
                {errors.guest_first_name[0]}
              </p>
            {/if}
          </div>
          <div>
            <label for="last_name" class="block text-sm font-medium mb-1"
              >Apellido</label
            >
            <input
              type="text"
              id="last_name"
              bind:value={formData.guest_last_name}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.guest_last_name}
              <p class="mt-1 text-sm text-red-600">
                {errors.guest_last_name[0]}
              </p>
            {/if}
          </div>
          <div>
            <label for="email" class="block text-sm font-medium mb-1"
              >Email</label
            >
            <input
              type="email"
              id="email"
              bind:value={formData.guest_email}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.guest_email}
              <p class="mt-1 text-sm text-red-600">{errors.guest_email[0]}</p>
            {/if}
          </div>
          <div>
            <label for="phone" class="block text-sm font-medium mb-1"
              >Teléfono (Opcional)</label
            >
            <input
              type="tel"
              id="phone"
              bind:value={formData.guest_phone}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
            {#if errors.guest_phone}
              <p class="mt-1 text-sm text-red-600">{errors.guest_phone[0]}</p>
            {/if}
          </div>
          <div>
            <label>DNI</label>
            <input
              type="text"
              id="last_name"
              bind:value={formData.guest_vat}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
          </div>
          <div class="flex items-center space-x-2">
            <input
              type="checkbox"
              id="myCheckbox"
              bind:checked={formData.guest_adult}
              class="h-4 w-4  border-gray-300 rounded focus:ring-indigo-500"
              aria-labelledby="myCheckboxLabel"
            />
            <label
              for="myCheckbox"
              id="myCheckboxLabel"
             
            >
              Adulto
            </label>
          </div>
        </div>
      </fieldset>

      {#each formData.additional_guests as guest, i (i)}
        <fieldset class="border border-gray-300 p-4 rounded-md relative">
          <legend class="text-lg font-semibold px-2"
            >Huésped Adicional {i + 1}</legend
          >
          <button
            type="button"
            on:click={() => removeGuest(i)}
            class="absolute top-2 right-2 text-red-600 hover:text-red-800 font-bold text-xl"
            aria-label="Remove guest"
          >
            &times;
          </button>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
            <div>
              <!-- name -->
              
              <label
                for="additional_guest_first_name_{i}"
                class="block text-sm font-medium mb-1">Nombre</label
              >
              <input
                type="text"
                id="additional_guest_first_name_{i}"
                bind:value={guest.name}
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
              {#if errors.additional_guests && errors.additional_guests[i] && errors.additional_guests[i].first_name}
                <p class="mt-1 text-sm text-red-600">
                  {errors.additional_guests[i].name[0]}
                </p>
              {/if}
            </div>
            <div>
              <label
                for="additional_guest_last_name_{i}"
                class="block text-sm font-medium mb-1">Apellido</label
              >
              <input
                type="text"
                id="additional_guest_last_name_{i}"
                bind:value={guest.last_name}
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
              {#if errors.additional_guests && errors.additional_guests[i] && errors.additional_guests[i].last_name}
                <p class="mt-1 text-sm text-red-600">
                  {errors.additional_guests[i].last_name[0]}
                </p>
              {/if}
            </div>
            <div>
              <label>DNI</label>
              <input
                type="text"
                id="last_name"
                bind:value={guest.vat}
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>
            <div class="flex items-center space-x-2">
              <input
                type="checkbox"
                id="myCheckbox"
                bind:checked={formData.guest_adult}
                class="h-4 w-4  border-gray-300 rounded focus:ring-indigo-500"
                aria-labelledby="myCheckboxLabel"
              />
              <label
                for="myCheckbox"
                id="myCheckboxLabel"
               
              >
                Adulto
              </label>
            </div>
          </div>
        </fieldset>
      {/each}
      <div class="flex justify-center">
        <button
          type="button"
          on:click={addGuest}
          class="core_button font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform mt-0"
        >
          Añadir Huésped
        </button>
      </div>
      <fieldset class="border border-gray-300 p-4 rounded-md">
        <legend class="text-lg font-semibold px-2">Fechas de la Reserva</legend>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <div>
            <label for="check_in_date" class="block text-sm font-medium mb-1"
              >Fecha de Entrada</label
            >
            <input
              type="date"
              id="check_in_date"
              bind:value={formData.check_in_date}
              min={today}
              on:change={updateMinCheckoutDate}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.check_in_date}
              <p class="mt-1 text-sm text-red-600">{errors.check_in_date[0]}</p>
            {/if}
          </div>
          <div>
            <label for="check_out_date" class="block text-sm font-medium mb-1"
              >Fecha de Salida</label
            >
            <input
              type="date"
              id="check_out_date"
              bind:value={formData.check_out_date}
              min={formData.check_in_date
                ? new Date(
                    new Date(formData.check_in_date).setDate(
                      new Date(formData.check_in_date).getDate() + 1,
                    ),
                  )
                    .toISOString()
                    .split("T")[0]
                : ""}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.check_out_date}
              <p class="mt-1 text-sm text-red-600">
                {errors.check_out_date[0]}
              </p>
            {/if}
          </div>
        </div>
      </fieldset>

      <div>
        <label for="special_requests" class="block text-sm font-medium mb-1"
          >Solicitudes Especiales (Opcional)</label
        >
        <textarea
          id="special_requests"
          bind:value={formData.special_requests}
          rows="4"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        ></textarea>
        {#if errors.special_requests}
          <p class="mt-1 text-sm text-red-600">{errors.special_requests[0]}</p>
        {/if}
      </div>
      <div class="flex justify-center">
        <button
          type="submit"
          class="core_button font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform mt-0"
          disabled={isLoading}
        >
          {#if isLoading}
            Enviando...
          {:else}
            Confirmar Reserva
          {/if}
        </button>
      </div>
    </form>
  </div>
  <div class="min-h-[24px]"></div>
</div>
