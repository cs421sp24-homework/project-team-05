import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '@/App.vue'
import router from '@/router'



// describe('Routing Test for Authentication Protection', () => {
    
//     const routes = router.getRoutes();
//     const wrapper = mount(App, {global: {plugins: [router]}});
//     for (const route of routes) {
//         it(route.meta.requiresAuth? 
//             "Redirects to 'Home' page when accessing '" + route.path + "' page without authentication;" : 
//             "Stay at '" + route.path + "' page without authentication;" , async () => {
//                 await router.push(route.path);
//                 if (route.meta.requiresAuth) expect(wrapper.vm.$route.path).toBe('/');
//                 else expect(wrapper.vm.$route.path).toBe(route.path);
//             }
//         )
//     }
// })


describe("End-to-end Test", () => {
    const wrapper = mount(App, {global: {plugins: [router]}});
    it("Click 'login' at Home page" , async () => {
        await router.push('/');
        await wrapper.find('#navLogin').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe('/login');
    })

    it("Input JHED" , async () => {
        const jin = wrapper.find('#jhed');
        jin.element.value = 'zxu129';
        await jin.trigger('input');
        expect(jin.element.value).toBe('zxu129');
    })

    it("Input Password" , async () => {
        const pin = wrapper.find('#pw');
        pin.element.value = '111qqq';
        await pin.trigger('input');
        expect(pin.element.value).toBe('111qqq');
    })

    it("Click 'Login' button on Login page", async () => {
        wrapper.find('#logBtn').trigger('click');
        await router.isReady();
        await new Promise(resolve => setTimeout(resolve, 2000));
        expect(wrapper.vm.$route.path).toBe('/userhome');
    })

    it("Click avatar on the nav-bar", async () => {
        wrapper.find('#avt').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe('/me');
    })

    it("Click 'New Post' Button", async () => {
        wrapper.find('#toPost').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe('/postitem');
    })

    it("Input Item Name", async () => {
        const inin = wrapper.find('#itemName');
        inin.element.value = 'E2E Test Item';
        await inin.trigger('input');
        expect(inin.element.value).toBe('E2E Test Item');
    })

    it("Select Catogory", async () => {
        const ctsl = wrapper.find('#Category');
        ctsl.element.value = 'Electronics';
        await ctsl.trigger('change');
        expect(ctsl.element.value).toBe('Electronics');
    })

    it("Input Price", async () => {
        const inin = wrapper.find('#price');
        inin.element.value = '88';
        await inin.trigger('input');
        expect(inin.element.value).toBe('88');
    })

    it("Input Description", async () => {
        const dsin = wrapper.find('#description');
        dsin.element.value = 'E2E Test Item E2E Test Item';
        await dsin.trigger('input');
        expect(dsin.element.value).toBe('E2E Test Item E2E Test Item');
    })

    it("Click 'Post' Button", async () => {
        await wrapper.find('#form').trigger('submit.prevent');
        await new Promise(resolve => setTimeout(resolve, 1000));
        expect(wrapper.vm.$route.path).toBe('/me');
        expect(wrapper.html()).toContain('E2E Test Item');
    })

    it("Click the New Item", async () => {
        await wrapper.find('#card0').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 10));
    })
    
    it("Click 'Edit' Button", async () => {
        await new Promise(resolve => setTimeout(resolve, 300));
        await wrapper.find('#editBtn').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toContain('/edititem');
    })
    
    it("Change the Name of the Item", async () => {
        const nnin = wrapper.find('#itemName');
        nnin.element.value = 'E2E Changed';
        await nnin.trigger('input');
        expect(nnin.element.value).toBe('E2E Changed');
    })

    it("Click 'Update' Button", async () => {
        await wrapper.find('#form').trigger('submit.prevent');
        await new Promise(resolve => setTimeout(resolve, 1000));
        expect(wrapper.vm.$route.path).toContain('/showitem');
        expect(wrapper.html()).toContain('E2E Changed');
    })

    it("Click avatar on the nav-bar", async () => {
        wrapper.find('#avt').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe('/me');
        expect(wrapper.html()).toContain('E2E Changed');
    });

})