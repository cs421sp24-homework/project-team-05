<template>
  <nav class="navbar navbar-expand-sm fixed-top">
    <div class="navbar-elements">
      <a class="navbar-brand" href="#" @click="goToHome">
        <img src="../assets/logo_temp.svg" alt="Icon" class="icon" />
        Sechand</a>
      <div class="navbar-nav ml-auto">
        <div class="nav-item">
          <img :src="currentUser.image" class="user-icon" @click="profile" />
        </div>
        <div class="nav-item">
          <Button @btn-click="profile" :text="currentUser.displayname" color="transparent"></Button>
        </div>
        <div class="nav-item">
          <Button class="logout-btn" @btn-click="logout" text="Logout" color="danger"></Button>
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
    currentUser: Object,
  },
  components: {
    Button,
  },
  methods: {
    profile() {
      this.$router.push("/me");
    },
    goToHome() {
      this.$router.push("/userhome");
    },
    logout() {
      localStorage.clear(); // Clear all storage
      this.$emit("userLogout", {});
      this.$router.replace({ name: 'Home' });
    }
  }
};
</script>

<style>
.navbar {
  background-color: #98a497;
  /* padding-top: 15px; */
  /* Increase top padding */
  /* padding-bottom: 20px; */
  /* Increase bottom padding */
}

.navbar-elements {
  margin-left: 5vw;
  margin-right: 5vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
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

.user-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
}

.user-icon:hover {
  opacity: 0.5;
}

.logout-btn {
  padding: 5px 10px;
  border-radius: 5px;
  /* cursor: pointer; */
}
</style>
