import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '@/App.vue'
import router from '@/router'

describe('Routing Test for Authentication Protection', () => {
    const routes = router.getRoutes();
    for (const route of routes) {
        it(route.meta.requiresAuth? 
            "Redirects to 'Home' page when accessing '" + route.path + "' page without authentication;" : 
            "Stay at '" + route.path + "' page without authentication;" , async () => {
            const wrapper = mount(App, {global: {plugins: [router]}});
            await router.push(route.path);
            if (route.meta.requiresAuth) expect(wrapper.vm.$route.path).toBe('/');
            else expect(wrapper.vm.$route.path).toBe(route.path);
        })
    }

    // for (const route of routes) {
    //     it("Stay at '" + route.path + "' page WITH authentication;" , async () => {
    //         const wrapper = mount(App, {global: {plugins: [router]}});

    //         await router.push('/login');
    //         await wrapper.find('#jhed').setValue('zxu129');
    //         await wrapper.find('#pw').setValue('111qqq');
    //         await wrapper.find('#logBtn').trigger('click');
    //         // await wrapper.vm.$nextTick();
    //         await new Promise(resolve => setTimeout(resolve, 3000));
    //         expect(wrapper.vm.$route.path).toBe('/userHome');
    //     })
    // }
})