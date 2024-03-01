<template>
  <div>
    <UserNavbar :currentUser="currentUser" />
    <Seach />
    <Dropdown text="Location" @dropdown-click="$emit('showLocation')" emitMethod="Updatelocation"
      :dropdownData="locations"></Dropdown>
    <Cards :cards="cardsData" @item-detail="handleItemDetail" />
  </div>
</template>
<script>
import UserNavbar from "../components/UserNavbar.vue";
import Seach from "../components/Seach.vue";
import Dropdown from "../components/Dropdown.vue";
import Cards from "../components/Cards.vue";
import axios from "axios";
export default {
  name: "UserHome",
  props: {
    currentUser: Object,
  },
  components: {
    UserNavbar,
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
      isLoading: false,
      cardsData: [],
    };
  },
  async created() {
    try {
      const accessToken = localStorage.getItem('access_token');
      const response = await axios.get('http://127.0.0.1:8000/api/v1/post/Items/all', {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
      });
      this.cardsData = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {

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