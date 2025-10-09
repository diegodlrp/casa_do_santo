<script lang="ts">
    import { LL } from "$i18n/i18n-svelte";
    import RiPhoneLine from "svelte-remixicon/RiPhoneLine.svelte";
    import RiMailLine from "svelte-remixicon/RiMailLine.svelte";
    import RiMapPin2Line from "svelte-remixicon/RiMapPin2Line.svelte";
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";

    export let data: PageData;

    // Destructure the data directly
    const {
        title_img,
        contact_img,
        form_img,
        error,
    } = data;
    
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

    const handleSubmit = async () => {

        const response = await fetch('http://localhost:8000/api/send-mail/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'

					// Add CSRF token header if needed (see previous email example notes)
				},
				mode: 'cors',
				// Send petition data as JSON
				body: JSON.stringify({ name: name, mail: email, message: message, language: locale}),
				credentials: 'omit'
			});
    };
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
                                    <a href="tel:{phone.number}">{phone.number}</a>
                                </div>
                                {/each}
                                
                                <div
                                    class="flex felx-row items-center space-x-2"
                                >
                                    <RiMailLine />
                                    <a href="mailto:{contact_email}">{contact_email}</a>
                                </div>
                                <div
                                    class="flex felx-row items-center space-x-2"
                                >
                                    <RiMapPin2Line />
                                    <a href="{contact_address_link}">{contact_address}</a>
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
                                <div class="flex items-center">
                                    <input
                                        id="checked-checkbox"
                                        type="checkbox"
                                        value=""
                                        class="w-4 h-4"
                                        required
                                    />
                                    
                                </div>
                                <!-- END checkbox -->
                                <!-- START button -->
                                <button
                                    class="core_button font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform mt-[30px]"
                                    >{$LL.send_message()}</button
                                >
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
