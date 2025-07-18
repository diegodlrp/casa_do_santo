<script lang="ts">
    import { invalidateAll } from '$app/navigation';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
  
    // Tipos para los datos del formulario
    interface FormData {
      guest_first_name: string;
      guest_last_name: string;
      guest_email: string;
      guest_phone: string;
      check_in_date: string; // Usamos string para el input type="date"
      check_out_date: string;
      num_adults: number;
      num_children: number;
      special_requests: string;
    }
  
    let formData: FormData = {
      guest_first_name: '',
      guest_last_name: '',
      guest_email: '',
      guest_phone: '',
      check_in_date: '',
      check_out_date: '',
      num_adults: 1,
      num_children: 0,
      special_requests: '',
    };
  
    let errors: { [key: string]: string[] } = {};
    let successMessage: string = '';
    let isLoading: boolean = false;
  
    // Set minimum date for check-in to today
    let today: string;
    onMount(() => {
      const d = new Date();
      const year = d.getFullYear();
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const day = d.getDate().toString().padStart(2, '0');
      today = `${year}-${month}-${day}`;
  
      // Initialize check-in date if not set, and ensure it's not in the past
      if (!formData.check_in_date || new Date(formData.check_in_date) < new Date(today)) {
        formData.check_in_date = today;
      }
      // Ensure check-out is at least one day after check-in
      updateMinCheckoutDate();
    });
  
    // Function to update the minimum check-out date
    function updateMinCheckoutDate() {
      if (formData.check_in_date) {
        const checkIn = new Date(formData.check_in_date);
        checkIn.setDate(checkIn.getDate() + 1); // Check-out must be at least one day after check-in
        const year = checkIn.getFullYear();
        const month = (checkIn.getMonth() + 1).toString().padStart(2, '0');
        const day = checkIn.getDate().toString().padStart(2, '0');
        const minCheckout = `${year}-${month}-${day}`;
  
        // If current check-out date is before the new minimum, reset it
        if (!formData.check_out_date || new Date(formData.check_out_date) < new Date(minCheckout)) {
          formData.check_out_date = minCheckout;
        }
      }
    }
  
    // Basic client-side validation
    function validateForm(): boolean {
      errors = {}; // Clear previous errors
      let isValid = true;
  
      if (!formData.guest_first_name.trim()) {
        errors.guest_first_name = ['El nombre es requerido.'];
        isValid = false;
      }
      if (!formData.guest_last_name.trim()) {
        errors.guest_last_name = ['El apellido es requerido.'];
        isValid = false;
      }
      if (!formData.guest_email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.guest_email)) {
        errors.guest_email = ['Por favor, introduce un email válido.'];
        isValid = false;
      }
      if (!formData.check_in_date) {
        errors.check_in_date = ['La fecha de entrada es requerida.'];
        isValid = false;
      }
      if (!formData.check_out_date) {
        errors.check_out_date = ['La fecha de salida es requerida.'];
        isValid = false;
      }
  
      if (formData.check_in_date && formData.check_out_date) {
        const checkIn = new Date(formData.check_in_date);
        const checkOut = new Date(formData.check_out_date);
        if (checkOut <= checkIn) {
          errors.check_out_date = ['La fecha de salida debe ser posterior a la de entrada.'];
          isValid = false;
        }
      }
  
      if (formData.num_adults < 1) {
        errors.num_adults = ['Debe haber al menos un adulto.'];
        isValid = false;
      }
  
      return isValid;
    }
  
    async function handleSubmit() {
      successMessage = '';
      if (!validateForm()) {
        return; // Stop if client-side validation fails
      }
  
      isLoading = true;
      try {
        const response = await fetch('http://127.0.0.1:8000/reservations/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // If you have CSRF protection, you'd need to send the CSRF token from Django
            // For Django, you'd typically get the CSRF token from a meta tag or a cookie
            // Example (assuming CSRF_USE_SESSIONS is True and you have a CSRF cookie):
            // 'X-CSRFToken': getCookie('csrftoken') // You'd need a helper function for this
          },
          body: JSON.stringify(formData),
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          errors = errorData; // Django REST Framework often returns errors in this format
          if (response.status === 409 && errorData.detail) {
              errors.general = [errorData.detail]; // For availability conflicts
          } else if (errorData.non_field_errors) {
              errors.general = errorData.non_field_errors;
          } else {
              errors.general = ["Ocurrió un error inesperado al procesar la reserva. Por favor, inténtalo de nuevo."];
          }
          console.error('API Error:', errorData);
        } else {
          const result = await response.json();
          successMessage = '¡Reserva realizada con éxito!';
          console.log('Reservation successful:', result);
          // Optionally reset form
          formData = {
            guest_first_name: '',
            guest_last_name: '',
            guest_email: '',
            guest_phone: '',
            check_in_date: today,
            check_out_date: new Date(new Date(today).setDate(new Date(today).getDate() + 1)).toISOString().split('T')[0],
            num_adults: 1,
            num_children: 0,
            special_requests: '',
          };
          errors = {}; // Clear errors on success
          // Invalidate all SvelteKit load functions if you have any lists of reservations
          // invalidateAll();
        }
      } catch (error) {
        console.error('Network or other error:', error);
        errors.general = ['No se pudo conectar con el servidor. Por favor, revisa tu conexión a internet.'];
      } finally {
        isLoading = false;
      }
    }
  
    // Helper function to get CSRF token from cookies (if using cookie-based CSRF)
    // This is a basic example, you might want a more robust one.
    function getCookie(name: string) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  </script>
  
  <div class="max-w-3xl mx-auto p-6 bg-white shadow-lg rounded-lg my-8">
    <h2 class="text-3xl font-bold text-center mb-6 text-gray-800">Formulario de Reserva</h2>
  
    {#if successMessage}
      <div role="alert" class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-4">
        <p>{successMessage}</p>
      </div>
    {/if}
  
    {#if errors.general}
      <div role="alert" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
        {#each errors.general as error}
          <p>{error}</p>
        {/each}
      </div>
    {/if}
  
    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      <fieldset class="border border-gray-300 p-4 rounded-md">
        <legend class="text-lg font-semibold text-gray-700 px-2">Datos del Huésped Principal</legend>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <div>
            <label for="first_name" class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
            <input
              type="text"
              id="first_name"
              bind:value={formData.guest_first_name}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.guest_first_name}
              <p class="mt-1 text-sm text-red-600">{errors.guest_first_name[0]}</p>
            {/if}
          </div>
          <div>
            <label for="last_name" class="block text-sm font-medium text-gray-700 mb-1">Apellido</label>
            <input
              type="text"
              id="last_name"
              bind:value={formData.guest_last_name}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.guest_last_name}
              <p class="mt-1 text-sm text-red-600">{errors.guest_last_name[0]}</p>
            {/if}
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
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
            <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Teléfono (Opcional)</label>
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
        </div>
      </fieldset>
  
      <fieldset class="border border-gray-300 p-4 rounded-md">
        <legend class="text-lg font-semibold text-gray-700 px-2">Fechas de la Reserva</legend>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <div>
            <label for="check_in_date" class="block text-sm font-medium text-gray-700 mb-1">Fecha de Entrada</label>
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
            <label for="check_out_date" class="block text-sm font-medium text-gray-700 mb-1">Fecha de Salida</label>
            <input
              type="date"
              id="check_out_date"
              bind:value={formData.check_out_date}
              min={formData.check_in_date ? new Date(new Date(formData.check_in_date).setDate(new Date(formData.check_in_date).getDate() + 1)).toISOString().split('T')[0] : ''}
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.check_out_date}
              <p class="mt-1 text-sm text-red-600">{errors.check_out_date[0]}</p>
            {/if}
          </div>
        </div>
      </fieldset>
  
      <fieldset class="border border-gray-300 p-4 rounded-md">
        <legend class="text-lg font-semibold text-gray-700 px-2">Número de Huéspedes</legend>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <div>
            <label for="num_adults" class="block text-sm font-medium text-gray-700 mb-1">Adultos</label>
            <input
              type="number"
              id="num_adults"
              bind:value={formData.num_adults}
              min="1"
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.num_adults}
              <p class="mt-1 text-sm text-red-600">{errors.num_adults[0]}</p>
            {/if}
          </div>
          <div>
            <label for="num_children" class="block text-sm font-medium text-gray-700 mb-1">Niños</label>
            <input
              type="number"
              id="num_children"
              bind:value={formData.num_children}
              min="0"
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
            {#if errors.num_children}
              <p class="mt-1 text-sm text-red-600">{errors.num_children[0]}</p>
            {/if}
          </div>
        </div>
      </fieldset>
  
      <div>
        <label for="special_requests" class="block text-sm font-medium text-gray-700 mb-1">Solicitudes Especiales (Opcional)</label>
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
  
      <button
        type="submit"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        disabled={isLoading}
      >
        {#if isLoading}
          Enviando...
        {:else}
          Confirmar Reserva
        {/if}
      </button>
    </form>
  </div>
