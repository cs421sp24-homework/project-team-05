<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img src="/icon.jpg" alt="Icon" class="mr-2 icon" @click="goToHome" />
        Sechand</a>
      <div class="row justify-content-end">
        <div class="col-auto">
          <img :src="icon_src" alt="User Icon" class="user-icon" @click="profile" />
        </div>
        <div class="col-auto">
          <Button @btn-click="profile" :text="Username" color="transparent"></Button>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
import Button from "./Button.vue";
export default {
  name: "UserNavbar",
  props: {
    icon_src: String,
    Username: String,
  },
  components: {
    Button,
  },
  methods: {
    profile() {
      this.$router.push("/me");
      console.log("profile");
    },
    goToHome() {
      this.$router.push("/userhome");
      console.log("goToHome");
    },
  }
};
</script>
<style>
.space {
  margin-left: 10px;
  /* Adjust the margin to create space between buttons */
}

.icon {
  width: 30px;
  /* Adjust width as needed */
  height: 30px;
  /* Adjust height as needed */
}

.user-icon {
  width: 30px;
  /* Adjust width as needed */
  height: 30px;
  /* Adjust height as needed */
  cursor: pointer;
}
</style>