import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import App from "@/App.vue";
import router from "@/router";

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
        await new Promise((resolve) => setTimeout(resolve, 4000));
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
        await new Promise((resolve) => setTimeout(resolve, 100));
        const nnin = wrapper.find("#itemName");
        nnin.element.value = "E2E Changed";
        await nnin.trigger("input");
        expect(nnin.element.value).toBe("E2E Changed");
    });

    it("Click 'Update' Button", async () => {
        await wrapper.find("#form").trigger("submit.prevent");
        await new Promise((resolve) => setTimeout(resolve, 1000));
        expect(wrapper.vm.$route.path).toContain("/showitem");
        await new Promise((resolve) => setTimeout(resolve, 300));
        expect(wrapper.html()).toContain("E2E Changed");
    });
    // Search the new item -- show changed name
    it("Click Icon on the Nav-bar", async () => {
        wrapper.find("#sechand-icon").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/");
    });

    it("Input New Item Name in the Search Box", async () => {
        await new Promise((resolve) => setTimeout(resolve, 500));
        const nnin = wrapper.find("#searchid");
        nnin.element.value = "E2E";
        await nnin.trigger("input");
        expect(nnin.element.value).toBe("E2E");
    });

    it("Click the Search Button", async () => {
        await wrapper.find("#searchbtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.html()).toContain("E2E Changed");
    });

    it("Click the New Item", async () => {
        await wrapper.find("#cardE2E").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toContain("/showitem");
    });

    it("Click 'Edit' Button", async () => {
        await new Promise((resolve) => setTimeout(resolve, 500));
        await wrapper.find("#editBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 500));
        expect(wrapper.vm.$route.path).toContain("/edititem");
    });

    it("Click 'Delete' Button", async () => {
        await new Promise((resolve) => setTimeout(resolve, 100));
        await wrapper.find("#dltBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/me");
        expect(wrapper.html()).not.contain("E2E Changed");
    });
    // Update profile -- change nickname -- sync with all pages
    it("Click 'My Profile' Button", async () => {
        await wrapper.find("#profile").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/profile");
    });

    it("Click 'Edit' Button", async () => {
        await wrapper.find("#editBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.html()).contain("Save");
    });

    it("Change the Nick Name of the User", async () => {
        await new Promise((resolve) => setTimeout(resolve, 100));
        const nnin = wrapper.find("#nickname");
        nnin.element.value = "E2E Name";
        await nnin.trigger("input");
        expect(nnin.element.value).toBe("E2E Name");
    });

    it("Click 'Save' Button (Save the Nick Name)", async () => {
        await wrapper.find("#saveBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        const nnin = wrapper.find("#nickname");
        expect(nnin.element.value).toBe("E2E Name");
    });

    it("Click 'Back' Button", async () => {
        await new Promise((resolve) => setTimeout(resolve, 300));
        await wrapper.find("#backBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/me");
        expect(wrapper.html()).contain("E2E Name");
    });

    it("Click 'My Profile' Button", async () => {
        await wrapper.find("#profile").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/profile");
    });

    it("Click 'Edit' Button", async () => {
        await wrapper.find("#editBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.html()).contain("Save");
    });

    it("Change the Nick Name of the User", async () => {
        await new Promise((resolve) => setTimeout(resolve, 100));
        const nnin = wrapper.find("#nickname");
        nnin.element.value = "Elain";
        await nnin.trigger("input");
        expect(nnin.element.value).toBe("Elain");
    });
    // change the name back
    it("Click 'Save' Button (Save the Nick Name)", async () => {
        await wrapper.find("#saveBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        const nnin = wrapper.find("#nickname");
        expect(nnin.element.value).toBe("Elain");
    });

    it("Click 'Back' Button", async () => {
        await new Promise((resolve) => setTimeout(resolve, 300));
        await wrapper.find("#backBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/me");
        expect(wrapper.html()).contain("Elain");
    });

    // Send new message in Chat
    it("Click Icon on the Nav-bar", async () => {
        wrapper.find("#chat").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 10));
        expect(wrapper.vm.$route.path).toBe("/chat");
    });

    it("Select a Chat", async () => {
        await new Promise((resolve) => setTimeout(resolve, 2000));
        await wrapper.find("#list_item").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.html()).contain("Send");
    });

    it("Input 'E2E msg' in the Chat Box", async () => {
        const msgin = wrapper.find("#input-box");
        msgin.element.value = "E2E msg";
        await msgin.trigger("input");
        expect(msgin.element.value).toBe("E2E msg");
    });

    it("Click Send Button", async () => {
        wrapper.find("#sendBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 200));
        const msgin = wrapper.find("#input-box");
        expect(msgin.element.value).not.toContain("E2E msg");
        expect(wrapper.html()).toContain("E2E msg");
    });

    // User logout
    it("Click 'Logout' Button", async () => {
        await wrapper.find("#logoutBtn").trigger("click");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.vm.$route.path).toBe("/");
        await new Promise((resolve) => setTimeout(resolve, 100));
        expect(wrapper.html()).contain("Login");
    });
});
