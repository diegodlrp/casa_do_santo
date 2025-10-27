<script lang="ts">
  import { invalidateAll } from "$app/navigation";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import type { PageData } from "./$types";
  import FormField from "$lib/FormField.svelte";

  export let data: PageData;

  // Destructure props from data
  $: ({
    main_guest_name,
    main_guest_vat,
    main_guest_email,
    check_in_date,
    check_out_date,
    special_request,
    reservation_id,
    reservationform_mandatory1,
    reservationform_mandatory2,
    reservationform_mandatory3,
    reservationform_info1,
    reservationform_info2,
  } = data);

  // --- 1. UNIFIED GUEST INTERFACE ---
  // All fields are now in one interface for every guest.
  interface GuestData {
    first_name: string;
    last_name: string;
    last_name2: string;
    sex: string;
    document_type: string;
    document_support: string;
    vat: string;
    birth_date: string;
    nacionality: string;
    address: string;
    address_state: string;
    country: string;
    phone: string;
    mobile: string;
    email: string;
    adult: boolean;
  }

  // --- 2. UNIFIED FORM DATA STRUCTURE ---
  // The form now holds a single array of guests. The primary guest is always at index 0.
  interface FormData {
    guests: GuestData[];
    check_in_date: string;
    check_out_date: string;
    special_requests: string;
    reservation_id: Integer;
  }

  // Helper function to create a new, empty guest object
  const createNewGuest = (isPrimary = false): GuestData => ({
    first_name: "",
    last_name: "",
    last_name2: "",
    sex: "",
    document_type: "",
    document_support: "",
    vat: "",
    birth_date: "",
    nacionality: "",
    address: "",
    address_state: "",
    country: "",
    phone: "",
    mobile: "",
    email: "",
    adult: isPrimary, // Primary guest is an adult by default
  });

  // Initial form data with one primary guest
  let formData: FormData = {
    guests: [createNewGuest(true)], // Start with the primary guest
    check_in_date: "",
    check_out_date: "",
    special_requests: "",
    reservation_id: 0,
  };

  // --- 3. UPDATED ERROR STRUCTURE ---
  // Errors will now be an object containing a 'guests' array.
  let errors: {
    guests?: { [key: string]: string[] }[];
    general?: string[];
    [key: string]: any;
  } = {};
  let successMessage: string = "";
  let isLoading: boolean = false;

  const documentTypes = [
    { value: "dni", label: "DNI (Documento Nacional de Identidad)" },
    { value: "passport", label: "Pasaporte" },
    { value: "nie", label: "NIE (Número de Identidad de Extranjero)" },
  ];

  onMount(() => {
    // Populate the primary guest (at index 0) and other form data
    formData.guests[0].first_name = main_guest_name || "";
    formData.guests[0].vat = main_guest_vat || "";
    formData.guests[0].email = main_guest_email || "";
    formData.check_in_date = check_in_date;
    formData.check_out_date = check_out_date;
    formData.special_requests = special_request;
    formData.reservation_id = reservation_id;
  });

  // --- 4. SIMPLIFIED GUEST MANAGEMENT ---
  function addGuest() {
    formData.guests = [...formData.guests, createNewGuest()];
  }

  function removeGuest(index: number) {
    // Prevent removing the primary guest
    if (index > 0) {
      formData.guests = formData.guests.filter((_, i) => i !== index);
    }
  }

  // --- 5. UNIFIED VALIDATION LOGIC ---
  function validateForm(): boolean {
    errors = {}; // Clear previous errors
    let isValid = true;
    const guestErrors: { [key: string]: string[] }[] = [];

    formData.guests.forEach((guest, index) => {
      const singleGuestErrors: { [key: string]: string[] } = {};
      if (!guest.first_name.trim())
        singleGuestErrors.first_name = ["El nombre es requerido."];
      if (!guest.last_name.trim())
        singleGuestErrors.last_name = ["El primer apellido es requerido."];
      if (!guest.vat.trim())
        singleGuestErrors.vat = ["El Nº del documento es requerido."];
      if (!guest.birth_date)
        singleGuestErrors.birth_date = ["La fecha de nacimiento es requerida."];
      if (!guest.document_type)
        singleGuestErrors.document_type = [
          "El tipo de documento es requerido.",
        ];
      if (
        index === 0 &&
        (!guest.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(guest.email))
      ) {
        singleGuestErrors.email = ["Por favor, introduce un email válido."];
      }

      if (Object.keys(singleGuestErrors).length > 0) {
        isValid = false;
        guestErrors[index] = singleGuestErrors;
      }
    });

    if (guestErrors.length > 0) {
      errors.guests = guestErrors;
    }

    // Validate dates
    if (new Date(formData.check_out_date) <= new Date(formData.check_in_date)) {
      errors.check_out_date = [
        "La fecha de salida debe ser posterior a la de entrada.",
      ];
      isValid = false;
    }

    return isValid;
  }

  async function handleSubmit() {
    successMessage = "";
    if (!validateForm()) {
      return;
    }
    isLoading = true;
    try {
      // The formData is already in the correct shape for the backend
      const response = await fetch(
        "https://casadosantoadmin.casacam.net/api-reservation/edit-reservation/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: JSON.stringify(formData),
        },
      );

      if (!response.ok) {
        const errorData = await response.json();
        errors = errorData;
      } else {
        successMessage = "¡Reserva realizada con éxito!";
        errors = {};
      }
    } catch (error) {
      errors.general = ["No se pudo conectar con el servidor."];
    } finally {
      isLoading = false;
    }
  }

  function getCookie(name: string) {
    if (typeof document === "undefined") return null;
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
        {#each errors.general as error}<p>{error}</p>{/each}
      </div>
    {/if}

    <div>{@html reservationform_info1}</div>
    <div>{@html reservationform_info2}</div>

    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      {#each formData.guests as guest, i (i)}
        <fieldset class="border border-gray-300 p-4 rounded-md relative">
          <legend class="text-lg font-semibold px-2">
            {#if i === 0}
              Datos del Huésped Principal
            {:else}
              Huésped Adicional {i}
            {/if}
          </legend>

          {#if i > 0}
            <button
              type="button"
              on:click={() => removeGuest(i)}
              class="absolute top-2 right-2 text-red-600 hover:text-red-800 font-bold text-xl"
              aria-label="Remove guest">&times;</button
            >
          {/if}

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
            <FormField
              label="Nombre <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>⁾"
              id="first_name_{i}"
              bind:value={guest.first_name}
              required
              errors={errors.guests?.[i]?.first_name}
            />
            <FormField
              label="Primer Apellido <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="last_name_{i}"
              bind:value={guest.last_name}
              optional
              errors={errors.guests?.[i]?.last_name}
            />
            <FormField
              label="Segundo Apellido <a href='#section_1'>¹⁾</a>"
              id="last_name2_{i}"
              bind:value={guest.last_name2}
              optional
              errors={errors.guests?.[i]?.last_name2}
            />
            <FormField
              label="Fecha Nacimiento <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="birth_date_{i}"
              type="date"
              bind:value={guest.birth_date}
              optional
              errors={errors.guests?.[i]?.birth_date}
            />
            <FormField
              label="Sexo"
              id="sex_{i}"
              bind:value={guest.sex}
              optional
              errors={errors.guests?.[i]?.sex}
            />
            <FormField
              label="País de Nacionalidad <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="nationality_{i}"
              bind:value={guest.nacionality}
              optional
              errors={errors.guests?.[i]?.nacionality}
            />
            <FormField
              label="Tipo de Documento <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="document_type_{i}"
              type="select"
              bind:value={guest.document_type}
              options={documentTypes}
              optional
              errors={errors.guests?.[i]?.document_type}
            />
            <FormField
              label="Nº del documento <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="vat_{i}"
              bind:value={guest.vat}
              optional
              errors={errors.guests?.[i]?.vat}
            />
            <FormField
              label="Soporte del documento <a href='#section_1'>¹⁾</a>"
              id="document_support_{i}"
              bind:value={guest.document_support}
              optional
              errors={errors.guests?.[i]?.document_support}
            />
            <FormField
              label="Dirección <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="address_{i}"
              bind:value={guest.address}
              optional
              errors={errors.guests?.[i]?.address}
            />
            <FormField
              label="Provincia <a href='#section_1'>¹⁾</a>"
              id="address_state_{i}"
              bind:value={guest.address_state}
              optional
              errors={errors.guests?.[i]?.address_state}
            />
            <FormField
              label="País <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="country_{i}"
              bind:value={guest.country}
              optional
              errors={errors.guests?.[i]?.country}
            />
            <FormField
              label="Teléfono <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="phone_{i}"
              type="tel"
              bind:value={guest.phone}
              optional
              errors={errors.guests?.[i]?.phone}
            />
            <FormField
              label="Móvil"
              id="mobile_{i}"
              type="tel"
              bind:value={guest.mobile}
              optional
              errors={errors.guests?.[i]?.mobile}
            />
            <FormField
              label="Email <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
              id="email_{i}"
              type="email"
              bind:value={guest.email}
              required={i === 0}
              optional={i > 0}
              errors={errors.guests?.[i]?.email}
            />
            <FormField
              label="Parentesco <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a><a href='#section_3'>³⁾</a>"
              id="country_{i}"
              bind:value={guest.country}
              optional
              errors={errors.guests?.[i]?.country}
            />
            <FormField
              label="Adulto"
              id="adult_{i}"
              type="checkbox"
              bind:value={guest.adult}
            />
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
          <FormField
            label="Fecha de Entrada <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
            id="check_in_date"
            type="date"
            bind:value={formData.check_in_date}
            optional
            disabled
            errors={errors.check_in_date}
          />
          <FormField
            label="Fecha de Salida <a href='#section_1'>¹⁾</a><a href='#section_2'>²⁾</a>"
            id="check_out_date"
            type="date"
            bind:value={formData.check_out_date}
            optional
            disabled
            errors={errors.check_out_date}
          />
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
      </div>

      <div class="flex justify-center">
        <button
          type="submit"
          class="core_button font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform mt-0"
          disabled={isLoading}
        >
          {#if isLoading}Enviando...{:else}Confirmar Reserva{/if}
        </button>
      </div>
    </form>
  </div>
  <div class="min-h-[24px]"></div>
  <div
    id="section_1"
    class="max-w-3xl mx-auto p-6 bg-[color:var(--color-bg-dark)]/90 shadow-lg rounded-lg bg-cover bg-center"
    style="background-image: url('/svg/core_bg.svg'); opacity: 1;"
  >
   1) {@html reservationform_mandatory1}
  </div>

  <div class="min-h-[24px]"></div>
  <div
    id="section_2"
    class="max-w-3xl mx-auto p-6 bg-[color:var(--color-bg-dark)]/90 shadow-lg rounded-lg bg-cover bg-center"
    style="background-image: url('/svg/core_bg.svg'); opacity: 1;"
  >
   2) {@html reservationform_mandatory2}
  </div>
  <div class="min-h-[24px]"></div>
  <div
    id="section_3"
    class="max-w-3xl mx-auto p-6 bg-[color:var(--color-bg-dark)]/90 shadow-lg rounded-lg bg-cover bg-center"
    style="background-image: url('/svg/core_bg.svg'); opacity: 1;"
  >
   3) {@html reservationform_mandatory3}
  </div>
  <div class="min-h-[24px]"></div>
</div>
