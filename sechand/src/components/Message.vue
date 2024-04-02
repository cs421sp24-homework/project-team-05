<template>
    <div id="msg-main">
        <div v-if="message.sender.id != user.id" id="msg-guest">
            <div id="guest-img">
                <img :src="message.sender.image" style="height: 5vh; width: 5vh; border-radius: 50%; object-fit: cover;"/>
            </div>

            <div id="guest-text">

                <div id="guest-headline">
                    <div style="font-size: 1vw; font-weight: 700;  margin-left: 0.5vw; margin-right: 0.7vw;">
                        {{ message.sender.displayname }}</div>
                    <div style="color: #666666; font-size: 0.8vw;">{{ message.timestamp }}</div>
                </div>

                <div id="guest-content">
                    {{ message.content }}
                    <span v-if="message.data">
                        <br>{{ message.data }}
                    </span>
                </div>
            </div>
        </div>

        <div id="msg-home" v-else>
            <div id="home-text">

                <div id="home-headline">
                    <div style="color: #666666; font-size: 0.8vw;">{{ message.timestamp }}</div>
                    <div style="font-size: 1vw; font-weight: 700; margin-left: 0.7vw; margin-right: 0.8vw;">
                        {{ message.sender.displayname }}</div>
                </div>

                <div id="home-content">
                    {{ message.content }}
                    <span v-if="message.data">
                        <br>{{ message.data }}
                    </span>
                </div>

            </div>

            <div id="home-img">
                <img :src="message.sender.image" style="height: 5vh; width: 5vh; border-radius: 50%; object-fit: cover;"/>
            </div>
        </div>
    </div>

    
</template>

<script>

export default {
    data(){
        return {
            
        }
    },

    props: {
        user: Object,
        message: Object,
    },
}

</script>

<style scoped>
#msg-main{
    height: 100%;
}

#msg-guest{
    margin-top: 1vh;
    margin-bottom: 1vh;
    margin-left: 1vw;
    flex-direction: row;
    display: flex;
}

#guest-img{
    float: left;
    width: 5vh;
    height: 100%;
    margin-top: 1vh;
}

#guest-text{
    margin-left: 1vw; 
}

#guest-headline{
    display: flex;
    align-items: center;
}

#guest-content{
    background-color: white;
    border-radius: 1vh;
    font-size: 0.9vw;
    max-width: 20vw;
    width: fit-content;
    padding-left: 0.5vw;
    padding-right: 0.5vw;
    padding-top: 0.5vh;
    padding-bottom: 0.5vh;
    overflow-wrap: break-word;
}

#msg-home{
    margin-top: 1vh;
    margin-bottom: 1vh;
    margin-right: 1vw;
    flex-direction: row;
    display: flex;
}

#home-img{
    margin-top: 1vh;
    float: right;
    width: 5vh;
    height: 5vh;
}

#home-text{
    margin-left: auto;
    margin-right: 1vw;
}

#home-headline{
    display: flex;
    align-items: center;
    margin-left:auto;
    width: fit-content;
}

#home-content{
    background-color: #0d6efd;
    color: white;
    border-radius: 1vh;
    font-size: 0.9vw;
    max-width: 20vw;
    width: fit-content;
    padding-left: 0.5vw;
    padding-right: 0.5vw;
    padding-top: 0.5vh;
    padding-bottom: 0.5vh;
    margin-left: auto;
    overflow-wrap: break-word;
}

</style>