<template>
  <div>
    <UserNavbar />
    <div class="container">
      <div class="left">
        <!-- category buttons -->
        <ul class="list-group">
          <li
            v-for="(value, index) in categories"
            :key="index"
            class="list-group-item"
            @click="UpdateCategory(value)"
          >
            {{ value }}
          </li>
        </ul>
      </div>
      <div class="right">
        <Seach :categories="this.categories" />
        <div class="dropdowns-container">
          <Dropdown
            class="buttons"
            text="Location"
            :dropdownData="this.addrList"
            @update:selected="UpdateLocation"
          ></Dropdown>
          <Dropdown
            class="buttons"
            text="Distance"
            :dropdownData="this.distanceList"
            @update:selected="UpdateDistance"
          ></Dropdown>
          <div class="dropdown-center buttons">
            <button
              class="btn btn-secondary dropdown-toggle"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Price
            </button>
            <div class="dropdown-menu dropdown-menu-dark">
              <div class="dropdown-item">
                <PriceRange @update:min-max="UpdateMinMax"></PriceRange>
              </div>
            </div>
          </div>
          <Button
            @btn-click="applyFilter"
            text="Apply"
            color="lightblue"
          ></Button>
        </div>

        <Cards :cards="cardsData" />
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import Seach from "../components/Seach.vue";
import Button from "@/components/Button.vue";
import Dropdown from "../components/Dropdown.vue";
import Cards from "../components/Cards.vue";
import PriceRange from "../components/PriceRange.vue";
import axios from "axios";
export default {
  name: "UserHome",
  props: {
    addrList: Array,
    categories: Array,
  },
  components: {
    UserNavbar,
    Seach,
    Dropdown,
    Cards,
    Button,
    PriceRange,
  },
  data() {
    return {
      distanceList: ["< 1mile", "< 3mile", "< 5miles", "< 10miles"],
      isLoading: false,
      cardsData: [],
      currentUser: JSON.parse(localStorage.getItem("user")),
      filters: { locations: [], distance: [], min: "", max: "" },
    };
  },
  async created() {
    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    try {
      const accessToken = localStorage.getItem("access_token");
      const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/all", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      this.cardsData = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    applyFilter() {
      console.log("apply filter", this.filters);
    },
    UpdateCategory(category) {
      console.log("update category", category);
    },
    UpdateLocation(locations) {
      this.filters.locations = locations;
      console.log("update location", locations);
    },
    UpdateDistance(distance) {
      this.filters.distance = distance;
      console.log("update distance", distance);
    },
    UpdateMinMax({ min, max }) {
      this.filters.min = min;
      this.filters.max = max;
    },
  },
};
</script>

<style>
.left {
  width: 15%;
  height: 100vh;
  float: left;
  margin-right: 1vw;
}
.right {
  width: 80%;
  height: 100vh;
  float: right;
}
.container {
  margin-top: 12vh;
  margin-left: 5vw;
}

.search {
  margin-top: 20px;
}

.buttons {
  margin-top: 20px;
}
.dropdowns-container {
  display: flex;
  justify-content: space-between;
}
.list-group-item {
  background: #333435;
  color: white;
  text-align: center;
  justify-content: center;
  height: 100%;
}
.list-group-item:hover {
  background: #f9f9f9;
  color: black;
  cursor: pointer;
}
</style>