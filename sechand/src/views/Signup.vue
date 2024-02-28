<template>
<!-- TODO nav bar -->
    <div :class="{ 'blurred': isVerifying }" style="user-select: none;">
        <h1 id="title">Sign up to explore SecHand!</h1>

        <div id="left">
            <label class="form-label input-left" style="text-align: left;">JHED</label>
            <div class="input-group mb-3 input-left">
                <input v-model="jhed" type="text" class="form-control" placeholder="Enter your JHED" style="width: 50%;" @input="initState" :disabled="isVerifying">
                <select v-model="suffix" id="suffix" class="form-select form-control" :disabled="isVerifying">
                    <option>@jh.edu</option>
                    <option>@jhu.edu</option>
                </select>
            </div>

            <div class="mb-3 input-left">
                <label class="form-label" style="text-align: left; margin-top: 9%;">Set your Password</label>
                <input type="password" class="form-control" placeholder="Enter your password" @input="initState" :disabled="isVerifying" v-model="password"/>
                <div class="form-text" style="font-size: small;">
                    Your password must be 8-20 characters long.
                </div>
            </div>

            <div class="mb-3 input-left">
                <label class="form-label" style="text-align: left; margin-top: 4%;">Repeat Password</label>
                <input type="password" class="form-control" placeholder="Reapeat your password" @input="initState" :disabled="isVerifying" v-model="repeat"/>
            </div>

        </div>

        <div id="right">

            <div class="mb-3 input-right">
                <label class="form-label" style="text-align: left;">Nick Name</label>
                <input type="text" class="form-control" placeholder="Enter your nick name" @input="initState" :disabled="isVerifying" v-model="uname"/>
                <div class="form-text" style="font-size: small;">
                    Your nick name must be 6-16 characters long.
                </div>
            </div>
            
            <div class="mb-3 input-right">
                <label class="form-label" style="text-align: left; margin-top: 4%;">Closest Address</label>
                <select v-model="addr" class="form-select form-control" :disabled="isVerifying" @input="initState">
                    <option disabled>Select the closest address to you...</option>
                    <option v-for="(item, index) of addrList">{{ item }}</option>
                </select>
            </div>
            
            <label class="form-label input-right" style="text-align: left; margin-top: 5%;">USA Mobile Phone Number</label>
            <div class="input-group mb-3 input-right">
                <select v-model="prefix" class="form-select form-control" disabled>
                    <option disabled>+1</option>
                </select>
                <input type="text" class="form-control" placeholder="Enter your number" style="width: 11vw;" @input="initState" :disabled="isVerifying" v-model="mobile"/>
                <input type="text" class="form-control" placeholder="Visible to all users" style="width: 9.5vw;" disabled/>
                <div class="input-group-text">
                    <input class="form-check-input mt-0" type="checkbox" v-model="visible" aria-label="Checkbox for following text input" :disabled="isVerifying">
                </div>
            </div>
        </div>

        <div id="bottom">
            <div style="color: red; font-size: 1vw; margin-bottom: 3vh;">
                <div :style="{ visibility: state > 0 ? 'visible' : 'hidden' }">{{ err_text }}</div>
            </div>

            <button v-if="counting" class="btn btn-primary" style="width: 20vw;" @click="toVerify" disabled>Resend Verification in {{ countDownTime }} seconds</button>
            <button v-else class="btn btn-primary" style="width: 20vw;" @click="toVerify" :disabled="isVerifying">Verify JHED by E-mail</button>
        </div>
    </div>

    <div class="show toast" v-show="isVerifying">
        <div class="toast-header">
            <img src="/logo.jpg" class="rounded me-2" alt="...">
            <strong class="me-auto">Verifying JHED</strong>
            <small>{{ jhed }}</small>
            <!-- <button type="button" class="btn-close"></button> -->
        </div>
        <div class="toast-body">
            <div style="text-align: center; font-size: 1.5vw;">
                A verification code has been sent to:
                <p style="margin-top: 2vh; font-size: 2vw; color: #007bff; font-weight: bold;">{{ jhed + suffix }}</p>
            </div>

            <div class="mb-3 input-toast">
                <label class="form-label" style="margin-top: 4%; margin-bottom: 5%;">Enter the 6-digit Verification Code:</label>
                <div>
                    <CodeContainer ref="code" @ivcode="getVer" @backspace="initToast"/>
                </div>
            </div>

            <div style="color: red; font-size: 0.9vw; text-align: center;">
                <div :style="{ visibility: toast_err > 0 ? 'visible' : 'hidden' }">{{ toast_err_text }}</div>
            </div>

            <div style="text-align: center; margin-top: 2%; margin-bottom: 2%;">
                <button class="btn btn-secondary" style="margin-right:8%; width: 15%;" @click="exitVerify">Cancel</button>
                <button class="btn btn-primary" style="width: 15%;" @click="trySignup">Sign up</button>
            </div>

        </div>
    </div>

