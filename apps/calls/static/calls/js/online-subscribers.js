"use strict";
const ws = new WebSocket('ws://localhost:8000/subscribers/');
window.subscriberWebsocket = ws;
