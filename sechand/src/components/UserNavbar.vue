<template>
  <nav class="navbar navbar-expand-sm fixed-top">
    <div class="navbar-elements">
      <a class="navbar-brand" href="#" @click="goToHome">
        <img src="../assets/logo_temp.svg" alt="Icon" class="icon" id="sechand-icon" />
        Sechand</a>
      <div class="navbar-nav ml-auto">
        <div class="nav-item" id="chat-icon">
          <img src="/comment.png" id="chat" @click="chat" />
          <div id="notification" v-if="notification_count > 0">
            {{ notification_count > 99? '···' : notification_count}}
          </div>
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
import { getWebSocketInstance, closeWebSocketInstance } from "@/services/WebSocketManager";
import axios from "axios";
const HTTP_PREFIX = import.meta.env.VITE_HOST;
const accessToken = localStorage.getItem("access_token");
export default {
  data(){
    return{
      notification_count: 0,
    }
  },
  name: "UserNavbar",
  props: {
    currentUser: Object,
  },
  components: {
    Button,
  },
  mounted() {
    // this.getNotification();
    window.addEventListener("getNotification", this.getNotification);
  },
  methods: {
    chat() {
      // this.getNotification();
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
      sessionStorage.clear(); // Clear all session storage
      closeWebSocketInstance(this.currentUser.id);
      this.$emit("userLogout", {});
      console.log("logout", this.currentUser);
    },
    getNotification() {
      const accessToken = localStorage.getItem("access_token");
      axios.get(HTTP_PREFIX + "api/v1/chat/Conversation/notification/total-count",{
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }).then((notification_count) => {
        this.notification_count = notification_count.data.count;
        console.log("total notifications:" + this.notification_count);
      });
    },
    offsetNotification() {
      this.notification_count = 0;
      console.log("offset notification");

    },
  },
  beforeDestroy() {
    window.removeEventListener("getNotification", this.getNotification);
  },
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

#chat-icon{
    position: relative;
    display: inline-block;
    padding: 10px;
}

#notification{
    position: absolute;
    top: 0;
    right: 0;
    background-color: rgb(255, 33, 33);
    color: white;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 700;
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
