<template>
    <div>
        <UserNavbar :icon_src="icon_src" :Username="Username" />
        <div class="item-detail">
            <!-- Left side: Image -->
            <div class="left-side">
                <img :src="item.imageUrl" alt="Item Image" style="width: 300px; height: 300px; border-radius: 50%" />
            </div>

            <!-- Right side: Details -->
            <div class="right-side">
                <h2>{{ item.name }}</h2>
                <p>Price: ${{ item.price }}</p>
                <p>Seller: {{ item.seller }}</p>
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
export default {

    name: "ShowItem",
    props: {

        item: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            isCurrentUserSeller: false,
            icon_src: "/icon.jpg",
            Username: "User",
            isLoading: false,
            item: {
                id: 1,
                name: "Title 1",
                description: "Text for card 1",
                imageUrl: "/icon.jpg",
                seller: "Seller 1",
                sellerid: 1,
                price: 100,
            },
        };
    },
    components: {
        UserNavbar,
    },
    methods: {
        editItem() {
            this.$router.push("/postitem/" + this.item.id);
        }
    },
    created() {
        // Check if the current user is the seller of the item
        if (this.Username === this.item.seller) {
            this.isCurrentUserSeller = true;
        }
    }


    // mounted() {
    //     this.isLoading = true;
    //     axios.get('/api/items') // Assuming your backend API endpoint is '/api/items'
    //         .then(response => {
    //             this.items = response.data;
    //         })
    //         .catch(error => {
    //             console.error('Error fetching data:', error);
    //         })
    //         .finally(() => {
    //             this.isLoading = false;
    //         });
    // }
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