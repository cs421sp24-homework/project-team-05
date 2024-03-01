<template>
  <div>
    <UserNavbar :currentUser="currentUser" />
    <div class="row">
      <div class="col-12">
        <h1>My Profile</h1>
      </div>
    </div>
    <!-- User profile information -->
    <div class="row mb-3">
      <div class="col-12">
        <div class="d-flex align-items-center">
          <img :src="this.currentUser.image" alt="User Icon" class="me-3"
            style="width: 300px; height: 300px; border-radius: 50%" />
          <div>
            <p class="mb-1 font-large-vh font-large-vw">{{ this.currentUser.displayname }}</p>
            <!-- Increase font size -->
            <p class="mb-0 font-large-vh font-large-vw">{{ this.currentUser.address }}</p>
            <!-- Increase font size -->
          </div>
        </div>
        <Button class="edit-profile-btn" text="My Profile" color="transparent" @click="editProfile">
        </Button>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <h2>My Items</h2>
        <div class="card-container">
          <Cards :cards="postCardsData" @item-detail="handleItemDetail" />
          <Button text="New Post" color="green" @click="newPost"></Button>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <h2>Order History</h2>
        <div class="card-container">
          <Cards :cards="historyCardsData" @item-detail="handleItemDetail" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Cards from "@/components/Cards.vue";
import Button from "@/components/Button.vue";
import axios from "axios";
export default {
  name: "Me",
  props: {
    currentUser: Object,
  },
  components: {
    UserNavbar,
    Cards,
    Button,
  },
  data() {
    return {
      postCardsData: [],
      historyCardsData: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/post/UserItems/all');
      this.postCardsData = response.data;
    } catch (error) {
      console.error(error);
    }
    // history card data
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/post/UserItems/all');
      this.historyCardsData = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    handleItemDetail(id) {
      console.log("Item detail", id);
    },
    editProfile() {
      // this.$router.push("/profile");
      console.log("Edit profile");
    },
    newPost() {
      this.$router.push("/postitem");
    },
  },
};
</script>
<style scoped>
/* Add scoped styles if needed */
.font-large-vh {
  font-size: 3vh;
  /* Font size will be 10% of the viewport height */
}

.font-large-vw {
  font-size: 3vw;
  /* Font size will be 10% of the viewport width */
}

.card-container {
  overflow-x: auto;
  /* Enable horizontal scrollbar */
  white-space: nowrap;
  /* Prevent card items from wrapping */
}

.card {
  display: inline-block;
  /* Display cards in one row */
  margin-right: 10px;
  /* Add margin between cards */
}

.edit-profile-btn {
  background: none;
  /* No background color */
  border: none;
  /* No border */
  color: inherit;
  /* Inherit text color */
  text-decoration: underline;
  /* Underline text */
  cursor: pointer;
  /* Change cursor to pointer on hover */
  outline: none;
  /* Remove default focus outline */
}

.edit-profile-btn:hover {
  color: #8a1717;
  /* Change text color on hover */
}
</style>