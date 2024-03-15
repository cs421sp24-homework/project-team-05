<template>
    <UserNavbar :currentUser="this.currentUser" @userLogout="userStateChange" />
    <div class="contain">


        <div id="left"></div>
        <div id="right"></div>

        <div id="main">
            <div>
                <h1 id="title">My Profile</h1>
            </div>

            <div id="content">

                <div id="inputs">
                    <div class="mb-3">
                        <label class="form-label" style="text-align: left;">JHU Email</label>
                        <input type="text" class="form-control" @input="initState" disabled v-model="email" />
                    </div>

                    <div class="mb-3">
                        <label class="form-label" style="text-align: left; margin-top: 3.5vh">Nick Name</label>
                        <input type="text" class="form-control" placeholder="Enter your nick name" @input="initState"
                            :disabled="!isEditting" v-model="show_uname" />
                        <div class="form-text" style="font-size: 0.7vw;"
                            :style="{ visibility: isEditting ? 'visible' : 'hidden' }">
                            Your nick name must be 4-16 characters long.
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label" style="text-align: left; margin-top: 0.7vh;">Closest Address</label>
                        <select v-model="show_addr" class="form-select form-control" :disabled="!isEditting"
                            @input="initState">
                            <option disabled>Select the closest address to you...</option>
                            <option v-for="(item, index) of addrList">{{ item }}</option>
                        </select>
                    </div>

                    <label class="form-label" style="text-align: left; margin-top: 3.5vh;">USA Mobile Phone
                        Number</label>
                    <div class="input-group mb-3">
                        <select v-model="prefix" class="form-select form-control" disabled>
                            <option disabled>+1</option>
                        </select>
                        <input type="text" class="form-control" placeholder="Enter your number" style="width: 8vw;"
                            @input="initState" :disabled="!isEditting" v-model="show_mobile" />
                        <input type="text" class="form-control" placeholder="Visible to all users" style="width: 9.5vw;"
                            disabled />
                        <div class="input-group-text">
                            <input class="form-check-input mt-0" type="checkbox" v-model="show_visible"
                                aria-label="Checkbox for following text input" :disabled="!isEditting">
                        </div>
                    </div>
                </div>

                <div id="avatar">
                    <label class="form-label"
                        style="margin-top: 5vh; margin-bottom: 3vh; font-size: 1.8vw;">Avatar</label>
                    <ImageUploader size="30" :default_src="show_image_url" :edittable="isEditting" @upload="changeImage"
                        style="margin-left: auto; margin-right: auto;" />
                    <div class="form-text" style="font-size: 0.7vw; margin-top: 2vh;"
                        :style="{ visibility: isEditting ? 'visible' : 'hidden' }">
                        Click your avatar to upload a new one
                    </div>
                </div>
            </div>


            <div style="color: red; font-size: 0.9vw; text-align: center;">
                <div :style="{ visibility: state > 0 ? 'visible' : 'hidden' }">{{ err_text }}</div>
            </div>

            <div style="text-align: center; margin-top: 3%;">
                <button v-if="!isEditting" class="btn btn-secondary" style="margin-right:15%; width: 20%;"
                    @click="goBack">Back</button>
                <button v-if="!isEditting" class="btn btn-primary" style="width: 20%;" @click="toEdit">Edit</button>
                <button v-if="isEditting" class="btn btn-secondary" style="margin-right:15%; width: 20%;"
                    @click="exitCancel">Cancel</button>
                <button v-if="isEditting" class="btn btn-primary" style="width: 20%;" @click="toSave">Save</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import UserNavbar from '@/components/UserNavbar.vue';
