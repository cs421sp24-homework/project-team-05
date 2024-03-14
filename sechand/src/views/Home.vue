<template>
  <div>
    <Navbar />
    <div class="container">
      <Seach />
      <Dropdown
        class="buttons"
        text="Location"
        @dropdown-click="$emit('showLocation')"
        emitMethod="Updatelocation"
        :dropdownData="locations"
      ></Dropdown>
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
    const currUser = JSON.parse(localStorage.getItem('user'));
    if (currUser) {
        this.$router.push('/userhome');
    }
    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    try {
      const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/all");
      this.cardsData = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async UpdateLocation(item) {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      try {
        const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/all");
        this.cardsData = response.data;
      } catch (error) {
        console.error(error);
      }
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