<template>
    <!-- TODO nav bar -->
    <div id="left"></div>
    <div id="right"></div>

    <div id="main">
        <div>
            <h1 id="title">My Profile</h1>
        </div>

        <div class="mb-3">
            <label class="form-label" style="text-align: left;">Nick Name</label>
            <input type="text" class="form-control" placeholder="Enter your nick name" @input="initState" :disabled="!isEditting" v-model="show_uname"/>
            <div class="form-text" style="font-size: small;" :style="{ visibility: isEditting ? 'visible' : 'hidden' }">
                Your nick name must be 6-16 characters long.
            </div>
        </div>
        
        <div class="mb-3">
            <label class="form-label" style="text-align: left; margin-top: 3%;">Closest Address</label>
            <select v-model="show_addr" class="form-select form-control" :disabled="!isEditting" @input="initState">
                <option disabled>Select the closest address to you...</option>
                <option v-for="(item, index) of addrList">{{ item }}</option>
            </select>
        </div>
        
        <label class="form-label" style="text-align: left; margin-top: 5%;">USA Mobile Phone Number</label>
        <div class="input-group mb-3">
            <select v-model="prefix" class="form-select form-control" disabled>
                <option disabled>+1</option>
            </select>
            <input type="text" class="form-control" placeholder="Enter your number" style="width: 11vw;" @input="initState" :disabled="!isEditting" v-model="show_mobile"/>
            <input type="text" class="form-control" placeholder="Visible to all users" style="width: 9.5vw;" disabled/>
            <div class="input-group-text">
                <input class="form-check-input mt-0" type="checkbox" v-model="visible" aria-label="Checkbox for following text input" :disabled="!isEditting">
            </div>
        </div>

        <div style="color: red; font-size: 0.9vw; text-align: center;">
            <div :style="{ visibility: state > 0 ? 'visible' : 'hidden' }">{{ err_text }}</div>
        </div>

        <div style="text-align: center; margin-top: 4%; margin-bottom: 2%;">
            <button v-if="!isEditting" class="btn btn-primary" style="width: 20%;" @click="toEdit">Edit</button>
            <button v-if="isEditting" class="btn btn-secondary" style="margin-right:15%; width: 20%;" @click="exitCancel">Cancel</button>
            <button v-if="isEditting" class="btn btn-primary" style="width: 20%;" @click="toSave">Save</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
// TODO import nav bar

export default {
    data(){
        return {
            uname: "IsaacXU",
            addrList: ["addr1", "addr2","addr3","addr4", ],
            addr: "addr1",
            mobile: "1234567890",
            prefix: "+1",
            visible: false,
            isEditting: false,
            show_uname: "",
            show_addr: "",
            show_mobile: "",
            show_visible: null,
            state: 0,
        }
    },

    computed:{
        err_text(){
            if (this.state == 1) return "Invalid length of nick name!";
            else if (this.state == 2) return "Invalid US mobile number!";
            else if (this.state == 3) return "Unexpected error. Please try again later.";
            return "no msg"
        },
    },

    methods: {
        exitCancel(){
            this.show_visible = this.visible;
            this.show_mobile = this.mobile;
            this.show_uname = this.uname;
            this.show_addr = this.addr;
            this.isEditting = false;
            this.state = 0;
        },

        toSave() {
            if (this.show_uname.length > 16 || this.show_uname.length < 6) this.state = 1;
            else if (this.show_mobile.length != 10 || isNaN(Number(this.show_mobile, 10))) this.state = 2;
            else {
                // TODO http request -- submit new info
                // if success
                this.visible = this.show_visible;
                this.mobile = this.show_mobile;
                this.uname = this.show_uname;
                this.addr = this.show_addr;
                this.isEditting = false;
                // if failed
                // this.state = 3; // network issue
                // this.show_visible = this.visible;
                // this.show_mobile = this.mobile;
                // this.show_uname = this.uname;
                // this.show_addr = this.addr;
    
            }
        },

        toEdit() {
            this.isEditting = true;
        },
    },

    mounted (){
        // TODO http request -- get profile
        this.show_uname = this.uname;
        this.show_addr  = this.addr;
        this.show_mobile= this.mobile;
        this.visible    = this.visible;
    }
}

</script>

<style scoped>

#left{
    float: left;
    width: 30vw;
    height: 100vh;
    background-color: #007bff;  
}

#right{
    float: right;
    width: 30vw;
    height: 100vh;
    background-color: #007bff;  
}


#main {
    float: inline-start;
    width: 30vw;
    margin-left: 5vw;
    user-select: none;
}

#title{
    font-size: 3vw;
    font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    margin-top: 10vh;
    margin-bottom: 8vh;
}

</style>