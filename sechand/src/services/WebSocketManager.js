// let instance = null;

// function createInstance(url) {
//     const ws = new WebSocket(url);

//     ws.onopen = () => {
//         console.log("WebSocket connected");
//         // Handle WebSocket opening actions
//     };

//     ws.onmessage = (message) => {
//         console.log("WebSocket message received:", message.data);
//         // Handle incoming messages
//     };

//     ws.onerror = (error) => {
//         console.error("WebSocket error:", error);
//         // Handle errors
//     };

//     ws.onclose = () => {
//         console.log("WebSocket disconnected");
//         // Handle WebSocket closing actions
//     };

//     return ws;
// }

// export function getWebSocketInstance(url) {
//     if (!instance || instance.readyState === WebSocket.CLOSED) {
//         instance = createInstance(url);
//     }
//     return instance;
// }

const webSockets = {};

function createWebSocket(userId) {
    const WBSOCKET_PREFIX = import.meta.env.VITE_SOCKET_HOST ? import.meta.env.VITE_SOCKET_HOST : "ws://127.0.0.1:8000/";
    const wsPath = WBSOCKET_PREFIX + `ws/chat/${userId}/`;
    const ws = new WebSocket(wsPath);
    ws.onopen = () => console.log(`WebSocket connected for user ${userId}`);
    ws.onclose = () => console.log(`WebSocket disconnected for user ${userId}`);
    ws.onerror = (error) => console.error(`WebSocket error for user ${userId}:`, error);
    // Setup other event handlers as needed
    return ws;
}

export function getWebSocketInstance(userId) {
    if (!webSockets[userId] || webSockets[userId].readyState === WebSocket.CLOSED) {
        webSockets[userId] = createWebSocket(userId);
    }
    return webSockets[userId];
}

export function closeWebSocketInstance(userId) {
    if (webSockets[userId]) {
        webSockets[userId].close();
        delete webSockets[userId];
    }
}