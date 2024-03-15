<template>
    <div>
        <UserNavbar v-if="currentUser" :currentUser="this.currentUser" @userLogout="userStateChange" />
        <Navbar v-else />
        <div class="item-detail container">
            <!-- Left side: Image -->
            <div class="left-side">
                <img :src="item.image" alt="Item Image" id="item-img" />
            </div>

            <!-- Right side: Details -->
            <div class="right-side">
                <h2>{{ item.name }}</h2>
                <p class="price">Price: ${{ item.price }}</p>

                <p>
                    <img :src="item.sellerIcon" class="user-icon" />{{ item.displayname }}
                    <img v-if="!isCurrentUserSeller" src="/comment.png" id="chat" @click="chat" />
                </p>

                <!-- Description -->
                <div class="description">
                    <h5>Description:</h5>
                    <p>{{ item.description }}</p>
                </div>
                <Button id="editBtn" v-if="isCurrentUserSeller" @click="editItem" text="Edit" color="red"></Button>
                <Button id="cllBtn" v-if="!isitemCollected" @click="collectItem" text="Collect"
                    color="lightgreen"></Button>
                <Button v-if="isitemCollected" @click="unCollectItem" text="Collected" color="orange"></Button>
            </div>
        </div>
    </div>
</template>

<script>
import UserNavbar from "@/components/UserNavbar.vue";
import axios from "axios";
import Button from "@/components/Button.vue";
import Navbar from "@/components/Navbar.vue";
export default {

    name: "ShowItem",
    props: {
        currentUser: Object,
    },
    data() {
        return {
            // isCurrentUserSeller: true,
            isitemCollected: Boolean,
            isLoading: false,
            item: {},
            id: null,
            // currentUser: JSON.parse(localStorage.getItem('user'))
        };
    },
    components: {
        UserNavbar,
        Button,
        Navbar
    },
    methods: {
        chat() {
            // console.log("Chatting with seller", this.item.seller);
            this.$router.push({ name: 'DirectChat', params: { receiver: this.item.seller } });
        },
        userStateChange() {
            this.$emit("userStateChange", {});
        },
        editItem() {
            this.$router.push({ name: 'EditItem', params: { id: this.id } });
        },
        async collectItem() {
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            console.log("Collecting item");
            try {
                const accessToken = localStorage.getItem("access_token");
                const response = await axios.post(HTTP_PREFIX + `api/v1/post/Items/Collection/new/${this.id}`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });
                this.isitemCollected = true;
                console.log("collect", this.isitemCollected);
            } catch (error) {
                console.error(error);
            }
        },
        async unCollectItem() {
            console.log("UnCollecting item");
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            try {
                const accessToken = localStorage.getItem("access_token");
                const response = await axios.delete(HTTP_PREFIX + `api/v1/post/Items/Collection/delete/${this.id}`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });
                this.isitemCollected = false;
                console.log("uncollect", this.isitemCollected);
            } catch (error) {
                console.error(error);
            }
        }
    },
    async created() {
        const HTTP_PREFIX = import.meta.env.VITE_HOST;
        // Check if the current user is the seller of the item

        this.id = this.$route.params.id;
        // console.log("collect", this.isitemCollected);
        try {
            const response = await axios.get(HTTP_PREFIX + `api/v1/post/Item/${this.id}`);
            console.log(response.data);
            this.item = response.data;
        } catch (error) {
            console.error(error);
        }

        if (this.currentUser) {
            if (this.currentUser.id === this.item.seller) {
                this.isCurrentUserSeller = true;
            }
        }
        // get if item in collection
        try {
            const accessToken = localStorage.getItem("access_token");
            console.log("collect", this.id);
            const response = await axios.post(HTTP_PREFIX + `api/v1/post/Items/Collection/item/${this.id}`, {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            });
            this.isitemCollected = response.data.collected;
        } catch (error) {
            console.error(error);
        }
    },
    computed: {
        isCurrentUserSeller() {
            return this.currentUser.id === this.item.seller;
        }
    }
};
</script>

<style scoped>
.container {
    margin-top: 12vh;
    margin-left: 5vw;
}

.item-detail {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.left-side {
    flex: 1;
    width: 50vw;
    margin-right: 20px;
    float: left;
}

.right-side {
    flex: 1;
    align-items: flex-start;
}

.description {
    margin-top: 20px;
}

.price {
    margin-top: 20px;
    font-size: 20px;
    font-weight: bold;
}

#item-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

#chat {
    width: 30px;
    height: 30px;
    float: right;
    cursor: pointer;
}

.user-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 10px;
}
</style>