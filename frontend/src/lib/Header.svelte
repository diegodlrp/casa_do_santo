<script lang="ts">
	import { base } from '$app/paths'
	import { LL, locale } from '$i18n/i18n-svelte'
	import LocaleSwitcher from './LocaleSwitcher.svelte'
	import RiMenu5Line from "svelte-remixicon/RiMenu5Line.svelte";
    import RiCloseLargeFill from "svelte-remixicon/RiCloseLargeFill.svelte";
    import ReservationSwitcher from './ReservationSwitcher.svelte';

	let nav_menu: HTMLDivElement;
    let show_open = true;
    let name = "Casa do Santo";

    function NavToggle() {
        nav_menu.classList.toggle("left-[0]");
        show_open = !show_open;
    }

</script>

<header class="bg-[color:var(--color-bg-dark)] fixed w-full top-0 left-0 z-950 px-2 sm:px-6 lg:px-8">
    <nav class="container flex items-center justify-between h-16 sm:h-20">
        <div class="sm:text-2xl">
            <h2 class="text-center">
                {name}
            </h2>
        </div>

        <div
            bind:this={nav_menu}
            class="bg-[color:var(--color-bg-dark)]/80 absolute top-0 left-[-100%] min-h-[100vh] w-full backdrop-blur-sm flex items-center justify-center duration-300 overflow-hidden lg:static lg:min-h-fit lg:bg-transparent lg:w-auto"
        >
            <ul class="flex flex-col items-center gap-8 lg:flex-row">
                <li>
                    <a href="{base}/{$locale}" class="nav-link">{$LL.home()}</a>
                </li>
                <ReservationSwitcher />
                <li>
                    <a href="{base}/{$locale}/rooms" class="nav-link">{$LL.rooms()}</a>
                </li>
                <li>
                    <a href="{base}/{$locale}/location" class="nav-link">{$LL.what_to_visit()}</a>
                </li>
                <li>
                    <a href="{base}/{$locale}/gallery" class="nav-link">{$LL.gallery()}</a>
                </li>
                <li>
                    <a href="{base}/{$locale}/contact" class="nav-link">{$LL.contact()}</a>
                </li>
                
                <LocaleSwitcher />
                
            </ul>
        </div>
        
        <div class="text-xl sm:text-3xl cursor-pointer z-50 lg:hidden">
            <button on:click={NavToggle} class="nav-link">
                {#if show_open}
                    <RiMenu5Line />
                {:else}
                    <RiCloseLargeFill />
                {/if}
            </button>
        </div>
    </nav>

</header>
<div class="relative h-16 sm:h-20"></div>