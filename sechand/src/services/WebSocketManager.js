let instance = null;

function createInstance(url) {
    const ws = new WebSocket(url);

    ws.onopen = () => {
        console.log("WebSocket connected");
        // Handle WebSocket opening actions
    };

    ws.onmessage = (message) => {
        console.log("WebSocket message received:", message.data);
        // Handle incoming messages
    };

    ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        // Handle errors
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected");
        // Handle WebSocket closing actions
    };

    return ws;
}

export function getWebSocketInstance(url) {
    if (!instance || instance.readyState === WebSocket.CLOSED) {
        instance = createInstance(url);
    }
    return instance;
}
