<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#" @click="goToHome">
        <img src="/icon.jpg" alt="Icon" class="mr-2 icon" />
        Sechand</a>
      <div class="row justify-content-end">
        <div class="col-auto">
          <img :src="this.currentUser.image" alt="User Icon" class="user-icon" @click="profile" />
        </div>
        <div class="col-auto">
          <Button @btn-click="profile" :text="this.currentUser.displayname" color="transparent"></Button>
        </div>
        <div class="col-auto">
          <Button @btn-click="logout" text="Logout" color="red"></Button>
        </div>

      </div>
    </div>
  </nav>
</template>
<script>
import Button from "./Button.vue";
export default {
  name: "UserNavbar",
  // props: {
  //   currentUser: Object,
  // },
  components: {
    Button,
  },
  data() {
    return {
      currentUser: JSON.parse(localStorage.getItem('user'))
    };
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
    logout() {
      // localStorage.removeItem('access_token');
      // localStorage.removeItem('refresh_token');
      localStorage.clear(); // Clears all local storage
      sessionStorage.clear(); // Clears all session storage
      // this.$emit("userLogout", {});
      this.$router.replace({ name: 'Home' });
      // this.$router.push("/")
    }

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