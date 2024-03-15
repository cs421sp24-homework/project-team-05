<template>
  <div>
    <UserNavbar v-if="currentUser" :currentUser="currentUser" @userLogout="userStateChange" />
    <Navbar v-else />
    <div class="container">
      <div class="left">
        <!-- category buttons -->
        <ul class="list-group">
          <li class="list-group-item" @click="UpdateCategory(this.All)">
            All Category
          </li>
          <li v-for="(value, index) in categories" :key="index" class="list-group-item" @click="UpdateCategory(value)">
            {{ value }}
          </li>
        </ul>
      </div>
      <div class="right">
        <Seach :categories="this.categories" @onClick="search" />
        <div class="dropdowns-container">
          <Dropdown class="buttons" text="Location" :dropdownData="this.addrList" @update:selected="UpdateLocation">
          </Dropdown>
          <Dropdown v-if="currentUser" class="buttons" text="Distance" :dropdownData="this.distanceList"
            @update:selected="UpdateDistance">
          </Dropdown>
          <div class="dropdown-center buttons">
            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
              aria-expanded="false">
              Price
            </button>
            <div class="dropdown-menu dropdown-menu-dark">
              <div class="dropdown-item">
                <PriceRange @update:min-max="UpdateMinMax"></PriceRange>
              </div>
            </div>
          </div>
          <!-- <div class="col-9 text-end">
            <Button @btn-click="search" text="Apply" color="lightblue" id="apply"></Button>
          </div> -->
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
import Navbar from "@/components/Navbar.vue";
import axios from "axios";
export default {
  name: "Home",
  props: {
    addrList: Array,
    categories: Array,
    currentUser: Object,
  },
  components: {
    UserNavbar,
    Seach,
    Dropdown,
    Cards,
    Button,
    PriceRange,
    Navbar,
  },
  data() {
    return {
      All: "all",
      distanceList: ["< 1mile", "< 3mile", "< 5miles", "< 10miles"],
      isLoading: false,
      cardsData: [],
      input: "",
      cate: "",
      filters: { locations: [], distance: [], min: "-1", max: "-1" },
    };
  },
  async created() {
    console.log("logined", this.addrList);
    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    try {
      if (this.currentUser) {
        const accessToken = localStorage.getItem("access_token");
        const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/all", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.cardsData = response.data;
      } else {
        const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/all");
        this.cardsData = response.data;
      }
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    userStateChange() {
      this.$emit("userStateChange", {});
    },
    async search(payload) {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      try {
        // console.log(payload.cate)
        const formData = new FormData();
        formData.append("desc_text", payload.input);
        formData.append("category", payload.cate);
        formData.append("lowest_price", this.filters.min);
        formData.append("highest_price", this.filters.max);
        const loc_array = this.filters.locations
        loc_array.forEach((item, index) => {
          formData.append("location", item);
        });
        const response = await axios.post(
          HTTP_PREFIX + "api/v1/post/Items/Search",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log("Form submitted successfully:", response.data);
        this.cardsData = response.data;
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    },
    // async applyFilter() {
    //   const HTTP_PREFIX = import.meta.env.VITE_HOST;
    //   try {
    //     const formData = new FormData();
    //     formData.append("desc_text", "");
    //     formData.append("lowest_price", this.filters.min);
    //     formData.append("highest_price", this.filters.max);
    //     const loc_array = this.filters.locations
    //     loc_array.forEach((item, index) => {
    //       formData.append("locations", item);
    //     });
    //     const response = await axios.post(
    //       HTTP_PREFIX + "api/v1/post/Items/Search",
    //       formData,
    //       {
    //         headers: {
    //           "Content-Type": "multipart/form-data",
    //         },
    //       }
    //     );
    //     console.log("Form submitted successfully:", response.data);
    //     this.cardsData = response.data;
    //   } catch (error) {
    //     console.error("Error submitting form:", error);
    //   }
    // },
    async UpdateCategory(category) {
      console.log("update category", category);
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      try {
        const formData = new FormData();
        formData.append("category", category);
        const response = await axios.post(
          HTTP_PREFIX + "api/v1/post/Items/Browse",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log("Form submitted successfully:", response.data);
        this.cardsData = response.data;
      } catch (error) {
        console.error("Error submitting form:", error);
      }
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
      this.filters.min = min.toString();
      this.filters.max = max.toString();
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
  /* justify-content: space-between; */
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

#apply {
  border: 1px solid #00cc66;
  margin-top: 2.5vh;
  margin-left: 10px;
  height: 4.6vh;
  width: 7.5vw;
}
</style>