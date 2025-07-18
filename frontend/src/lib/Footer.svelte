<script lang="ts">
    import RiFacebookFill from "svelte-remixicon/RiFacebookFill.svelte";
    import RiTwitterXFill from "svelte-remixicon/RiTwitterXFill.svelte";
    import RiInstagramLine from "svelte-remixicon/RiInstagramLine.svelte";
    import RiPhoneLine from "svelte-remixicon/RiPhoneLine.svelte";
    import RiMailLine from "svelte-remixicon/RiMailLine.svelte";
    import RiMapPin2Line from "svelte-remixicon/RiMapPin2Line.svelte";
    import { base } from "$app/paths";
    import { LL, locale } from "$i18n/i18n-svelte";

    let name = "Casa do Santo";
    let address = "";
    let email = "";
    let phone = "";
</script>

<footer class="bg-[color:var(--color-bg-dark)] relative overflow-hidden">
    <div class="container">
        <!-- START nav links -->
        <div class="flex h-24 items-center text-sm text-gray-300">
            <div
                class="flex flex-1 items-center justify-start sm:items-stretch sm:justify-start"
            >
                <div>
                    <h2>
                        {@html name}
                    </h2>
                </div>
            </div>
            <div
                class="pt-8 mt-12 mb-4 pb-8 flex items-center justify-center sm:items-stretch sm:justify-center"
            >
                <div class="grid grid-cols-1">
                    <a href="{base}/{$locale}" class="nav-link">{$LL.home()}</a>
                    <a href="{base}/{$locale}/rooms" class="nav-link"
                        >{$LL.rooms()}</a
                    >
                    <a href="{base}/{$locale}/location" class="nav-link"
                        >{$LL.location()}</a
                    >
                    <a href="{base}/{$locale}/gallery" class="nav-link"
                        >{$LL.gallery()}</a
                    >
                    <a href="{base}/{$locale}/contact" class="nav-link"
                        >{$LL.contact()}</a
                    >
                </div>
            </div>
            <div
                class="flex flex-1 items-center justify-end sm:items-stretch sm:justify-end"
            >
                <div class="pl-4">
                    <span
                        class="email_icon flex items-center gap-x-1 text-white"
                    >
                        <RiMapPin2Line />
                        {address}
                    </span>

                    <a
                        href="tel:{phone}"
                        class="tel_icon flex items-center gap-x-1 text-white"
                    >
                        <RiPhoneLine />
                        {phone}
                    </a>
                    <a
                        href="mailto:{email}"
                        class="email_icon flex items-center gap-x-1 text-white"
                    >
                        <RiMailLine />
                        {email}
                    </a>
                </div>
            </div>
        </div>
        <!-- END nav links -->

        <!-- START separation line -->
        <div class="container mt-14 mb-5">
            <div class="border-b border-gray-200 relative">
                <div
                    class="absolute top-0 transform -translate-y-1/2 left-0 right-0 max-w-36 mx-auto"
                >
                    <div
                        class="bg-[color:var(--color-bg-dark)] text-white flex justify-center text-lg text-center"
                    >
                        <RiFacebookFill />
                        <RiTwitterXFill />
                        <RiInstagramLine />
                    </div>
                </div>
            </div>
        </div>
        <!-- END separation line -->
        <!-- START nav links -->
        <div class="flex flex-1 items-center justify-center">
            <a href="{base}/{$locale}/legal_advice" class="nav-link px-4 py-2">
                {$LL.legal_notice()}
            </a>

            <a href="{base}/{$locale}/privacy" class="nav-link px-4 py-2">
                {$LL.privacy_politic()}
            </a>

            <a href="{base}/{$locale}/cookies" class="nav-link px-4 py-2">
                {$LL.cookies_policy()}
            </a>
        </div>
        <!-- END nav links -->
    </div>
</footer>
