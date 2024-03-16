import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import App from "@/App.vue";
import router from "@/router";

describe('Routing Test for Authentication Protection', () => {

    const routes = router.getRoutes();
    const wrapper = mount(App, {global: {plugins: [router]}});
    for (const route of routes) {
        it(route.meta.requiresAuth?
            "Redirects to 'Home' page when accessing '" + route.path + "' page without authentication;" :
            "Stay at '" + route.path + "' page without authentication;" , async () => {
                await router.push(route.path);
                if (route.meta.requiresAuth) expect(wrapper.vm.$route.path).toBe('/');
                else expect(wrapper.vm.$route.path).toBe(route.path);
            }
        )
    }
})
