import adapter from '@sveltejs/adapter-node';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter({
            out: 'build' // This is the default; can be omitted or customized
        }),
        alias: {
            '$i18n': 'src/i18n'
        }
    }
};

export default config;