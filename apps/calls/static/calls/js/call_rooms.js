/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./apps/calls/ts/components/videos/index.ts":
/*!**************************************************!*\
  !*** ./apps/calls/ts/components/videos/index.ts ***!
  \**************************************************/
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
    closeButton.onclick = () => {
        callback ? callback() : null;
        location.href = window.homePath;
    };
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
/*!**************************************************!*\
  !*** ./apps/calls/ts/scripts/call_rooms/main.ts ***!
  \**************************************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _components_videos__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../components/videos */ "./apps/calls/ts/components/videos/index.ts");
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __asyncValues = (undefined && undefined.__asyncValues) || function (o) {
    if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
    var m = o[Symbol.asyncIterator], i;
    return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () { return this; }, i);
    function verb(n) { i[n] = o[n] && function (v) { return new Promise(function (resolve, reject) { v = o[n](v), settle(resolve, reject, v.done, v.value); }); }; }
    function settle(resolve, reject, d, v) { Promise.resolve(v).then(function(v) { resolve({ value: v, done: d }); }, reject); }
};

const RTC_CONFIGURATION = {
    iceServers: [{ urls: ['stun:stun2.1.google.com:19302'] }],
};
const peerConnection = new RTCPeerConnection(RTC_CONFIGURATION);
let callRoomsWebSocket;
let offer;
let answer;
let isClose = false;
peerConnection.addEventListener('icecandidate', ({ candidate }) => {
    if (candidate) {
        console.log('Sending ICE candidate:', candidate);
        callRoomsWebSocket.send(JSON.stringify({ type: "candidate.send" /* ActionType.candidateSend */, data: candidate }));
    }
});
peerConnection.addEventListener('iceconnectionstatechange', () => {
    if (['connecting', 'connected'].includes(peerConnection.connectionState)) {
        callRoomsWebSocket.close();
        isClose = true;
    }
});
const startCommunication = () => {
    console.log('Start communication');
    const roomId = location.pathname.split('/').at(-1);
    callRoomsWebSocket = new WebSocket(`ws://${location.host}/call-rooms/${roomId}/`);
    callRoomsWebSocket.onmessage = (_a) => __awaiter(void 0, [_a], void 0, function* ({ data }) {
        var _b, e_1, _c, _d;
        const parsedData = JSON.parse(data);
        console.log('Received data:', parsedData);
        if (!parsedData.data) {
            return;
        }
        switch (parsedData.type) {
            case "who" /* ActionType.who */: {
                return yield handleWhoAmI(parsedData.data);
            }
            case "offer.get" /* ActionType.offerGet */: {
                yield setOffer(parsedData.data);
                return yield sendAnswer();
            }
            case "answer.get" /* ActionType.answerGet */: {
                return yield setAnswer(parsedData.data);
            }
            case "candidate.get" /* ActionType.candidateGet */: {
                try {
                    for (var _e = true, _f = __asyncValues(parsedData.data), _g; _g = yield _f.next(), _b = _g.done, !_b; _e = true) {
                        _d = _g.value;
                        _e = false;
                        const candidate = _d;
                        yield addIceCandidate(candidate);
                    }
                }
                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                finally {
                    try {
                        if (!_e && !_b && (_c = _f.return)) yield _c.call(_f);
                    }
                    finally { if (e_1) throw e_1.error; }
                }
                break;
            }
        }
    });
};
const handleWhoAmI = (whoAmI) => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Handle Who Am I', whoAmI);
    switch (whoAmI) {
        case 'starter': {
            yield sendOffer();
            return loopSends(getAnswer);
        }
        case 'answerer': {
            return loopSends(getOffer);
        }
        default: {
            return console.error('Incorrect whoAmI value');
        }
    }
});
const sendOffer = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Send offer');
    const offer = yield peerConnection.createOffer();
    yield peerConnection.setLocalDescription(offer);
    console.log('Set local offer', peerConnection.localDescription);
    callRoomsWebSocket.send(JSON.stringify({
        type: "offer.send" /* ActionType.offerSend */,
        data: peerConnection.localDescription,
    }));
});
const setOffer = (receiverOffer) => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Set offer');
    offer = new RTCSessionDescription(receiverOffer);
    yield peerConnection.setRemoteDescription(offer);
    console.log('Set remote offer');
    loopSends(getCandidate, 3000);
});
const sendAnswer = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Send answer');
    const answer = yield peerConnection.createAnswer();
    yield peerConnection.setLocalDescription(answer);
    callRoomsWebSocket.send(JSON.stringify({ type: "answer.send" /* ActionType.answerSend */, data: peerConnection.localDescription }));
});
const setAnswer = (receivedAnswer) => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Setting answer');
    answer = new RTCSessionDescription(receivedAnswer);
    yield peerConnection.setRemoteDescription(answer);
    loopSends(getCandidate, 3000);
});
const loopSends = (callback, time = 500) => {
    const interval_id = setInterval(() => {
        if (callback()) {
            return clearInterval(interval_id);
        }
    }, time);
};
const getOffer = () => {
    console.log('get offer', offer);
    if (offer) {
        return true;
    }
    return Boolean(callRoomsWebSocket.send(JSON.stringify({ type: "offer.get" /* ActionType.offerGet */ })));
};
const getAnswer = () => {
    console.log('get answer');
    if (answer) {
        return true;
    }
    return Boolean(callRoomsWebSocket.send(JSON.stringify({ type: "answer.get" /* ActionType.answerGet */ })));
};
const getCandidate = () => {
    if (isClose) {
        return true;
    }
    return Boolean(callRoomsWebSocket.send(JSON.stringify({ type: "candidate.get" /* ActionType.candidateGet */ })));
};
const addIceCandidate = (iceCandidate) => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Adding candidate');
    try {
        yield peerConnection.addIceCandidate(new RTCIceCandidate(iceCandidate));
    }
    catch (error) {
        console.error('Error adding ICE candidate', error);
    }
});
const init = () => __awaiter(void 0, void 0, void 0, function* () {
    console.log('Inittializing media streams');
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
    (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.addCloseCallHandler)();
    (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.addMuteCallHandler)(localMediaStream);
    (0,_components_videos__WEBPACK_IMPORTED_MODULE_0__.addHideCallHandler)(localMediaStream);
});
init();

})();

/******/ })()
;
//# sourceMappingURL=call_rooms.js.map