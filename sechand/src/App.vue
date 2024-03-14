<template>
  <!-- <router-view @userLogin="userLogin" 
                 @userLogout="logout"
                 :currentUser="user"
                 :addrList="addrList"
                 :token="token"></router-view> -->
  <router-view @userLogin="userLogin" @userLogout="logout" :addrList="addrList" :logined="login"
    :categories="categories" @updateUser="updateUser"></router-view>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      login: false,
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
    userLogin(data) {
      this.login = true;
      console.log("userLogin", this.login);
      // this.user = data.user;
      // this.token = data.token;
    },

    logout() {
      this.login = false;
      // this.user = null;
      // this.token = null;
    },
    updateUser(data) {
      this.user = data;
      console.log("updatedUser", this.user);
    },
  },

  async mounted() {
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
  },
};
</script>
