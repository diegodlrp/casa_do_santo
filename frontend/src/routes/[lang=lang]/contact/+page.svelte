<script lang="ts">
    import RiPhoneLine from "svelte-remixicon/RiPhoneLine.svelte";
    import RiMailLine from "svelte-remixicon/RiMailLine.svelte";
    import RiMapPin2Line from "svelte-remixicon/RiMapPin2Line.svelte";
    import type { PageData } from "./$types";
    import Title from "$lib/Title.svelte";

    export let data: PageData;

    // Destructure the data directly
    const {
        title_title,
        title_subtitle,
        title_img,
        form_title,
        form_subtitle,
        form_img,
        error,
    } = data;

    let content = "";
    let title = "";
    let phone = "";
    let address = "";
    let name = "";
    let email = "";
    let message = "";
    let img = "";

    const handleSubmit = async () => {};
</script>

<Title title={title_title} subtitle={title_subtitle} img={title_img} />
<div class="min-h-[calc(100vh-264px)] sm:min-h-[calc(100vh-280px)]">
    <div
        id="contact_form"
        class="bg-cover bg-center items-center"
        style="background-image: url({img});"
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
                                    {@html title}
                                </h2>
                                <p class="pr-4">
                                    {@html content}
                                </p>
                            </div>

                            <div>
                                <div
                                    class="flex felx-row items-center space-x-2"
                                >
                                    <RiPhoneLine />
                                    <span>{phone}</span>
                                </div>
                                <div
                                    class="flex felx-row items-center space-x-2"
                                >
                                    <RiMailLine />
                                    <span>{email}</span>
                                </div>
                                <div
                                    class="flex felx-row items-center space-x-2"
                                >
                                    <RiMapPin2Line />
                                    <span>{address}</span>
                                </div>
                            </div>
                        </div>
                        <!-- end -->
                        <!-- start -->
                        <div class="w-[55%]">
                            <form
                                onsubmit={handleSubmit}
                                class="flex flex-col space-y-4 w-[80%]"
                            >
                                <!-- START name -->
                                <div>
                                    <label for="name" class="text-sm"
                                        >'name'</label
                                    >
                                </div>
                                <div>
                                    <input
                                        bind:value={name}
                                        type="text"
                                        placeholder={"your name"}
                                        class="text-[color:var(--color-text)] ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none"
                                        required
                                    />
                                </div>
                                <!-- END name -->
                                <!-- START email -->
                                <div>
                                    <label for="email" class="text-sm"
                                        >{"mail"}:</label
                                    >
                                </div>
                                <div>
                                    <input
                                        bind:value={email}
                                        type="email"
                                        placeholder={"your email"}
                                        class="text-[color:var(--color-text)] ring-1 ring-gray-300 w-full rounded-md px-4 py-2 outline-none"
                                        required
                                    />
                                </div>
                                <!-- END email -->
                                <!-- START message -->
                                <div>
                                    <label for="message" class="text-sm"
                                        >Message</label
                                    >
                                </div>
                                <div>
                                    <textarea
                                        bind:value={message}
                                        placeholder={"write your message"}
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
                                    <label
                                        for="checked-checkbox"
                                        class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                                        >{"accept"}
                                        <a
                                            href="/privacy"
                                            class="text-[#c8a655]"
                                            >{"privacy_politic"}</a
                                        ></label
                                    >
                                </div>
                                <!-- END checkbox -->
                                <!-- START button -->
                                <button
                                    class="contact_form_button font-bold py-2 px-4 hover:scale-105 active:scale-95 transition duration-150 ease-in-out transform"
                                    >{"send message"}</button
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
