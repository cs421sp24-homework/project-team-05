<template>
    <div class="verification-container">
        <input
            v-for="(code, index) in ivCode"
            :key="index"
            v-model="ivCode[index]"
            @input="handleInput([code, index], $event)"
            @keydown="handleKeyDown([code, index], $event)"
            @paste="handlePaste"
            ref="inputFieldRef"
            maxlength="1"
            class="verification-input"
        />
    </div>
</template>
    
<script>
    import { nextTick, ref, getCurrentInstance } from 'vue';
    export default{
        data(){
            return {
                ivCode: ['', '', '', '', '', '']
            }
        },
        methods: {
            handleInput(data, event) {
                const value = data[0];
                const index = data[1];
                this.ivCode[index] = value;
            
                if (this.ivCode.join('').length === 6) {
                    this.$emit('ivcode', this.ivCode.join(''));
                }
            
                if (value && index < this.ivCode.length - 1) {
                    const nextInput = event.target.nextElementSibling;
                    if (nextInput) {
                        nextTick(() => {
                            nextInput.focus();
                        });
                    }
                }
            },
            handleKeyDown(data, event) {
                const value = data[0];
                const index = data[1];
                if (event.key === 'Backspace' && index > 0 && !value) {
                    const prevInput = event.target.previousElementSibling;
                    if (prevInput) {
                        nextTick(() => {
                            prevInput.focus();
                        });
                    }
                }
                if (event.key === 'Backspace' && this.ivCode.join('').length === 6) {
                    this.$emit("backspace")
                }
            },
            handlePaste(event){
                const clipboardData = event.clipboardData;
                const pastedText = clipboardData.getData('text');
                const codes = pastedText.trim().substring(0, 6).split('');
                this.ivCode = codes.concat(Array(6 - codes.length).fill(''));
                nextTick(() => {
                    const lastInput = this.$refs.inputFieldRef[this.ivCode.length - 1];
                    if (lastInput) {
                        lastInput.focus();
                    }
            })
            },
            clear() {
                this.ivCode = ['', '', '', '', '', ''];
            }
        }
    }
</script>

<style scoped>
     
    .verification-input {
        width: 3.3vw;
        height: 3.3vw;
        margin-left: 0.6vw;
        margin-right: 0.6vw;
        text-align: center;
        font-size: 2vw;
        font-weight: 300;
        border: 2px solid #cec7c7;
        border-radius: 8px;
    }
     
    .verification-input:focus {
        outline: none;
        border-color: #007bff;
        box-shadow: 0 0 5px #007bff;
    }
</style>