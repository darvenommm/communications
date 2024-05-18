export {};

declare global {
  interface Window {
    callOffersWebSocket: WebSocket;
  }
}
