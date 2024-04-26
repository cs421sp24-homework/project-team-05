<template>
    <div>
        <UserNavbar v-if="currentUser" :currentUser="this.currentUser" @userLogout="userStateChange" />
        <Navbar v-else />
        <div class="item-detail container">
            <!-- Left side: Image -->
            <div class="left-side">
                <img :src="item.image" alt="Item Image" id="item-img" />
                <div v-if="reviews.reviews.length != 0" style="font-size: 20px; font-weight: bold; padding: 10px;">
                    Seller Reviews:
                </div>
                <div v-for="review in reviews.reviews" :key="review.id" class="review-container">
                    <div class="avatar-info">
                        <img :src="review.buyer_avatar" class="review-image" />
                        <p class="buyer-name">{{ review.buyer_displayname }}</p>
                        <Star :rating="review.rating" :selectable="false" />
                    </div>
                    <p>
                        Bought this item: <i>{{ review.item_name }}</i></p>
                    <div>
                        <p class="review-text">{{ review.review }}</p>
                    </div>
                    <div class="row">
                        <hr class="segment" />
                    </div>
                </div>
            </div>

            <!-- Right side: Details -->
            <div class="right-side">
                <h2>{{ item.name }} </h2>
                <span class="category">{{ item.category }}</span>
                <p class="price">Price: ${{ item.price }}</p>

                <p>
                    <img :src="item.sellerIcon" class="user-icon" />{{ item.displayname }}
                    <Star :rating="reviews.overall_rating" :selectable="false" />
                    <Button id="chat" v-if="currentUser && !isCurrentUserSeller" @click="chat" text="Chat with Seller"
                        color="lightBlue"></Button>
                </p>
                <div class="location">{{ item.sellerLocation }}
                </div>
                <!-- Description -->
                <div class="description">
                    <h5>Description:</h5>
                    <p>{{ item.description }}</p>
                </div>
                <Button id="editBtn" v-if="isCurrentUserSeller" @click="editItem" text="Edit" color="red"></Button>
                <Button id="cllBtn" v-if="currentUser && !isitemCollected" @click="collectItem" text="Collect"
                    color="lightgreen"></Button>
                <Button v-if="currentUser && isitemCollected" @click="unCollectItem" text="Collected"
                    color="orange"></Button>
            </div>
        </div>
    </div>
</template>

<script>
import UserNavbar from "@/components/UserNavbar.vue";
import axios from "axios";
import Button from "@/components/Button.vue";
import Navbar from "@/components/Navbar.vue";
import Star from "@/components/Star.vue";
export default {

    name: "ShowItem",
    props: {
        currentUser: Object,
    },
    data() {
        return {
            // isCurrentUserSeller: true,
            isitemCollected: false,
            isLoading: false,
            item: {},
            id: null,
            reviews: {},
            // currentUser: JSON.parse(localStorage.getItem('user'))
        };
    },
    components: {
        UserNavbar,
        Button,
        Navbar,
        Star
    },
    methods: {
        chat() {
            sessionStorage.setItem("receiver", this.item.seller);
            sessionStorage.setItem("item", this.item.id);
            this.$router.push({ name: 'Chat' });
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
            // console.log(response.data);
            this.item = response.data;
        } catch (error) {
            console.error(error);
        }
        try {
            const response = await axios.get(HTTP_PREFIX + `api/v1/post/Order/Transaction/Review/${this.item.seller}`);
            console.log(response.data);
            this.reviews = response.data;
            // console.log("reviews", this.reviews.overallrating);
        } catch (error) {
            console.error(error);
        }

        if (this.currentUser) {
            if (this.currentUser.id === this.item.seller) {
                this.isCurrentUserSeller = true;
            }
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
        }

    },
    computed: {
        isCurrentUserSeller() {
            if (this.currentUser) {
                return this.currentUser.id === this.item.seller;
            }
            return false;
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

.location {
    font-size: 20px;
    font-style: italic;
    color: #7d7c7c;
}

.loc_label {
    font-weight: bold;
}

.segment {
    width: 100vw;
}

#item-img {
    width: 40vw;
    height: 60vh;
    object-fit: cover;
}

#chat {
    float: right;
    cursor: pointer;
}

.user-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 10px;
}

.category {
    font-size: 15px;
    font-style: italic;
    color: #555353;
}

.review-container {
    margin-left: 1vw;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 20px;
}

.review-image {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 10px;
}


.buyer-name {
    font-weight: bold;
    margin-bottom: 5px;
    margin: 5px;
}

.avatar-info {
    display: flex;
    align-items: center;
}

.review-text {
    margin-top: 5px;
}
</style>