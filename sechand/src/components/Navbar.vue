<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#" @click="goToHome">
        <img src="/icon.jpg" alt="Icon" class="mr-2 icon" />
        Sechand</a
      >
      <div class="row justify-content-end">
        <div class="col-auto">
          <Button @btn-click="$emit('Login')" text="Login" color="red"></Button>
        </div>
        <div class="col-auto">
          <Button
            @btn-click="$emit('Signup')"
            text="Sign Up"
            color="red"
          ></Button>
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
  methods:{
    goToHome() {
      this.$router.push("/");
      console.log("goToHome");
    },
  },
};
</script>
<style>
.space {
  margin-left: 10px; /* Adjust the margin to create space between buttons */
}
.icon {
  width: 30px; /* Adjust width as needed */
  height: 30px; /* Adjust height as needed */
}
</style>