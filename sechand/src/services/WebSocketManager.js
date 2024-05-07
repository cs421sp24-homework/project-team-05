const webSockets = {};

function createWebSocket(userId) {
    const WBSOCKET_PREFIX = import.meta.env.VITE_SOCKET_HOST ? import.meta.env.VITE_SOCKET_HOST : "ws://127.0.0.1:8000/";
    const wsPath = WBSOCKET_PREFIX + `ws/chat/${userId}/`;
    const ws = new WebSocket(wsPath);
    ws.onopen = () => console.log(`WebSocket connected for user ${userId}`);
    ws.onmessage = (event) => {
        console.log("websocket manager triggers new notification");
        const e = new CustomEvent("getNotification");
        window.dispatchEvent(e);
    }
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

export function reconnectWebSocketInstance(userId) {
    closeWebSocketInstance(userId);
    return getWebSocketInstance(userId);
}