<template>
    <router-view @userLogin="userLogin" 
                 @logout="logout"
                 :currentUser="user"
                 :addrList="addrList"
                 :token="token"></router-view>
</template>

<script>
import axios from 'axios';
    export default {
        data(){
            return {
                login: false,
                user: null,
                token: null,
                addrList: ["nine east", "Social"],
            }
        },

        methods:{
            userLogin(data){
                this.login = true;
                this.user = data.user;
                this.token = data.token;
            },

            logout(){

            }
        },

        async mounted(){
            await axios.get('http://127.0.0.1:8000/user/init-info')
                .then(response => {
                    console.log(response.data);
                    this.addrList = response.data.addrList;
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    window.alert("Failed to fetch address.");
                })
        }
    }
</script>