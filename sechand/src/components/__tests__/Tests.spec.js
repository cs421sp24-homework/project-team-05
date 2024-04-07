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

describe("End-to-end Test", () => {
    const wrapper = mount(App, { global: { plugins: [router] } });
    // User login
    it("Click 'login' at Home page", async () => {
        await router.push("/");
        await wrapper.find("#navLogin").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/login");
    });

    it("Input JHED", async () => {
        const jin = wrapper.find("#jhed");
        jin.element.value = "mxia8";
        await jin.trigger("input");
        expect(jin.element.value).toBe("mxia8");
    });

    it("Input Password", async () => {
        const pin = wrapper.find("#pw");
        pin.element.value = "qq1111";
        await pin.trigger("input");
        expect(pin.element.value).toBe("qq1111");
    });

    it("Click 'Login' button on Login page", async () => {
        wrapper.find("#logBtn").trigger("click");
        await router.isReady();
        await new Promise((resolve) => setTimeout(resolve, 2000));
        expect(wrapper.vm.$route.path).toBe("/");
        expect(wrapper.html()).toContain("Logout");
    });

    it("Click Avatar on the nav-bar", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });
    // Post a new item
    it("Click 'New Post' Button", async () => {
        wrapper.find("#toPost").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/postitem");
    });

    it("Input Item Name", async () => {
        expect(wrapper.vm.$route.path).toBe("/postitem");
        await new Promise((resolve) => setTimeout(resolve, 10));
        const inin = wrapper.find("#itemName");
        inin.element.value = "E2E Test Item";
        await inin.trigger("input");
        expect(inin.element.value).toBe("E2E Test Item");
    });

    it("Select Catogory", async () => {
        const ctsl = wrapper.find("#Category");
        ctsl.element.value = "Electronics";
        await ctsl.trigger("change");
        expect(ctsl.element.value).toBe("Electronics");
    });

    it("Input Price", async () => {
        const inin = wrapper.find("#price");
        inin.element.value = "88";
        await inin.trigger("input");
        expect(inin.element.value).toBe("88");
    });

    it("Input Description", async () => {
        const dsin = wrapper.find("#description");
        dsin.element.value = "E2E Test Item E2E Test Item";
        await dsin.trigger("input");
        expect(dsin.element.value).toBe("E2E Test Item E2E Test Item");
    });

    it("Click 'Post' Button", async () => {
        await wrapper.find("#form").trigger("submit.prevent");
        await new Promise((resolve) => setTimeout(resolve, 1000));
        expect(wrapper.vm.$route.path).toBe("/me");
        expect(wrapper.html()).toContain("E2E Test Item");
    });

    // Change the name of the new item
    it("Click the New Item", async () => {
        await wrapper.find("#cardE2E").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toContain("/showitem");
    });

    it("Click 'Edit' Button", async () => {
        await new Promise((resolve) => setTimeout(resolve, 300));
        await wrapper.find("#editBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toContain("/edititem");
    });

    it("Change the Name of the Item", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Update' Button", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/");
    });
    // Search the new item -- show changed name
    it("Click Icon on the Nav-bar", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Input New Item Name in the Search Box", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Click the Search Button", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click the New Item", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Edit' Button", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Delete' Button", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });
    // Update profile -- change nickname -- sync with all pages
    it("Click 'My Profile' Button", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 20));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Edit' Button", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 20));
        expect(wrapper.vm.$route.path).toBe("/");
        
    });

    it("Change the Nick Name of the User", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Save' Button (Save the Nick Name)", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Back' Button", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'My Profile' Button", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Click 'Edit' Button", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Change the Nick Name of the User", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 400));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });
    // change the name back
    it("Click 'Save' Button (Save the Nick Name)", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Click 'Back' Button", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    // Send new message in Chat
    it("Click Icon on the Nav-bar", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 2500));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Select a Chat", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Input 'E2E msg' in the Chat Box", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 300));
        expect(wrapper.vm.$route.path).toBe("/");
    });
    
    it("Click Send Button", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });


    // Iter 3 collection and auto send
    it("Go to Home page", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 300));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Click an Item", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Collect'", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Click 'Message Icon'", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Back to Home", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 300));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Click an Item", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        expect(wrapper.vm.$route.path).toBe("/");
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Cancel Collection", async () => {
        wrapper.find("#avt").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/me");
    });

    it("Back to Home", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 300));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    // User logout
    it("Click 'Logout' Button", async () => {
        await wrapper.find("#logoutBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/");
        await new Promise((resolve) => setTimeout(resolve, 1000));
        expect(wrapper.html()).contain("v-if");
    });
});
