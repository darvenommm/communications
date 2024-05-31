/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./apps/calls/assets/ts/components/notify/index.ts":
/*!*********************************************************!*\
  !*** ./apps/calls/assets/ts/components/notify/index.ts ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   closeNotify: () => (/* binding */ closeNotify),
/* harmony export */   showNotify: () => (/* binding */ showNotify)
/* harmony export */ });
const NOTIFY_CLASS = 'notify';
const NOTIFY_ACTIVE_CLASS = `${NOTIFY_CLASS}--active`;
const NOTIFY_TEXT_CLASS = 'notify__text';
const notify = document.querySelector(`.${NOTIFY_CLASS}`);
if (!notify) {
    throw Error('Not found notify container!');
}
const notifyText = notify.querySelector(`.${NOTIFY_TEXT_CLASS}`);
if (!notifyText) {
    throw Error('Not found notify text container!');
}
const closeNotify = () => notify.classList.remove(NOTIFY_ACTIVE_CLASS);
let notifyTimeoutId;
const showNotify = (message, timeout = Infinity) => {
    clearTimeout(notifyTimeoutId);
    notifyText.textContent = message;
    notify.classList.add(NOTIFY_ACTIVE_CLASS);
    if (timeout !== Infinity) {
        notifyTimeoutId = setTimeout(closeNotify, timeout);
    }
};


/***/ }),

/***/ "./apps/calls/assets/ts/components/videos/index.ts":
/*!*********************************************************!*\
  !*** ./apps/calls/assets/ts/components/videos/index.ts ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   addCloseCallHandler: () => (/* binding */ addCloseCallHandler),
/* harmony export */   addHideCallHandler: () => (/* binding */ addHideCallHandler),
/* harmony export */   addMuteCallHandler: () => (/* binding */ addMuteCallHandler),
/* harmony export */   createAndSetLocalMediaStream: () => (/* binding */ createAndSetLocalMediaStream),
/* harmony export */   createAndSetRemoteMediaStream: () => (/* binding */ createAndSetRemoteMediaStream)
/* harmony export */ });
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
const videoControlsContainer = document.querySelector('.call-controls');
if (!videoControlsContainer) {
    throw Error('Not found video controls container!');
}
if (!localeVideo) {
    throw Error('Not found locale video container!');
}
if (!remoteVideo) {
    throw Error('Not found remote video container!');
}
const closeButton = videoControlsContainer.querySelector('.call-controls__close');
const muteButton = videoControlsContainer.querySelector('.call-controls__mute');
const hideButton = videoControlsContainer.querySelector('.call-controls__hide');
if (!closeButton || !muteButton || !hideButton) {
    throw Error('Not found some controls buttons in video controls container!');
}
const CONSTRAINTS = {
    audio: true,
    video: {
        width: { min: 640, ideal: 720, max: 720 },
        height: { min: 480, ideal: 720, max: 720 },
        facingMode: 'user',
    },
};
const getLocalMediaStream = () => __awaiter(void 0, void 0, void 0, function* () {
    return yield navigator.mediaDevices.getUserMedia(CONSTRAINTS);
});
const createAndSetLocalMediaStream = () => __awaiter(void 0, void 0, void 0, function* () {
    let localMediaStream;
    try {
        localMediaStream = yield getLocalMediaStream();
    }
    catch (error) {
        console.error(error);
        throw error;
    }
    return (localeVideo.srcObject = localMediaStream);
});
const createAndSetRemoteMediaStream = () => {
    return (remoteVideo.srcObject = new MediaStream());
};
const addCloseCallHandler = (callback) => {
    closeButton.onclick = callback;
};
const addMuteCallHandler = (localMediaStream) => {
    muteButton.onclick = () => {
        const audioTrack = localMediaStream.getTracks().find((track) => track.kind === 'audio');
        if (!audioTrack) {
            return;
        }
        audioTrack.enabled = !audioTrack.enabled;
    };
};
const addHideCallHandler = (localMediaStream) => {
    hideButton.onclick = () => {
        const videoTrack = localMediaStream.getTracks().find((track) => track.kind === 'video');
        if (!videoTrack) {
            return;
        }
        videoTrack.enabled = !videoTrack.enabled;
    };
};


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
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
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
/*!******************************************************!*\
  !*** ./apps/calls/assets/ts/main/call_rooms/main.ts ***!
  \******************************************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _components_videos__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../components/videos */ "./apps/calls/assets/ts/components/videos/index.ts");
/* harmony import */ var _components_notify__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../components/notify */ "./apps/calls/assets/ts/components/notify/index.ts");
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};


