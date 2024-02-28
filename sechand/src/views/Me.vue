<template>
  <div class="container">
    <UserNavbar
      :icon_src="icon_src"
      :Username="Username"
      @profile="openUserProfile"
    />
    <div class="row">
      <div class="col-12">
        <h1>My Profile</h1>
      </div>
    </div>
    <!-- User profile information -->
    <div class="row mb-3">
      <div class="col-12">
        <div class="d-flex align-items-center">
          <img
            :src="icon_src"
            alt="User Icon"
            class="me-3"
            style="width: 300px; height: 300px; border-radius: 50%"
          />
          <div>
            <p class="mb-1 font-large-vh font-large-vw">{{ Username }}</p>
            <!-- Increase font size -->
            <p class="mb-0 font-large-vh font-large-vw">{{ location }}</p>
            <!-- Increase font size -->
          </div>
        </div>
        <Button
          class="edit-profile-btn"
          text="Edit Profile"
          color="transparent"
          @click="editProfile"
        >
        </Button>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <h2>My Items</h2>
        <div class="card-container">
          <Cards :cards="cardsData" @item-detail="handleItemDetail" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Cards from "@/components/Cards.vue";
import Button from "@/components/Button.vue";
export default {
  name: "Me",
  components: {
    UserNavbar,
    Cards,
    Button,
  },
  data() {
    return {
      icon_src: "/icon.jpg",
      Username: "User",
      location: "Location",
      cardsData: [
        {
          id: 1,
          title: "Title 1",
          text: "Text for card 1",
          imageUrl: "/icon.jpg",
          seller: "Seller 1",
        },
        {
          id: 2,
          title: "Title 2",
          text: "Text for card 2",
          imageUrl: "image2.jpg",
        },
        {
          id: 3,
          title: "Title 2",
          text: "Text for card 2",
          imageUrl: "image2.jpg",
        },
        {
          id: 4,
          title: "Title 2",
          text: "Text for card 2",
          imageUrl: "image2.jpg",
        },
        {
          id: 5,
          title: "Title 2",
          text: "Text for card 2",
          imageUrl: "image2.jpg",
        },
        {
          id: 6,
          title: "Title 2",
          text: "Text for card 2",
          imageUrl: "image2.jpg",
        },
      ],
    };
  },
  methods: {
    handleItemDetail(id) {
      console.log("Item detail", id);
    },
    openUserProfile() {
      console.log("Open user profile");
    },
    editProfile() {
      // this.$router.push("/profile");
      console.log("Edit profile");
    },
  },
};
</script>
<style scoped>
/* Add scoped styles if needed */
.font-large-vh {
  font-size: 3vh; /* Font size will be 10% of the viewport height */
}

.font-large-vw {
  font-size: 3vw; /* Font size will be 10% of the viewport width */
}
.card-container {
  overflow-x: auto; /* Enable horizontal scrollbar */
  white-space: nowrap; /* Prevent card items from wrapping */
}

.card {
  display: inline-block; /* Display cards in one row */
  margin-right: 10px; /* Add margin between cards */
}
.edit-profile-btn {
  background: none; /* No background color */
  border: none; /* No border */
  color: inherit; /* Inherit text color */
  text-decoration: underline; /* Underline text */
  cursor: pointer; /* Change cursor to pointer on hover */
  outline: none; /* Remove default focus outline */
}

.edit-profile-btn:hover {
  color: #555; /* Change text color on hover */
}
</style>