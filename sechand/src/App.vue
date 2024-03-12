<template>
    <!-- <router-view @userLogin="userLogin" 
                 @userLogout="logout"
                 :currentUser="user"
                 :addrList="addrList"
                 :token="token"></router-view> -->
    <router-view @userLogin="userLogin" @userLogout="logout" :addrList="addrList" :logined="login"
        @updateUser="updateUser"></router-view>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            login: false,
            user: null,
            token: null,
            addrList: ["nine east", "Social"],
        }
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
        }
    },

    async mounted() {
        const HTTP_PREFIX = import.meta.env.VITE_HOST;
        await axios.get(HTTP_PREFIX + 'user/init-info/')
            .then(response => {
                this.addrList = response.data.addrList;
            })
            .catch(error => {
                // console.error('Error fetching data:', error);
                window.alert("Failed to fetch address.");
            })
    }
}
</script>