</template>

<script>
// TODO import nav bar
import axios from 'axios';
import CodeContainer from '@/components/CodeContainer.vue';
    export default {
        data(){
            return {
                jhed: "",
                suffix: "@jh.edu",
                password:"",
                repeat:"",
                addr:"Select the closest address to you...",
                addrList: ["addr1", "addr2", "addr3", "addr4"],
                uname:"",
                prefix: "+1",
                mobile: "",
                visible: true,
                state: 0,
                isVerifying: false,
                verCode: "",
                toast_err: 0,
                countDownTime: 0,
                counting: false
            }
        },

        computed:{
            err_text(){
                if (this.state == 1) return "Empty JHED!";
                else if (this.state == 2) return "Invalid length of password!";
                else if (this.state == 3) return "Passwords do not match!";
                else if (this.state == 4) return "Invalid length of nick name!";
                else if (this.state == 5) return "Please choose an address!";
                else if (this.state == 6) return "Invalid US mobile number!";
                // TODO err msg -- registered JHED
                // TODO err msg -- network issue
                return "no msg"
            },

            toast_err_text() {
                if (this.toast_err == 1) return "Please fill in the 6-digit verification code!";
                // TODO err msg -- incorrect V. code
                // TODO err msg -- network issue
                return "no msg"
            }
        },

        methods:{
            toVerify(){
                if (this.jhed.length == 0) this.state = 1;
                else if (this.password.length > 20 || this.password.length < 8) this.state = 2;
                else if (this.password != this.repeat) this.state = 3;
                else if (this.uname.length > 16 || this.uname.length < 6) this.state = 4;
                else if (this.addr == "Select the closest address to you...") this.state = 5;
                else if (this.mobile.length != 10 || isNaN(Number(this.mobile, 10))) this.state = 6;
                else {
                    // TODO http request -- check registered & send email
                    // show Toast
                    this.startCountDown(10);
                    this.isVerifying = true;
                }
            },
            initState(){
                this.state = 0;
            },
            // on the toast
            exitVerify(){
                this.$refs.code.clear();
                this.isVerifying = false;
            },
            getVer(code){
                this.verCode = code;
            },
            trySignup(){
                if (this.verCode.length == 0) this.toast_err = 1;
                // TODO http request -- verify code & signup
                else this.toast_err = 0;
            },
            initToast() {
                this.toast_err = 0;
                this.verCode = "";
            },
            startCountDown(time) {
                this.counting = true;
                this.countDownTime = time;
                const timer = setInterval(() => {
                    this.countDownTime--;
                    if (this.countDownTime <= 0) {
                        clearInterval(timer);
                        this.counting = false;
                    }
                }, 1000);
            }
        },

        components:{
            CodeContainer
        },
    }
</script>

<style scoped>


#title{
    text-align: center;
    margin-top: 10vh;
    margin-bottom: 10vh;
}

.blurred {
  filter: blur(5px);
}

#left{
    float: left;
    height: 45vh;
    width: 50%;
    border-right: 1px black solid;
}

#right{
    float: right;
    height: 45vh;
    width: 50%;
}

.input-left{
    width: 60%;
    margin-left: 30%;
    font-size: 1.2vw;
}
.input-right{
    width: 60%;
    margin-left: 10%;
    font-size: 1.2vw;
}

#suffix{
    background-color: rgb(239, 239, 239);
}

#bottom{
    margin-top: 57vh;
    text-align: center;
}

.input-toast{
    width: 80%;
    margin-left: 10%;
    font-size: 1.2vw;
    text-align: center;
}

.toast {
    width: 40%;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>