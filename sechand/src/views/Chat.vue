<template>
    <UserNavbar/>

    <div id="left"></div>
    <div id="right"></div>

    <div id="main">
        <div id="content">
            <div id="content-left">
                <div class="list-group" id="scroll" v-if="chat_list.length">
                    <a v-for="(item, index) in chat_list" 
                    @click="setActive(index)" 
                    :class="['list-group-item', 'list-group-item-action', {'active':index===active_chat }]" 
                    aria-current="true"
                    id="list_item">
                        <div class="d-flex w-100 justify-content-between">
                            <div style="display: flex;">
                                <h5 style="margin-right: 0; font-weight: 700; font-size: 2vh;">{{ item.name }}</h5>
                                <!-- tag -->
                            </div>
                        <small>{{ "time" }}</small>
                        </div>
                        <p class="mb-1">{{ "discription" }}</p>
                        <small style="font-weight: bold;">{{ "additional info" }} </small>
                    </a>
                </div>
            </div>

            <div id="no-select" v-if="active_chat == null">---</div>

            <div id="content-right" v-else>
                <div id="head_line">
                    <p style="margin-left: 2vw; margin-top: 1vh;" v-if="active_chat != null">{{ chat_list[active_chat].name }}</p>
                </div>

                <div id="msg">
                    <div v-for="(item, index) of chat_list[active_chat].msg">
                        <Message :user="home_user" :message="item"/>
                    </div>
                </div>

                <div id="input">
                    <div id="toolbox">
                        potentially a toolbox?
                    </div>

                    <div id="text-input">
                        <input id="input-box" type="text" v-model="cur_input" class="form-control" :placeholder="'Send a message to '+ chat_list[active_chat].name + '...'">
                        <button id="btn" @click="sendMessage" class="btn btn-primary">Send</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import UserNavbar from '@/components/UserNavbar.vue';
import Message from '@/components/Message.vue';


export default {
    data () {
        return {
            chat_list: [{name: "Elain",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHH"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        }, 
                        {name: "Allen",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGG"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        }, 
                        {name: "Tao",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGG"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        }, 
                        {name: "Ali Madooei",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGG"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        }, 
                        {name: "Kim",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGG"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        }, 
                        {name: "Captain America",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGG"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        }, 
                        {name: "Dayuummm",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGG"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        },
                        {name: "FIFA World Cup",
                         msg:  [{   id: true,
                                    content: "HHHHHHHHHHHHHH"
                                }, 
                                {
                                    id: false,
                                    content: "GGGGGGGGGGGGGGGGGGGGGGGGG"
                                }, 
                                {
                                    id: true,
                                    content: "LLLLLLLLLLLLLLLLLLLLLLLL"
                                }]
                        }],
            active_chat: 0,
            cur_input: "",
            home_user: null
        }
    },
    methods: {
        setActive(index) {
            this.active_chat = index;
        }
    },
    components: {
        UserNavbar,
        Message
    },
    created(){
        this.home_user = JSON.parse(localStorage.getItem('user'));
        console.log(this.home_user);
    },
    
}
</script>


<style scoped>
#left {
    float: left;
    width: 15vw;
    height: 100vh;
    background-color: #d8e8fa;
}

#right {
    float: right;
    width: 15vw;
    height: 100vh;
    background-color: #d8e8fa;
}

#main {
    margin-top: 15vh;
    float: inline-start;
    width: 70vw;
}

#content{
    width: 60vw;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
    border-radius: 1vh;
    display: flex;
    flex-direction: row;
}

#content-left{
    width: 15vw;
    border-right: solid rgb(134, 134, 134) 1px;
}

#scroll{
    height: 73vh;
    overflow-y: auto;
    overflow-x: hidden;
}


#content-right{
    width: 45vw;
}

#head_line{
    font-size: 3vh;
    height: 5vh;
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    border-bottom: solid rgb(134, 134, 134) 1px;
}

#msg{
    height: 55vh;
    border-bottom: solid rgb(134, 134, 134) 1px;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: rgb(244, 244, 244);
}


#input{
    height: calc(100% - 45vh - 5vh);
}

#toolbox{
    height: 2vh;
    /* border-bottom: solid rgb(134, 134, 134) 1px; */
}

#text-input{
    margin-top: 1.5vh;
    margin-left: 1vw;
    margin-right: 1vw;
    display: flex;
    flex-direction: row;
}

#input-box{
    height: 4vh;
    font-size: 2vh;
    width: 39vw;
    border-radius: 2vh;
}

#btn {
    margin-left: 1vw; 
    height: 4vh; 
    border-radius: 1vh;
    font-size: 2vh;
    border-radius: 2vh;
}

</style>