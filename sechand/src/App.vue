<template>
  <router-view @userStateChange="userStateChange" :currentUser="currentUser" :addrList="addrList"
    :categories="categories" @updateUser="updateUser"></router-view>
</template>

<script>
import axios from "axios";
import { getWebSocketInstance, closeWebSocketInstance } from '@/services/WebSocketManager';

export default {
  data() {
    return {
      currentUser: null,
      user: null,
      token: null,
      addrList: [],
      categories: [
        "Electronics",
        "Clothing",
        "Furniture",
        "Books",
        "Home Appliances",
        "Sporting Goods",
        "Toys and Games",
        "Beauty and Personal Care",
        "Health and Wellness",
        "Jewelry and Accessories",
        "Automotive",
        "Home Decor",
        "Arts and Crafts",
        "Pet Supplies",
        "Office Supplies",
      ],
    };
  },

  methods: {
    updateUser(data) {
      this.currentUser = JSON.parse(localStorage.getItem("user"));
      console.log("updatedUser", this.user);
    },
    userStateChange() {
      this.currentUser = JSON.parse(localStorage.getItem("user"));
      console.log("APP", this.currentUser);
      if (this.currentUser) {
        getWebSocketInstance(this.currentUser.id);
      }
    },
  },

  async mounted() {
    this.currentUser = JSON.parse(localStorage.getItem("user"));
    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    await axios
      // another get to get category
      .get(HTTP_PREFIX + "user/init-info/")
      .then((response) => {
        console.log(response.data);
        this.addrList = response.data.addrList;
        // console.log(this.addrList);
      })
      .catch((error) => {
        // console.error('Error fetching data:', error);
        window.alert("Failed to fetch address.");
      });
    
      if (this.currentUser) {
        getWebSocketInstance(this.currentUser.id);
      }
  },
  
  beforeDestroy() {
    if (this.currentUser) {
      closeWebSocketInstance(this.currentUser.id);
    }
  },
};

</script>
