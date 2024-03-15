<template>
    <div class="my-items">
        <UserNavbar :currentUser="currentUser" @userLogout="userStateChange" />
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <h1 class="text-center">{{ text }}</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <Cards :cards="postCardsData" />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Cards from "@/components/Cards.vue";
import axios from "axios";
export default {
    name: "ShowAll",
    props: {
        currentUser: Object,
    },
    components: {
        UserNavbar,
        Cards,
    },
    data() {
        return {
            text: "",
            data: "",
            postCardsData: [],
        };
    },
    created() {
        const HTTP_PREFIX = import.meta.env.VITE_HOST;
        this.data = this.$route.params.data;
        if (this.data == "myItems") {
            this.text = "My Items";
            this.getAllItems();
        }
        else if (this.data == "Wishlist") {
            this.text = "Wishlist";
            this.getWishlist();
        }
        else if (this.data == "history") {
            this.text = "Order History";
            this.getHistoryItems();
        }
    },
    methods: {
        userStateChange() {
            this.$emit("userStateChange", {});
        },
        async getAllItems() {
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            try {
                const accessToken = localStorage.getItem("access_token");
                const response = await axios.get(HTTP_PREFIX + "api/v1/post/UserItems/all", {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });
                this.postCardsData = response.data;
            } catch (error) {
                console.error(error);
            }
        },
        async getWishlist() {
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            try {
                const accessToken = localStorage.getItem("access_token");
                const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/Collection", {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });
                this.postCardsData = response.data;
            } catch (error) {
                console.error(error);
            }
        },
        async getHistoryItems() {
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            try {
                const accessToken = localStorage.getItem("access_token");
                const response = await axios.get(HTTP_PREFIX + "api/v1/post/UserItems/all", {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });
                this.postCardsData = response.data;
            } catch (error) {
                console.error(error);
            }
        },
    },
};
</script>
<style scoped>
.container {
    margin-top: 12vh;
}
</style>