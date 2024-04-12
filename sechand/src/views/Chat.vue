<template>
  <div v-if="this.currentUser">
    <UserNavbar :currentUser="currentUser" @userLogout="userStateChange" />

    <div id="left"></div>
    <div id="right"></div>

    <div id="main">
      <div id="content">
        <div id="content-left">
          <div class="list-group" id="scroll" v-if="chat_list">
            <a v-for="(item, index) in chat_list" @click="setActive(item, index)" :class="[
    'list-group-item',
    'list-group-item-action',
    { active: index === active_chat },
    'w-100',
  ]" aria-current="true" id="list_item">
              <div class="avatar-wrapper">
                <img :src="item.user.image" style="
                    height: 3vw;
                    width: 3vw;
                    border-radius: 50%;
                    object-fit: cover;
                  " />
              </div>
              <div class="left-info">
                <div class="d-flex">
                  <h5 style="margin-right: 0; font-weight: 700; font-size: 1.2vw">
                    {{ item.user.displayname }}
                  </h5>
                  {{ item.notification }}
                  <small style="font-size: 0.7vw" id="time" v-if="item.last_message">{{ item.last_message.timestamp
                    }}</small>
                </div>
                <p class="mb-1" style="color: #a0a0a0; font-size: 0.9vw" v-if="item.last_message">
                  {{
                    item.last_message.content.length > 35
                      ? item.last_message.content.slice(0, 35) + "..."
                      : item.last_message.content
                  }}
                </p>
                <!-- <small style="font-weight: bold;">{{ "additional info" }} </small> -->
              </div>
            </a>
          </div>
        </div>

        <div id="no-select" v-if="active_chat == null">
          {{
    chat_list ? "No conversation selected." : "No conversation exists."
  }}
        </div>

        <div id="content-right" v-else>
          <div id="head_line">
            <p style="margin-left: 2vw; margin-top: 1vh" v-if="active_chat != null">
              {{ chat_list[active_chat].user.displayname }}
            </p>
          </div>

          <div id="msg" ref="messageContainer">
            <div v-for="(item, index) of chat_list[active_chat].messages">
              <Message :user="home_user" :message="item" @buy="sendOrder" @confirm="sendConfirmation" />
            </div>
          </div>

          <div id="input">
            <div id="toolbox">potentially a toolbox?</div>

            <div id="text-input">
              <input id="input-box" type="text" v-model="newMessage" class="form-control" :placeholder="'Send a message to ' +
    chat_list[active_chat].user.displayname +
    '...'
    " />
              <button id="sendBtn" @click="sendMessage" class="btn btn-primary">
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Message from "@/components/Message.vue";
import { getWebSocketInstance } from "@/services/WebSocketManager";
import axios from "axios";

