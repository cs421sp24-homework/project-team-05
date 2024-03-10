<template>
    <div class="chat-container">
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" class="message">
          <strong>{{ message.sender }}:</strong> {{ message.content }}
        </div>
      </div>
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." class="message-input">
    </div>
  </template>
  
  <script>
  export default {
    props: ['roomId'], // Accept room ID as a prop
    data() {
      return {
        ws: null,
        newMessage: '',
        messages: [],
      };
    },
    created() {
      this.connect();
    },
    methods: {
      connect() {
        const wsPath = `ws://127.0.0.1:8000/ws/chat/${this.roomId}/`; // Use roomId in the path
        console.log('using wsPath ', wsPath)
        this.ws = new WebSocket(wsPath);
        this.ws.onmessage = this.receiveMessage;
        this.ws.onclose = () => {
          console.log('WebSocket closed. Attempting to reconnect...');
          setTimeout(this.connect, 1000);
        };
      },
      receiveMessage(e) {
        console.log("Message receive", e)
        const message = JSON.parse(e.data);
        this.messages.push(message);
      },
      sendMessage() {
        if (this.newMessage.trim() !== '') {
          const message = {
            "message": this.newMessage, // Adjust according to your backend expectations
            // The sender should be determined by the backend.
          };
          this.ws.send(JSON.stringify(message)); // Send the message content
          console.log(message)
          this.newMessage = '';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 90vh;
  }
  
  .messages {
    flex-grow: 1;
    overflow-y: auto;
  }
  
  .message-input {
    margin-top: 10px;
  }
  </style>
  