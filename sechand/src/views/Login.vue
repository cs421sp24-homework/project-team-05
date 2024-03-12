<template>
    <div :class="{ 'blurred': isResetting }" style="user-select: none;">
        <div id="left">
            <h1 id="title" @click="toHome">SecHand</h1>
            <img id="logo" src="../assets/logo_temp.svg" />
            <h2 id="slogan"> {This is a slogan This is a slogan This is a slogan This is a slogan} </h2>
        </div>

        <div id="right">
            <legend>
                Login
            </legend>


            <label class="form-label input" style="text-align: left; margin-top: 4%;">JHED</label>
            <div class="input-group mb-3 input">
                <input id="jhed" v-model="jhed" type="text" class="form-control" placeholder="Enter your JHED"
                    style="width: 50%;" @focus="initState" :disabled="isResetting">
                <select v-model="suffix" class="form-select form-control" :disabled="isResetting">
                    <option>@jh.edu</option>
                    <option>@jhu.edu</option>
                </select>
            </div>

            <div class="mb-3 input">
                <label class="form-label" style="text-align: left; margin-top: 4%;">Password</label>
                <input id="pw" type="password" class="form-control" placeholder="Enter your password" v-model="password"
                    @focus="initState" :disabled="isResetting" />
            </div>

            <div style="color: red; font-size: 0.7vw; margin-left: 20%;">
                <div :style="{ visibility: state > 0 ? 'visible' : 'hidden' }">{{ err_text }}</div>
            </div>

            <div style="text-align: center;">
                <button class="underline btn" id="reset_btn" @click="toReset" :disabled="isResetting">
                    Forget password? Reset password!
                </button>
            </div>

            <div style="text-align: center; margin-top: 3%;">
                <button id="logBtn" class="btn btn-primary" style="width: 60%; font-size: 1vw;" @click="tryLogin"
                    :disabled="isResetting">Login</button>
            </div>

            <div style="text-align: center; margin-top: 8%;">
                <button id="toSignUp" class="underline btn" :disabled="isResetting" @click="toSignUp">
                    New to Sechand? Signup!
                </button>
            </div>
        </div>
    </div>

    <div class="show toast" v-show="isResetting">
        <div class="toast-header">
            <img src="/logo.jpg" class="rounded me-2" alt="...">
            <strong class="me-auto">Resetting password</strong>
            <small>Anything</small>
            <!-- <button type="button" class="btn-close"></button> -->
        </div>
        <div class="toast-body">
            <div style="text-align: center; font-size: 1.5vw;">
                A verification code has been sent to:
                <p style="margin-top: 2vh; font-size: 2vw; color: #007bff; font-weight: bold;">{{ jhed + suffix }}</p>
            </div>

            <div class="mb-3 input">
                <label class="form-label" style="text-align: left; margin-top: 4%;">Verification Code</label>
                <div style="text-align: center;">
                    <CodeContainer ref="code" @ivcode="getVer" @backspace="initToast" />
                </div>
            </div>

            <div class="mb-3 input">
                <label class="form-label" style="text-align: left; margin-top: 4%;">New Password</label>
                <input type="password" class="form-control" placeholder="Enter your new password" @input="initTerr"
                    v-model="newPW" />
                <div class="form-text" style="font-size: small;">
                    * 6-20 characters including letters and numbers
                </div>
            </div>

            <div class="mb-3 input">
                <label class="form-label" style="text-align: left; margin-top: 1%;">Repeat Password</label>
                <input type="password" class="form-control" placeholder="Reapeat your password" @input="initTerr"
                    v-model="repPW" />
            </div>

            <div style="color: red; font-size: 0.9vw; margin-left: 20%;">
                <div :style="{ visibility: toast_err > 0 ? 'visible' : 'hidden' }">{{ toast_err_text }}</div>
            </div>

            <div style="text-align: center; margin-top: 2%; margin-bottom: 2%;">
                <button class="btn btn-secondary" style="font-size: 1.2vw; margin-right:8%; width: 15%;"
                    @click="exitReset">Cancel</button>
                <button class="btn btn-primary" style="font-size: 1.2vw; width: 15%;" @click="tryReset">Reset</button>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
import CodeContainer from '@/components/CodeContainer.vue';