export default {
  data() {
    return {
      chat_list: null,
      active_chat: null,
      active_roomId: null,
      newMessage: "",
      home_user: null,
      ws: null,
      shouldReconnect: true,
      // receiver: null,
    };
  },
  props: {
    currentUser: Object,
  },
  methods: {
    userStateChange() {
      this.$emit("userStateChange", {});
    },
    setActive(item, index) {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      const accessToken = localStorage.getItem("access_token");
      if (this.active_roomId && index != this.active_chat) {
        axios.post(HTTP_PREFIX + `api/v1/chat/Conversation/notification/activate`, 
        {
          "room_id": this.active_roomId,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
      }
      this.active_chat = index;
      this.active_roomId = item.id;
      item.notification = 0;
      this.scrollToBottom();
      axios.post(HTTP_PREFIX + `api/v1/chat/Conversation/message/read`, 
        {
          "room_id": this.active_roomId,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
      // console.log("notifications", this.chat_list[index].user, this.chat_list[index].notification);
    },
    connect() {
      const WBSOCKET_PREFIX = import.meta.env.VITE_SOCKET_HOST ? import.meta.env.VITE_SOCKET_HOST : "ws://127.0.0.1:8000/";

      const wsPath = WBSOCKET_PREFIX + `ws/chat/${this.home_user.id}/`; // Use roomId in the path
      console.log("using wsPath ", wsPath);
      // if (this.ws) {
      //   console.log("ws instance exist, close the current one, open a new one.");
      //   this.shouldReconnect = false;
      //   this.ws.close(); // Close the existing connection if it exists
      // }
      this.ws = getWebSocketInstance(wsPath);
      this.ws.onmessage = this.receiveMessage;
      this.ws.onclose = () => {
        console.log("WebSocket closed.");
        // if (this.shouldReconnect) {
        //   console.log("Attempting to reconnect...")
        //   setTimeout(this.connect, 1000);
        // }
      };
    },
    receiveMessage(e) {
      const message = JSON.parse(e.data);
      console.log("received message", message);
      const room = this.chat_list.find((room) => room.id === message.room_id);
      // console.log("room", room);
      if (room == undefined) {
        this.chat_list.unshift({
          id: message.room_id,
          user: message.sender,
          messages: [message],
          last_message: message,
          notification: 0,
        });
        if (this.active_chat) {
          this.active_chat++;
          this.active_roomId = this.chat_list[this.active_chat].id;
        }
      }
      room.messages.push(message);
      room.last_message = message;
      this.scrollToBottom();
      if (this.active_roomId != message.room_id) {
        // room.notification++;
        const HTTP_PREFIX = import.meta.env.VITE_HOST;
        const accessToken = localStorage.getItem("access_token");
        axios.get(HTTP_PREFIX + `api/v1/chat/Conversation/notification/one-count/${room.id}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }).then((response) => {
            console.log("notification", room.user.displayname, response.data.count);
            room.notification = response.data.count;
          }).catch((error) => {
            console.error(error);
          });
      }
      // console.log("notification", room.user.displayname, room.notification);
    },
    sendMessage() {
      if (this.newMessage.trim() !== "") {
        // senderUser = JSON.parse(localStorage.getItem('user'))
        const message = {
          message: this.newMessage, // Adjust according to your backend expectations
          sender: this.home_user.id,
          room_id: this.active_roomId,
          // The sender should be determined by the backend.
        };
        this.ws.send(JSON.stringify(message)); // Send the message content
        console.log(message);
        this.newMessage = "";

        // const HTTP_PREFIX = import.meta.env.VITE_HOST;
        // const accessToken = localStorage.getItem("access_token");
        // axios.post(HTTP_PREFIX + `api/v1/chat/Conversation/message/new`, {
        //     "room_id": this.active_roomId,
        //     "receiver_id": this.chat_list[this.active_chat].user.id,
        //   },
        //   {
        //     headers: {
        //       Authorization: `Bearer ${accessToken}`,
        //     },
        //   }).then((response) => {
        //     console.log("notification", this.chat_list[this.active_chat].user.id, response.data.count);
        //   }).catch((error) => {
        //     console.error(error);
        //   });
      }
    },
    async sendOrder(data) {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      // const accessToken = localStorage.getItem("access_token");

      const response = await axios.get(HTTP_PREFIX + `api/v1/post/Item/${data.item_data.id}`)
      console.log("item is sold", response.data.is_sold);
      if (response.data.is_sold) {
        alert("This item has been sold.");
      } else {
        // console.log("item data", data);
        const message = {
          message: 'I want to buy this item.',
          sender: this.home_user.id,
          room_id: this.active_roomId,
          item: data.item_data,
        };
        this.ws.send(JSON.stringify(message));
      }
    },
    async sendConfirmation(data) {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      const accessToken = localStorage.getItem("access_token");
      const response = await axios.get(HTTP_PREFIX + `api/v1/post/Item/${data.item_data.id}`)
      if (response.data.is_sold) {
        alert("This item has been sold.");
      } else {
        const message = {
          message: 'I have sold this item to you.',
          sender: this.home_user.id,
          room_id: this.active_roomId,
          item: data.item_data,
        };
        this.ws.send(JSON.stringify(message));

        console.log("seller id", data.item_data.seller);
        // console.log("not sold")

        const response = await axios.post(
          HTTP_PREFIX + `api/v1/post/Order/Transaction/new`,
          {
            "item_id": data.item_data.id,
            "buyer_id": this.chat_list[this.active_chat].user.id,
            "seller_id": data.item_data.seller,
            "price": data.item_data.price,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        var container = this.$refs.messageContainer;
        if (container) container.scrollTop = container.scrollHeight;
      });
    },
  },
  components: {
    UserNavbar,
    Message,
  },
  async created() {
    this.home_user = JSON.parse(localStorage.getItem("user"));
    // console.log(this.home_user);
    // console.log('receiver', this.$route.params);
    const receiver = sessionStorage.getItem("receiver");
    const item = sessionStorage.getItem("item");
    sessionStorage.clear();

    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    const accessToken = localStorage.getItem("access_token");

    try {
      if (receiver) {
        await axios.post(
          HTTP_PREFIX + `api/v1/chat/Conversation/auto-send/${receiver}/${item}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        )

        const response = await axios.get(
          HTTP_PREFIX + `api/v1/chat/Conversation/list/${receiver}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.chat_list = response.data.chat_list;
        this.active_chat = response.data.active_chat;
        this.active_roomId = this.chat_list[this.active_chat].id;

        this.scrollToBottom();
      } else {
        const response = await axios.get(
          HTTP_PREFIX + "api/v1/chat/Conversation/list",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.chat_list = response.data;
      }
      // console.log("chat list", this.chat_list);
    } catch (error) {
      console.error(error);
    }
    this.connect();
  },
  beforeDestroy() {
    // this.shouldReconnect = false;
    if (this.ws) {
      this.ws.close();
    }
  },
  beforeRouteLeave(to, from, next) {
    if (this.active_roomId) {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      const accessToken = localStorage.getItem("access_token");
      axios.post(HTTP_PREFIX + `api/v1/chat/Conversation/notification/activate`, 
        {
          "room_id": this.active_roomId,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
    }
    next();
  },
};
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
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
  border-bottom: solid rgb(134, 134, 134) 1px;
}

#msg {
  height: 55vh;
  padding-bottom: 1.5vh;
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

#sendBtn {
  margin-left: 1vw;
  height: 3vh;
  font-size: 1.5vh;
  border-radius: 1.5vh;
  width: 4vw;
}
</style>