import ImageUploader from '@/components/ImageUploader.vue';
export default {
    props: {
        currentUser: Object,
    },
    data() {
        return {
            email: "",
            uname: "",
            addr: "",
            mobile: "",
            prefix: "+1",
            visible: false,
            image: null,
            isEditting: false,
            show_uname: "",
            show_addr: "",
            show_mobile: "",
            show_visible: null,
            show_image: null,
            new_image: false,
            state: 0,
            currentUser: JSON.parse(localStorage.getItem('user'))
        }
    },

    computed: {
        err_text() {
            if (this.state == 1) return "Invalid length of nick name!";
            else if (this.state == 2) return "Invalid US mobile number!";
            else if (this.state == 3) return "Unexpected error. Please try again later.";
            return "no msg";
        },
    },

    methods: {
        userStateChange() {
            this.$emit("userStateChange", {});
        },
        exitCancel() {
            this.show_visible = this.visible;
            this.show_mobile = this.mobile;
            this.show_uname = this.uname;
            this.show_addr = this.addr;
            this.show_image = this.image;
            this.isEditting = false;
            this.state = 0;
        },

        toSave() {
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            if (this.show_uname.length > 16 || this.show_uname.length < 4) this.state = 1;
            else if (this.show_mobile.length != 10 || isNaN(Number(this.show_mobile, 10))) this.state = 2;
            else {
                const formData = new FormData();
                formData.append("displayname", this.show_uname);
                formData.append("address", this.show_addr);
                formData.append("phone", this.show_mobile);
                formData.append("is_visible", this.show_visible);
                // console.log("new image", this.show_image);
                // console.log("original image", this.image);
                if (this.new_image) formData.append("image", this.show_image);
                axios.patch(HTTP_PREFIX + 'user/profile/update', formData)
                    .then(response => {
                        console.log(response.data);
                        localStorage.setItem('user', JSON.stringify(response.data));
                        this.visible = this.show_visible;
                        this.mobile = this.show_mobile;
                        this.uname = this.show_uname;
                        this.addr = this.show_addr;
                        this.image = this.show_image;
                        this.isEditting = false;
                    })
                    .catch(error => {
                        console.error('Error fetching data:', error);
                        window.alert("Failed to edit your profile.");
                        this.state = 3; // network issue
                        this.show_visible = this.visible;
                        this.show_mobile = this.mobile;
                        this.show_uname = this.uname;
                        this.show_addr = this.addr;
                        this.show_image = this.image;
                        this.isEditting = false;
                    })
            }
            // console.log("cu", this.currentUser)
        },

        changeImage(data) {
            this.new_image = true;
            this.show_image = data;
        },

        toEdit() {
            this.isEditting = true;
        },

        initState() {
            this.state = 0;
        },
        goBack() {
            this.$router.go(-1);
        }
    },

    props: {
        // currentUser: Object,
        addrList: Array
    },

    computed: {
        show_image_url() {
            try {
                return URL.createObjectURL(this.show_image);
            }
            catch {
                return this.show_image;
            }
        }
    },

    mounted() {
        const HTTP_PREFIX = import.meta.env.VITE_HOST;
        axios.get(HTTP_PREFIX + 'user/profile/')
            .then(response => {
                console.log(response.data);
                this.email = response.data.email;
                this.uname = response.data.displayname;
                this.addr = response.data.address.name;
                this.mobile = response.data.phone;
                this.visible = response.data.is_visible;
                this.image = response.data.image;
                this.show_uname = this.uname;
                this.show_addr = this.addr;
                this.show_mobile = this.mobile;
                this.show_visible = this.visible;
                this.show_image = this.image;
                localStorage.setItem('user', JSON.stringify(response.data));
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                window.alert("Failed to get your profile.");
                this.$router.push('/me');
            })

    },

    components: {
        UserNavbar,
        ImageUploader
    },
}

</script>

<style scoped>
.contain {
    margin-top: 5vh;
}

#left {
    float: left;
    width: 20vw;
    height: 95vh;
    background-color: #d8e8fa;
}

#right {
    float: right;
    width: 20vw;
    height: 95vh;
    background-color: #d8e8fa;
}


#main {
    float: inline-start;
    width: 59vw;
    user-select: none;
}

#content {
    height: 57vh;
}

#inputs {
    margin-left: 5vw;
    float: left;
    width: 29vw;
}

#avatar {
    text-align: center;
    float: inline-start;
    width: 25vw;
}

#title {
    font-size: 3.5vw;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    margin-top: 11vh;
    margin-bottom: 5vh;
    margin-left: 5vw;
}

label {
    font-size: 1.3vw;
}

input {
    font-size: 1vw
}

select {
    font-size: 1vw
}

.btn {
    font-size: 1vw;
}
</style>