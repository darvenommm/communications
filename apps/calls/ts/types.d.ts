export {};

declare global {
  interface Window {
    subscriberWebsocket: WebSocket;
  }
}
