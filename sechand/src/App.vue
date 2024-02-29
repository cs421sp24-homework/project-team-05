<template>
  <router-view :currentUser="user"></router-view>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
export default {
  components: {
    HelloWorld,
  },
  props: {
    icon_src: String,
    Username: String,
  },
  data() {
    return {
      user: {
        address: null,
        displayname: "",
        email: "zxu129@jh.edu",
        id: 11,
        image: null,
        username: "user",
      },
    };
  },
};
</script>
