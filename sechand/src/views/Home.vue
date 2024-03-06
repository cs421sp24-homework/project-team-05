<template>
  <div>
    <Navbar />
    <div class="container">
      <Seach />
      <Dropdown class="buttons" text="Location" @dropdown-click="$emit('showLocation')" emitMethod="Updatelocation"
        :dropdownData="locations"></Dropdown>
      <Cards :cards="cardsData" />
    </div>

  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import Seach from "../components/Seach.vue";
import Dropdown from "../components/Dropdown.vue";
import Cards from "../components/Cards.vue";
import axios from "axios";


export default {
  components: {
    Navbar,
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
      cardsData: [],
    };
  },
  async created() {
    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    console.log(import.meta.env.VITE_HOST);
    console.log(HTTP_PREFIX);
    try {
      const response = await axios.get(HTTP_PREFIX + 'api/v1/post/Items/all');
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
  },
};
</script>

<style>
.container {
  margin-top: 12vh;
  margin-left: 5vw;
}


.buttons {
  margin-top: 20px;
}
</style>