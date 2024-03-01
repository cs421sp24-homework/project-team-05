<template>
  <router-view :currentUser="user"></router-view>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
export default {
  components: {
    HelloWorld,
  },
  data() {
    return {
      user: {
        address: "dwaugduwagdwabuiwgdujwabd",
        displayname: "sbxzx",
        email: "zxu129@jh.edu",
        id: 11,
        image: "/icon.jpg",
        username: "user",
      },
    };
  },
};
</script>
