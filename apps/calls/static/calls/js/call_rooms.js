/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
/*!**************************************************!*\
  !*** ./apps/calls/ts/scripts/call_rooms/main.ts ***!
  \**************************************************/
__webpack_require__.r(__webpack_exports__);
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const room_id = location.pathname.split('/').at(-1);
const callRoomsWebSocket = new WebSocket(`ws://${location.host}/call-rooms/${room_id}`);
const localeVideo = document.querySelector('.video__current-user');
const remoteVideo = document.querySelector('.video__another-user');
if (!localeVideo) {
    throw Error('Not found locale video container!');
}
if (!remoteVideo) {
    throw Error('Not found remote video container!');
}
let localStream;
let remoteStream;
const servers = {
    iceServers: [{ urls: ['stun:stun1.l.google.com:19302'] }],
};
const createOffer = () => __awaiter(void 0, void 0, void 0, function* () {
    localStream = yield navigator.mediaDevices.getUserMedia({ audio: true, video: { facingMode: 'user' } });
    localeVideo.srcObject = localStream;
    remoteStream = new MediaStream();
    remoteVideo.srcObject = remoteStream;
    const peerConnection = new RTCPeerConnection(servers);
    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track);
    });
    peerConnection.ontrack = (event) => {
        event.streams[0].getTracks().forEach((track) => {
            remoteStream.addTrack(track);
        });
    };
    peerConnection.onicecandidate = () => __awaiter(void 0, void 0, void 0, function* () {
        console.log(peerConnection.localDescription);
    });
    const offer = yield peerConnection.createOffer();
    yield peerConnection.setLocalDescription(offer);
    console.log(offer);
});
callRoomsWebSocket.onmessage = (_a) => __awaiter(void 0, [_a], void 0, function* ({ data }) {
    const parsed_data = JSON.parse(data);
    switch (parsed_data.type) {
        case "offer" /* ActionType.offer */: {
            yield createOffer();
            break;
        }
    }
});


/******/ })()
;
//# sourceMappingURL=call_rooms.js.map