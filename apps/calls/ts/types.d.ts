export {};

declare global {
  interface Window {
    homePath: string;

    callOffersWebSocket: WebSocket;
  }
}
