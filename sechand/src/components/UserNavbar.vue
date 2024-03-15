<template>
  <nav class="navbar navbar-expand-sm fixed-top">
    <div class="navbar-elements">
      <a class="navbar-brand" href="#" @click="goToHome">
        <img src="../assets/logo_temp.svg" alt="Icon" class="icon" />
        Sechand</a>
      <div class="navbar-nav ml-auto">
        <div class="nav-item">
          <img src="/comment.png" id="chat" @click="chat" />
        </div>
        <div class="nav-item">
          <img :src="this.currentUser.image" class="user-icon" @click="profile" id="avt" />
        </div>
        <div class="nav-item">
          <Button @btn-click="profile" :text="currentUser.displayname" color="transparent"></Button>
        </div>
        <div class="nav-item">
          <Button class="logout-btn" id="logoutBtn" @btn-click="logout" text="Logout" color="danger"></Button>
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
  created() {
    console.log("UserNavbar", this.currentUser);
  },
  methods: {
    chat() {
      this.$router.push("/chat");
    },
    profile() {
      this.$router.push("/me");
    },
    goToHome() {
      this.$router.push("/");
    },
    logout() {
      this.$router.replace("/");
      localStorage.clear(); // Clear all storage
      this.$emit("userLogout", {});
      console.log("logout", this.currentUser);

    }
  }
};
</script>

<style scoped>
.navbar {
  background-color: #98a497;
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

#chat {
  width: 30px;
  height: 30px;
  cursor: pointer;
}
</style>