const RTC_CONFIGURATION = {
    iceServers: [{ urls: ['stun:stun2.1.google.com:19302'] }],
};
const peerConnection = new RTCPeerConnection(RTC_CONFIGURATION);
let callRoomsWebSocket;
peerConnection.addEventListener('icecandidate', ({ candidate }) => {
    if (candidate) {
        console.log('Sending ICE candidate:', candidate);
        callRoomsWebSocket.send(JSON.stringify({ type: "candidate" /* ActionType.candidate */, data: candidate }));
    }
});
peerConnection.addEventListener('connectionstatechange', () => {
    if (peerConnection.connectionState === 'connected') {
        console.log('connected');
        callRoomsWebSocket.send(JSON.stringify({ type: "connected" /* ActionType.connected */ }));
    }
});
const startCommunication = () => {
    console.log('Start communication');
    const roomId = location.pathname.split('/').filter(Boolean).at(-1);
    callRoomsWebSocket = new WebSocket(`ws://${location.host}/call-rooms/${roomId}/`);
    callRoomsWebSocket.onmessage = (_a) => __awaiter(void 0, [_a], void 0, function* ({ data }) {
        const parsedData = JSON.parse(data);
        console.log('Received data:', parsedData);
        switch (parsedData.type) {
            case "offer" /* ActionType.offer */: {
                yield setLocalOffer();
                return sendOffer();
            }
            case "answer" /* ActionType.answer */: {
                yield setRemoteOffer(parsedData.data);
                yield setLocalAnswer();
                return sendAnswer();
            }
            case "final" /* ActionType.final */: {
                return yield setRemoteAnswer(parsedData.data);
            }
            case "candidate" /* ActionType.candidate */: {
                return yield setCandidate(parsedData.data);
            }
            case "close" /* ActionType.close */: {
                return void (location.href = window.homePath);
            }
            case "time.limit" /* ActionType.timeLimit */: {
                return showTimeLimit(parsedData.data);
            }
            default: {
                return console.error('Unknown Action type in the call room script!');
            }
        }
    });
};
const setLocalOffer = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Create offer');
    const offer = yield peerConnection.createOffer();
    console.log('Set offer in local description');
    yield peerConnection.setLocalDescription(offer);
});
const sendOffer = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Send offer');
    callRoomsWebSocket.send(JSON.stringify({
        type: "offer" /* ActionType.offer */,
        data: peerConnection.localDescription,
    }));
});
const setRemoteOffer = (receivedOffer) => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Set remote offer');
    const offer = new RTCSessionDescription(receivedOffer);
    yield peerConnection.setRemoteDescription(offer);
});
const setLocalAnswer = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Create answer');
    const answer = yield peerConnection.createAnswer();
    yield peerConnection.setLocalDescription(answer);
});
const sendAnswer = () => {
    console.log('Send answer');
    callRoomsWebSocket.send(JSON.stringify({ type: "answer" /* ActionType.answer */, data: peerConnection.localDescription }));
};
const setRemoteAnswer = (receivedAnswer) => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Set remote answer');
    const answer = new RTCSessionDescription(receivedAnswer);
    yield peerConnection.setRemoteDescription(answer);
});
const setCandidate = (iceCandidate) => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Adding candidate');
    try {
        yield peerConnection.addIceCandidate(new RTCIceCandidate(iceCandidate));
    }
    catch (error) {
        console.error('Error adding ICE candidate', error);
    }
});
const showTimeLimit = (timeLimit) => {
    (0,_components_notify__WEBPACK_IMPORTED_MODULE_1__.showNotify)(`You will talk for ${timeLimit} minutes!`);
};
const init = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Initializing media streams');
    const localMediaStream = yield (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.createAndSetLocalMediaStream)();
    const remoteMediaStream = (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.createAndSetRemoteMediaStream)();
    localMediaStream.getTracks().forEach((track) => {
        console.log('Local media steams set');
        peerConnection.addTrack(track, localMediaStream);
    });
    peerConnection.ontrack = ({ streams }) => {
        console.log('Received remote stream:', streams[0]);
        streams[0].getTracks().forEach((track) => {
            remoteMediaStream.addTrack(track);
        });
    };
    startCommunication();
    (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.addCloseCallHandler)(() => callRoomsWebSocket.send(JSON.stringify({ type: "close" /* ActionType.close */ })));
    (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.addMuteCallHandler)(localMediaStream);
    (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.addHideCallHandler)(localMediaStream);
});
init();

})();

/******/ })()
;
//# sourceMappingURL=call_rooms.js.map