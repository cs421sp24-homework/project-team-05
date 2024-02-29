<template>
    <router-view @userLogin="userLogin" :currentUser="user"></router-view>
</template>

<script>
    export default {
        data(){
            return {
                login: false,
                user: null,
            }
        },

        methods:{
            userLogin(data){
                this.login = true;
                this.user = data;
            }
        },
    }
</script>