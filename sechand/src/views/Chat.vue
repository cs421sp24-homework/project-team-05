<template>
    <UserNavbar :currentUser="currentUser" @userLogout="userStateChange" />

    <div id="left"></div>
    <div id="right"></div>

    <div id="main">
        <div id="content">
            <div id="content-left">
                <div class="list-group" id="scroll" v-if="chat_list">
                    <a v-for="(item, index) in chat_list" @click="setActive(item, index)"
                        :class="['list-group-item', 'list-group-item-action', { 'active': index === active_chat }, 'w-100']"
                        aria-current="true" id="list_item">
                        <div class="avatar-wrapper">
                            <img :src="item.user.image"
                                style="height: 3vw; width: 3vw; border-radius: 50%; object-fit: cover;" />
                        </div>
                        <div class="left-info">
                            <div class="d-flex">
                                <h5 style="margin-right: 0; font-weight: 700; font-size: 1.4vw;">{{
        item.user.displayname }}</h5>
                                <small style="font-size: 0.7vw;" id="time" v-if="item.last_message">{{
        item.last_message.timestamp }}</small>
                            </div>
                            <p class="mb-1" style="color: #a0a0a0; font-size: 0.9vw;" v-if="item.last_message">
                                {{ item.last_message.content.length > 35 ? (item.last_message.content).slice(0, 35) +
        '...'
        : item.last_message.content }}</p>
                            <!-- <small style="font-weight: bold;">{{ "additional info" }} </small> -->
                        </div>
                    </a>
                </div>
            </div>

            <div id="no-select" v-if="active_chat == null">
                {{ chat_list ? "No conversation selected." : "No conversation exists." }}
            </div>

            <div id="content-right" v-else>
                <div id="head_line">
                    <p style="margin-left: 2vw; margin-top: 1vh;" v-if="active_chat != null">{{
        chat_list[active_chat].user.displayname }}</p>
                </div>

                <div id="msg" ref="messageContainer">
                    <div v-for="(item, index) of chat_list[active_chat].messages">
                        <Message :user="home_user" :message="item" />
                    </div>
                </div>

                <div id="input">
                    <div id="toolbox">
                        potentially a toolbox?
                    </div>

                    <div id="text-input">
                        <input id="input-box" type="text" v-model="newMessage" class="form-control"
                            :placeholder="'Send a message to '+ chat_list[active_chat].user.displayname + '...'">
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
import axios from "axios";


export default {
    data() {
        return {
            chat_list: null,
            active_chat: null,
            active_roomId: null,
            newMessage: "",
            home_user: null,
            // receiver: null,
        }
    },
    props: {
        currentUser: Object
    },
    methods: {
        userStateChange() {
            this.$emit("userStateChange", {});
        },
        setActive(item, index) {
            this.active_chat = index;
            this.active_roomId = item.id;
            console.log('active_roomId', this.active_roomId);
            this.scrollToBottom();
        },
        connect() {
            const wsPath = `ws://127.0.0.1:8000/ws/chat/${this.home_user.id}/`; // Use roomId in the path
            console.log('using wsPath ', wsPath)
            if (this.ws) {
                this.ws.close();  // Close the existing connection if it exists
            }
            this.ws = new WebSocket(wsPath);
            this.ws.onmessage = this.receiveMessage;
            this.ws.onclose = () => {
                console.log('WebSocket closed. Attempting to reconnect...');
                setTimeout(this.connect, 1000);
            };
        },
        receiveMessage(e) {
            const message = JSON.parse(e.data);
            console.log('received message', message);
            const room = this.chat_list.find(room => room.id === message.room_id);
            console.log('room', room);
            room.messages.push(message);
            room.last_message = message;
            this.scrollToBottom();
        },
        sendMessage() {
            if (this.newMessage.trim() !== '') {
                // senderUser = JSON.parse(localStorage.getItem('user'))
                const message = {
                    "message": this.newMessage, // Adjust according to your backend expectations
                    "sender": this.home_user.id,
                    "room_id": this.active_roomId
                    // The sender should be determined by the backend.
                };
                this.ws.send(JSON.stringify(message)); // Send the message content
                console.log(message)
                this.newMessage = '';
            }
        },
        scrollToBottom() {
            this.$nextTick(() => {
                var container = this.$refs.messageContainer;
                if (container) container.scrollTop = container.scrollHeight;
            });
        }
    },
    components: {
        UserNavbar,
        Message
    },
    async created() {
        this.home_user = JSON.parse(localStorage.getItem('user'));
        // console.log(this.home_user);
        console.log('receiver', this.$route.params);
        const receiver = this.$route.params.receiver;

        const HTTP_PREFIX = import.meta.env.VITE_HOST;

        try {
            const accessToken = localStorage.getItem('access_token');
            if (receiver) {
                const response = await axios.get(HTTP_PREFIX + `api/v1/chat/Conversation/list/${receiver}`, {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                });
                this.chat_list = response.data.chat_list;
                this.active_chat = response.data.active_chat;
            } else {
                const response = await axios.get(HTTP_PREFIX + 'api/v1/chat/Conversation/list', {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    },
                });
                this.chat_list = response.data;
            }
        } catch (error) {
            console.error(error);
        }
        this.connect();
    },

}
</script>


<style scoped>
#left {
    float: left;
    width: 14vw;
    height: 100vh;
    background-color: #d8e8fa;
}

#right {
    float: right;
    width: 14vw;
    height: 100vh;
    background-color: #d8e8fa;
}

#main {
    margin-top: 15vh;
    float: inline-start;
    width: 70vw;
}

#content {
    width: 60vw;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
    border-radius: 1vh;
    display: flex;
    flex-direction: row;
}



#content-left {
    width: 20vw;
    border-right: solid rgb(134, 134, 134) 1px;
}

#scroll {
    height: 73vh;
    overflow-y: auto;
    overflow-x: hidden;
    border-top-left-radius: 1vh;
    border-bottom-left-radius: 1vh;
}

.avatar-wrapper {
    align-items: center;
    float: left;
    margin-right: 0.7vw;
}

#left-info {

    flex-direction: 1;
}

#time {
    width: fit-content;
    margin-left: auto;
}

.small-text {
    font-size: 0.9vw;
}

#content-right {
    width: 40vw;
}

#no-select {
    font-size: 1vw;
    color: rgb(100, 100, 100);
    margin-top: 5vh;
    margin-left: auto;
    margin-right: auto;

}

#head_line {
    font-size: 3vh;
    height: 5vh;
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    border-bottom: solid rgb(134, 134, 134) 1px;
}

#msg {
    height: 55vh;
    border-bottom: solid rgb(134, 134, 134) 1px;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: rgb(244, 244, 244);
}


#input {
    height: calc(100% - 45vh - 5vh);
}

#toolbox {
    height: 1vh;
    /* border-bottom: solid rgb(134, 134, 134) 1px; */
}

#text-input {
    margin-top: 3.5vh;
    margin-left: 1vw;
    margin-right: 1vw;
    display: flex;
    flex-direction: row;
}

#input-box {
    height: 3vh;
    font-size: 1.5vh;
    width: 33vw;
    border-radius: 1.5vh;
}

#btn {
    margin-left: 1vw;
    height: 3vh;
    font-size: 1.5vh;
    border-radius: 1.5vh;
    width: 4vw;
}
</style>