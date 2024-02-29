<template>
    <div>
        <UserNavbar :currentUser="currentUser" />
        <div class="item-detail">
            <!-- Left side: Image -->
            <div class="left-side">
                <img :src="item.imageUrl" alt="Item Image" style="width: 300px; height: 300px; border-radius: 50%" />
            </div>

            <!-- Right side: Details -->
            <div class="right-side">
                <h2>{{ item.name }}</h2>
                <p>Price: ${{ item.price }}</p>
                <p>Seller: {{ item.displayname }}</p>
                <img :src="item.sellerIcon" alt="Seller Icon" />

                <!-- Description -->
                <div class="description">
                    <h3>Description:</h3>
                    <p>{{ item.description }}</p>
                </div>
                <button v-if="isCurrentUserSeller" @click="editItem">Edit</button>
            </div>
        </div>
    </div>
</template>
  
<script>
import UserNavbar from "@/components/UserNavbar.vue";
import axios from "axios";
export default {

    name: "ShowItem",
    props: {
        currentUser: Object,
        item: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            isCurrentUserSeller: false,
            isLoading: false,
            item: {},
            id: null,
        };
    },
    components: {
        UserNavbar,
    },
    methods: {
        editItem() {
            this.$router.push({ name: 'EditItem', params: { id: this.id } });
        }
    },
    async created() {
        // Check if the current user is the seller of the item
        this.id = this.$route.params.id;

        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/post/Item/${this.id}`);
            console.log(response.data);
            this.item = response.data;
        } catch (error) {
            console.error(error);
        }
        console.log(this.id);
        console.log(this.currentUser.id);
        if (this.currentUser.id === this.item.seller) {
            this.isCurrentUserSeller = true;
        }
    },
};
</script>
  
<style scoped>
.item-detail {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.left-side {
    flex: 1;
    margin-right: 20px;
}

.right-side {
    flex: 2;
}

.description {
    margin-top: 20px;
}
</style>