export default {
    data() {
        return {
            suffix: "@jh.edu",
            jhed: "",
            password: "",
            state: 0,
            isResetting: false,
            toast_err: 0,
            verCode: "",
            newPW: "",
            repPW: ""
        }
    },

    computed: {
        err_text() {
            if (this.state == 1) return "Empty JHED!";
            else if (this.state == 2) return "Empty password!";
            else if (this.state == 3) return "Unexpected error, please retry later.";
            else if (this.state == 4) return "JHED not registered";
            else if (this.state == 5) return "Incorrect password!";
            else if (this.state == 6) return "Fill in the JHED and suffix to reset the password!";
            else if (this.state == 7) return "Unxpected error. Please retry later.";
            else if (this.state == 8) return "You are trying to log in to a new account. Please log out from current account first.";
            return "no msg";
        },
        toast_err_text() {
            if (this.toast_err == 1) return "Incorrect verification code!";
            else if (this.toast_err == 2) return "Invalid format of the new password";
            else if (this.toast_err == 3) return "Passwords do not match.";
            else if (this.toast_err == 4) return "Please fill in the verification code.";
            else if (this.toast_err == 5) return "The verification code has expired. Please re-verify.";
            else if (this.toast_err == 6) return "Unxpected error. Please retry later.";
            return "no msg";
        }
    },

    methods: {

        async tryLogin() {
            if (this.jhed.length == 0) this.state = 1;
            else if (this.password.length == 0) this.state = 2;
            else if (JSON.parse(localStorage.getItem('user')) && JSON.parse(localStorage.getItem('user')).username != this.jhed.toLowerCase()) this.state = 8;
            else {
                var userInfo = null;
                const HTTP_PREFIX = import.meta.env.VITE_HOST;
                await axios.post(HTTP_PREFIX + 'user/login/', {
                    "username": this.jhed.toLowerCase(),
                    "password": this.password
                })
                .then(async response => {
                    if (!response.data.registered) {
                        console.log("HHHHHHHHHHHHH");
                        this.state = 4;
                    }
                    else if (!response.data.success) {
                        this.state = 5;
                        this.password = "";
                    }
                    else {
                        userInfo = response.data.userInfo;
                        try {
                            const HTTP_PREFIX = import.meta.env.VITE_HOST;
                            const response = await axios.post(HTTP_PREFIX + 'api/token/', {
                                "username": this.jhed.toLowerCase(),
                                "password": this.password
                            });
                            this.$emit('userLogin', {});
                            localStorage.setItem('access_token', response.data.access);
                            localStorage.setItem('refresh_token', response.data.refresh);
                            localStorage.setItem('user', JSON.stringify(userInfo));
                            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
                            console.log(userInfo);
                            this.$router.push('/userhome');
                        } catch (error) {
                            console.error('Login error:', error);
                            this.$emit('cancelLogin', {});
                        }
                    }
                })
                .catch(error => {
                    this.state = 7;
                    console.error('Error fetching data:', error);
                })
                
            }

        },
        toReset() {
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            if (this.jhed.length == 0) this.state = 6;
            else {
                axios.post(HTTP_PREFIX + 'user/forgot-password/', {
                    "email": (this.jhed + this.suffix).toLowerCase()
                })
                    .then(response => {
                        if (!response.data.registered) {
                            this.state = 4;
                        }
                        else {
                            this.state = 0;
                            this.isResetting = true;
                        }
                    })
                    .catch(error => {
                        this.state = 7;
                        console.error('Error fetching data:', error);
                    })

            }
        },
        exitReset() {
            this.newPW = "";
            this.repPW = "";
            this.$refs.code.clear();
            this.isResetting = false;
        },
        getVer(code) {
            this.verCode = code;
        },
        tryReset() {
            const HTTP_PREFIX = import.meta.env.VITE_HOST;
            const lengthRegex = /.{6,20}/
            const digitRegex = /\d/
            const letterRegex = /[a-zA-Z]/

            if (this.verCode.length == 0) this.toast_err = 4;
            else if (!(lengthRegex.test(this.newPW) && digitRegex.test(this.newPW) && letterRegex.test(this.newPW))) this.toast_err = 2;
            else if (this.newPW != this.repPW) this.toast_err = 3;
            else {
                this.toast_err = 0;
                axios.post(HTTP_PREFIX + 'user/reset-password/' + this.jhed, {
                    "code": this.verCode,
                    "new_password": this.newPW
                })
                    .then(response => {
                        if (!response.data.correct) {
                            this.toast_err = 1;
                            this.$refs.code.clear();
                        }
                        else if (response.data.expired) {
                            window.alert("This verification code has expired.");
                            this.password = "";
                            this.exitReset();
                        }
                        else {
                            window.alert("Your password has been reset.");
                            this.password = "";
                            this.exitReset();
                        }
                    })
                    .catch(error => {
                        this.state = 7;
                        console.error('Error fetching data:', error);
                    })
            };
        },
        initToast() {
            this.toast_err = 0;
            this.verCode = "";
        },
        initTerr() {
            this.toast_err = 0;
        },
        initState() {
            this.state = 0;
        },
        toSignUp() {
            this.$router.push('/signup');
        },
        toHome() {
            this.$router.push('/');
        }
    },

    components: {
        CodeContainer
    },

    mounted() {
        var autofill = this.$route.query;
        if (autofill.jhed != undefined) {
            this.jhed = autofill.jhed;
            this.password = autofill.password;
            this.suffix = autofill.suffix;
        }
    }

}
</script>

<style scoped>
.blurred {
    filter: blur(5px);
}

#title {
    margin-top: 3%;
    margin-left: 4%;
    font-family: "Comic Sans MS";
    font-size: 3vw;
    color: #758673;
    user-select: none;
}

#left {
    float: left;
    height: 100vh;
    width: 50%;
    background-color: #d8e8fa;
}

#right {
    float: right;
    height: 100vh;
    width: 50%;
}

#logo {
    width: 50%;
    margin-top: 5vh;
    margin-left: 27%;
    margin-right: 27%;
}

#slogan {
    text-align: center;
    width: 70%;
    margin-top: 8vh;
    margin-left: auto;
    margin-right: auto;
    font-family: "Comic Sans MS";
    font-style: italic;
    font-weight: 250;
    font-size: 2vw;
    user-select: none;
}

.input {
    width: 60%;
    margin-left: 20%;
    font-size: 1.2vw;
}

.form-control {
    font-size: 1vw;
}

.form-select {
    background-color: rgb(215, 216, 216);
}

.underline {
    text-decoration: none;
    margin-left: auto;
    margin-right: auto;
    font-size: 0.8vw;
    user-select: none;
}

.underline:hover {
    text-decoration: underline;
    color: rgb(0, 94, 255);
}

legend {
    font-family: "rush Script";
    font-style: italic;
    text-align: center;
    font-size: 2vw;
    font-weight: bold;
    margin-top: 15vh;
    user-select: none;
}

.toast {
    width: 50%;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
