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
                    <!-- text content -->
                    {{ message.content }}
                    <!-- item info -->
                    <div class="content-grid" v-if="message.data && Object.keys(message.data).length">
                        <!-- image -->
                        <img id="guest-content-left" :src="message.data.image">
                        <div id="guest-content-right">
                            <!-- name -->
                            <div class="content-right-name">
                                {{ message.data.name }}
                            </div>
                            <!-- discription -->
                            <div class="content-right-desc">
                                {{ message.data.description }}
                            </div>
                            <!-- price -->
                            <div class="content-right-price-new" v-if="message.data.new_price">
                                <div style="color: rgb(92, 255, 83); font-size: 1.1vw; font-weight: 800;">
                                    $ {{ message.data.new_price }}
                                </div>
                                <div style="color: rgb(255, 77, 0); font-size: 0.9vw; font-weight: 700; text-decoration: line-through 2px;">
                                    $ {{ message.data.price }}
                                </div>
                            </div>
                            <div class="content-right-price" v-else>
                                    $ {{ message.data.price }}
                            </div>
                            <!-- buttons -->
                            <button v-if="!message.data.is_sold && message.content.slice(0,2)=='Hi'" class="content-btn btn btn-primary" disabled>Wait for Order</button>
                            <button v-else-if="!message.data.is_sold && message.content.slice(0,3)=='I w'" class="content-btn btn btn-success" @click="confirm">Confirm</button>
                            <button v-else-if="!message.data.is_sold && message.content.slice(0,3)=='I h'" class="content-btn btn btn-secondary" disabled>Sold to You</button>
                            <button v-else class="content-btn btn btn-secondary" disabled>Sold</button>
                        </div>
                    </div>
                    <!-- order identifier -->
                    <div v-if="message.data && message.data.identifier" id="idtf-wrapper">
                        Order Identifier:
                        <div style="width: 0.5vw;"></div>
                        <div id="idtf" v-for="char in (message.data.identifier? message.data.identifier: message.content.slice(-6,))">
                            {{ char }}
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div id="msg-home" v-else>
            <div id="home-text">
                <!-- text content -->
                <div id="home-headline">
                    <div style="color: #666666; font-size: 0.8vw;">{{ message.timestamp }}</div>
                    <div style="font-size: 1vw; font-weight: 700; margin-left: 0.7vw; margin-right: 0.8vw;">
                        {{ message.sender.displayname }}</div>
                </div>

                <!-- item info -->
                <div id="home-content">
                    {{ message.content }}
                    <div class="content-grid" v-if="message.data && Object.keys(message.data).length">
                        <!-- image -->
                        <img id="guest-content-left" :src="message.data.image">
                        <div id="guest-content-right">
                            <!-- name -->
                            <div class="content-right-name">
                                {{ message.data.name }}
                            </div>
                            <!-- discription -->
                            <div class="content-right-desc">
                                {{ message.data.description }}
                            </div>
                            <!-- price -->
                            <div class="content-right-price-new" v-if="message.data.new_price">
                                <div style="color: rgb(92, 255, 83); font-size: 1.1vw; font-weight: 800;">
                                    $ {{ message.data.new_price }}
                                </div>
                                <div style="color: rgb(255, 77, 0); font-size: 0.9vw; font-weight: 700; text-decoration: line-through 2px;">
                                    $ {{ message.data.price }}
                                </div>
                            </div>
                            <div class="content-right-price" v-else>
                                    $ {{ message.data.price }}
                            </div>
                            <!-- buttons -->
                            <button v-if="!message.data.is_sold && message.content.slice(0,2)=='Hi'" class="content-btn btn btn-light" @click="buy">Buy</button>
                            <button v-else-if="!message.data.is_sold && message.content.slice(0,3)=='I w'" class="content-btn btn btn-warning" style="font-size: 1vh;" disabled>Wait for Confirmation</button>
                            <button v-else-if="!message.data.is_sold && message.content.slice(0,3)=='I h'" class="content-btn btn btn-secondary">Sold to You</button>
                            <button v-else class="content-btn btn btn-secondary" disabled>Sold</button>
                        </div>
                    </div>

                    <!-- order identifier -->
                    <!-- <div v-if="message.data && Object.keys(message.data).length && message.content.slice(0,3)=='I h'" id="idtf-wrapper"> -->
                    <div v-if="message.data && message.data.identifier" id="idtf-wrapper">
                        Order Identifier:
                        <div style="width: 0.5vw;"></div>
                        <div id="idtf" v-for="char in (message.data.identifier? message.data.identifier: message.content.slice(-6,))">
                            {{ char }}
                        </div>
                    </div>
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

    methods:{
        confirm(){
            this.$emit("confirm", {'item_data': this.message.data});
        },
        buy(){
            this.$emit("buy", {'item_data': this.message.data});
        }
    }
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
    height: fit-content;
    padding-left: 0.5vw;
    padding-right: 0.5vw;
    padding-top: 0.5vh;
    padding-bottom: 0.5vh;
    overflow-wrap: break-word;
}

.content-grid{
    display: flex;
    flex-direction: row;
    padding-top: 1vh;
    margin-top: 0.5vh;
    padding-bottom: 0.5vh;
    border-top: rgb(171, 171, 171) 1px solid;
}

.content-btn{
    font-size: 1.2vh;
    font-weight: 800;
    min-width: 5vw;
    width: fit-content;
}

#guest-content-left{
    width: 8vw; 
    aspect-ratio: 1;
    object-fit: cover;
    border: 1px gray solid;
}

#guest-content-right{
    width: auto;
    padding-left: 1vw;
}

.content-right-name{
    font-size: 0.9vw;
    font-weight: 700;
    max-height: 3vw;
    margin-bottom: 0.5vw;
    overflow: hidden;
    text-overflow: ellipsis;
}

.content-right-desc{
    font-size: 0.7vw;
    font-weight: 500;
    height: 3vw;
    margin-bottom: 1vw;
    overflow: hidden;
    text-overflow: ellipsis;
}

.content-right-price{
    color: rgb(255, 77, 0);
    font-size: 1.1vw;
    font-weight: 800;
    height: fit-content;
    padding-bottom: 0.5vw;
}

.content-right-price-new{
    height: fit-content;
    padding-bottom: 0.5vw;
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

#home-content-left{
    width: 45%; 
    aspect-ratio: 1;
    object-fit: cover;
    border: 1px white solid;
}

#idtf-wrapper{
    align-items: center;
    width: 100%;
    display: flex;
    font-weight: 600;
    border-top: rgb(171, 171, 171) 1px solid;
    padding-top: 0.5vh;
    margin-top: 0.5vh;
}

#idtf{
    display: flex;
    align-items: center;
    font-weight: 900;
    height: 1.2vw;
    width: 1.2vw;
    padding-left: 0.2vw;
    margin-left: 0.4vw;
    border: 2px solid rgb(255, 77, 0);
    border-radius: 0.3vw;
    background-color: rgb(255, 77, 0);
    color: white;
}



</style>