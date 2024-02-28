<template>
    <header>
        <h1>{{title}}</h1>
        <Button text="Add" color="yellow"/>
    </header>
</template>
<script>
import Button from './Button.vue';
    export default {
        name: 'Header',
        props : {
            title: {
                type: String,
                default: 'Default Title',
                required: true
            }
        },
        components: {
            Button
        }
    }
</script>

<style scoped>
    header {
        background: #333;
        color: #fff;
        padding: 10px;
        text-align: center;
    }
</style>