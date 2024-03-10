<template>
  <div>
    <UserNavbar />
    <div class="contain" :key="componentKey">
      <div class="row">
        <div class="col-12">
          <h1>My Profile</h1>
        </div>
      </div>
      <!-- User profile information -->
      <div class="row mb-3">
        <div class="col-12">
          <div class="d-flex align-items-center">
            <img :src="currentUser.image" alt="User Icon" class="me-3 profile-image"
              style="width: 150px; height: 150px; border-radius: 50%" />
            <div>
              <p class="mb-1 font-large-vh font-large-vw profile-name">{{ this.currentUser.displayname }}</p>
              <!-- Increase font size -->
              <p class="mb-0 font-large-vh font-large-vw profile-address">{{ this.currentUser.address.name }}</p>
              <!-- Increase font size -->
            </div>
          </div>
          <Button class="edit-profile-btn" text="My Profile" color="transparent" @click="editProfile">
          </Button>
        </div>
      </div>
      <!-- Segment -->
      <div class="row">
        <div class="col-12">
          <hr class="segment">
        </div>
      </div>
      <div class="row">
        <div class="row">
          <div class="col-6">
            <h2>My Items</h2>
          </div>
          <div class="col-6 text-end">
            <Button class="new-post-btn" text="New Post" color="green" @click="newPost"></Button>
          </div>
        </div>

        <div class="card-container">
          <Cards :cards="postCardsData" @item-detail="handleItemDetail" />
        </div>
      </div>

      <!-- Segment -->
      <div class="row">
        <div class="col-12">
          <hr class="segment">
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
  </div>
</template>

<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Cards from "@/components/Cards.vue";
import Button from "@/components/Button.vue";
import axios from "axios";

export default {
  name: "Me",
  // props: {
  //   currentUser: Object,
  // },
  components: {
    UserNavbar,
    Cards,
    Button,
  },
  data() {
    return {
      componentKey: 0,
      postCardsData: [],
      historyCardsData: [],
      currentUser: JSON.parse(localStorage.getItem('user')),
      // imageUrl: ''
    };
  },
  async created() {
    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    // console.log("11111", import.meta.env.VITE_LOCAL_HOST);
    // this.imageUrl = HTTP_PREFIX + this.currentUser.image;
    // console.log("image url", this.imageUrl);
    this.componentKey += 1; // Change key value to trigger rerender
    console.log("Me page created", this.componentKey);
    try {
      const accessToken = localStorage.getItem('access_token');
      const response = await axios.get(HTTP_PREFIX + 'api/v1/post/UserItems/all', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        },
      });
      this.postCardsData = response.data;
    } catch (error) {
      console.error(error);
    }
    // history card data
    try {
      const accessToken = localStorage.getItem('access_token');
      const response = await axios.get(HTTP_PREFIX + 'api/v1/post/UserItems/all', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        },
      });
      this.historyCardsData = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    forceRerender() {
      this.$forceUpdate(); // Call forceUpdate to trigger rerender
    },
    handleItemDetail(id) {
      console.log("Item detail", id);
    },
    editProfile() {
      this.$router.push("/profile");
      console.log("Edit profile");
    },
    newPost() {
      this.$router.push("/postitem");
    },
  },
};
</script>

<style scoped>
.contain {
  margin-top: 12vh;
  margin-left: 5vw;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.profile-name {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.profile-address {
  font-size: 16px;
  color: #666;
}

.edit-profile-btn {
  background: none;
  border: none;
  color: #007bff;
  font-size: 16px;
  cursor: pointer;
  text-decoration: underline;
  outline: none;
}

.edit-profile-btn:hover {
  color: #0056b3;
}

.new-post-btn {
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.new-post-btn:hover {
  background-color: #218838;
  cursor: pointer;
}

.segment {
  border-top: 1px solid #ddd;
}

.card-container {
  overflow-x: auto;
  white-space: wrap;
}

.card {
  display: inline-block;
  margin-right: 10px;
}
</style>
