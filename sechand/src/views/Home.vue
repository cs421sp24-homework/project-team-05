<template>
  <div class="container">
    <Navbar @login="login" @signup="signup" />
    <Seach />
    <Dropdown
      text="Location"
      @dropdown-click="$emit('showLocation')"
      emitMethod="Updatelocation"
      :dropdownData="locations"
    ></Dropdown>
    <Cards :cards="cardsData" @item-detail="handleItemDetail" />
  </div>
</template>
<script>
import Navbar from "../components/Navbar.vue";
import HelloWorld from "../components/HelloWorld.vue";
import Seach from "../components/Seach.vue";
import Dropdown from "../components/Dropdown.vue";
import Cards from "../components/Cards.vue";
export default {
  components: {
    Navbar,
    HelloWorld,
    Seach,
    Dropdown,
    Cards,
  },
  data() {
    return {
      locations: [
        { id: 1, label: "Location 1", link: "#" },
        { id: 2, label: "Location 2", link: "#" },
        { id: 3, label: "Location 3", link: "#" },
      ],
      cardsData: [
        {
          id: 1,
          title: "Title 1",
          text: "Text for card 1 Text for card 1 Text for card 1 Text for card 1 Text for card 1 Text for card 1 Text for card 1 Text for card 1Text for card 1",
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
    login() {
      // this.$router.push("/login");
      console.log("login");
    },
    signup() {
      // this.$router.push("/signup");
      console.log("signup");
    },
    showLocation() {
      console.log("showLocation");
    },
    // async showLocation() {
    //   try {
    //     // Simulating an asynchronous fetch
    //     const response = await fetch('/api/locations');
    //     if (!response.ok) {
    //       throw new Error('Network response was not ok');
    //     }
    //     const data = await response.json();
    //     this.locations = data;
    //   } catch (error) {
    //     console.error('Error fetching locations:', error);
    //   }
    // },
    UpdateLocation(item) {
      console.log(item);
    },
    handleItemDetail(cardId) {
      console.log("Detail for card:", cardId);
      // Handle the detail view for the clicked card
    },
  },
};
</script>