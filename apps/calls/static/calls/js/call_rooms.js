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
const localeVideo = document.querySelector('.video__current-user');
const remoteVideo = document.querySelector('.video__another-user');
if (!localeVideo) {
    throw Error('Not found locale video container!');
}
if (!remoteVideo) {
    throw Error('Not found remote video container!');
}
const servers = {
    iceServers: [{ urls: ['stun:stun.l.google.com:19302'] }],
};
const peerConnection = new RTCPeerConnection(servers);
peerConnection.onconnectionstatechange = (event) => {
    console.log(event);
    console.log('change ebuchiq state');
};
setInterval(() => {
    console.log(peerConnection.signalingState);
}, 50);
const getLocalMediaStream = () => __awaiter(void 0, void 0, void 0, function* () {
    return yield navigator.mediaDevices.getUserMedia({
        audio: true,
        video: {
            width: { min: 640, ideal: 1920, max: 1920 },
            height: { min: 480, ideal: 1080, max: 1080 },
            facingMode: 'user',
        },
    });
});
const createLocaleMediaStream = () => __awaiter(void 0, void 0, void 0, function* () {
    let localMediaStream;
    try {
        localMediaStream = yield getLocalMediaStream();
    }
    catch (error) {
        console.error(error);
        throw error;
    }
    localeVideo.srcObject = localMediaStream;
    return localMediaStream;
});
const createRemoteMediaStream = () => {
    const remoteMediaStream = new MediaStream();
    remoteVideo.srcObject = remoteMediaStream;
    return remoteMediaStream;
};
const createOffer = (webSocket) => __awaiter(void 0, void 0, void 0, function* () {
    let isSended = false;
    peerConnection.onicecandidate = () => __awaiter(void 0, void 0, void 0, function* () {
        if (isSended) {
            return;
        }
        webSocket.send(JSON.stringify({
            type: "offer.send" /* ActionType.offerSend */,
            data: offer,
        }));
        isSended = true;
    });
    const offer = yield peerConnection.createOffer();
    peerConnection.setLocalDescription(offer);
});
const createAnswer = (webSocket, offer) => __awaiter(void 0, void 0, void 0, function* () {
    let isSended = false;
    peerConnection.onicecandidate = () => {
        if (isSended) {
            return;
        }
        webSocket.send(JSON.stringify({ type: "answer.send" /* ActionType.answerSend */, data: answer }));
        isSended = true;
    };
    yield peerConnection.setRemoteDescription(offer);
    const answer = yield peerConnection.createAnswer();
    yield peerConnection.setLocalDescription(answer);
});
const setAnswer = (answer) => __awaiter(void 0, void 0, void 0, function* () {
    yield peerConnection.setRemoteDescription(answer);
    setTimeout(() => console.log(peerConnection.connectionState, peerConnection.localDescription, peerConnection.remoteDescription, peerConnection.signalingState), 2000);
});
const createWebSocket = () => __awaiter(void 0, void 0, void 0, function* () {
    const room_id = location.pathname.split('/').at(-1);
    const callRoomsWebSocket = new WebSocket(`ws://${location.host}/call-rooms/${room_id}/`);
    callRoomsWebSocket.onmessage = (_a) => __awaiter(void 0, [_a], void 0, function* ({ data }) {
        const parsed_data = JSON.parse(data);
        console.log(parsed_data);
        switch (parsed_data.type) {
            case "offer.create" /* ActionType.offerCreate */: {
                yield createOffer(callRoomsWebSocket);
                break;
            }
            case "answer.create" /* ActionType.answerCreate */: {
                yield createAnswer(callRoomsWebSocket, parsed_data['data']);
                break;
            }
            case "answer.get" /* ActionType.answerGet */: {
                yield setAnswer(parsed_data['data']);
                break;
            }
        }
    });
});
const init = () => __awaiter(void 0, void 0, void 0, function* () {
    const localMediaStream = yield createLocaleMediaStream();
    const remoteMediaStream = createRemoteMediaStream();
    localMediaStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localMediaStream);
    });
    peerConnection.ontrack = ({ streams }) => {
        streams[0].getTracks().forEach((track) => {
            remoteMediaStream.addTrack(track);
        });
    };
    yield createWebSocket();
});
init();


/******/ })()
;
//# sourceMappingURL=call_rooms.js.map