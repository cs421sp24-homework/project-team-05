<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container">
      <a class="navbar-brand" href="#" @click="goToHome">
        <img src="../assets/logo_temp.svg" alt="Icon" class="mr-2 icon" />
        Sechand</a>
      <div class="row justify-content-end">
        <div class="col-auto">
          <Button @btn-click="$emit('login')" text="Login" color="transparent"></Button>
        </div>
        <div class="col-auto">
          <Button @btn-click="$emit('signup')" text="Sign Up" color="transparent"></Button>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
import Button from "./Button.vue";
export default {
  name: "Navbar",
  components: {
    Button,
  },
  methods: {
    goToHome() {
      this.$router.push("/");
      console.log("goToHome");
    },
  },
};
</script>
<style>
.navbar {
  background-color: #98a497;
  padding-top: 20px;
  /* Increase top padding */
  padding-bottom: 20px;
  /* Increase bottom padding */
}

.space {
  margin-left: 10px;
  /* Adjust the margin to create space between buttons */
}

.navbar {
  background-color: #98a497;
  padding-top: 20px;
  /* Increase top padding */
  padding-bottom: 20px;
  /* Increase bottom padding */
}

.navbar-brand {
  color: #ffffff;
  /* Text color */
  font-weight: bold;
  font-size: 24px;

  line-height: 1;
}

.navbar-nav {
  display: flex;
  align-items: center;
}

.nav-item {
  margin-left: 10px;
}

.icon {
  width: 40px;
  height: 40px;
}
</style>