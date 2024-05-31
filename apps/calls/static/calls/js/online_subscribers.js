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

/***/ "./apps/calls/assets/ts/components/subscribers/index.ts":
/*!**************************************************************!*\
  !*** ./apps/calls/assets/ts/components/subscribers/index.ts ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   discardOnlineSubscriber: () => (/* binding */ discardOnlineSubscriber),
/* harmony export */   markOnlineSubscriber: () => (/* binding */ markOnlineSubscriber),
/* harmony export */   markOnlineSubscribers: () => (/* binding */ markOnlineSubscribers),
/* harmony export */   setCallButtonClickHandler: () => (/* binding */ setCallButtonClickHandler)
/* harmony export */ });
const SUBSCRIBERS_CONTAINER_CLASS = 'subscribers';
const SUBSCRIBER_CLASS = 'subscribers__item';
const SUBSCRIBER_ACTIVE_CLASS = `${SUBSCRIBER_CLASS}--active`;
const SUBSCRIBER_CALL_BUTTON_CLASS = 'subscribers__call-button';
const ONLINE_TEXT_CONTAINER_CLASS = 'subscribers__online';
const subscribersContainer = document.querySelector(`.${SUBSCRIBERS_CONTAINER_CLASS}`);
if (!subscribersContainer) {
    throw Error('Not found the subscribers container!');
}
const subscribers = subscribersContainer.querySelectorAll(`.${SUBSCRIBER_CLASS}`);
const goTroughSubscribers = (callback) => {
    for (const subscriber of subscribers) {
        const callButton = subscriber.querySelector(`.${SUBSCRIBER_CALL_BUTTON_CLASS}`);
        const onlineTextContainer = subscriber.querySelector(`.${ONLINE_TEXT_CONTAINER_CLASS}`);
        if (!callButton) {
            throw Error('Not found a call button in a subscriber!');
        }
        if (!onlineTextContainer) {
            throw Error('Not found a online text container in a subscriber!');
        }
        const needBreak = callback(subscriber, callButton, onlineTextContainer);
        if (needBreak) {
            break;
        }
    }
};
const getSubscriberData = (subscriber) => {
    const subscriberId = subscriber.dataset.subscriberId;
    const subscriberFullName = subscriber.dataset.subscriberFullName;
    if (!subscriberId || !subscriberFullName) {
        throw Error('Not found subscriber id or full name in dataset in the current subscriber!');
    }
    return { id: subscriberId, fullName: subscriberFullName };
};
const makeSubscriberActive = (subscriber, onlineTextContainer) => {
    subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
    onlineTextContainer.textContent = 'Online';
};
const makeSubscriberInactive = (subscriber, onlineTextContainer) => {
    subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
    onlineTextContainer.textContent = 'Offline';
};
const markOnlineSubscribers = (ids) => {
    goTroughSubscribers((subscriber, callButton, onlineTextContainer) => {
        const { id: subscriberId } = getSubscriberData(subscriber);
        if (ids[subscriberId]) {
            makeSubscriberActive(subscriber, onlineTextContainer);
            callButton.disabled = false;
        }
        else {
            makeSubscriberInactive(subscriber, onlineTextContainer);
            callButton.disabled = true;
        }
    });
};
const onlineUsersHistory = {};
const markOnlineSubscriber = (id) => {
    if (onlineUsersHistory[id]) {
        clearTimeout(onlineUsersHistory[id]);
        delete onlineUsersHistory[id];
        return;
    }
    goTroughSubscribers((subscriber, callButton, onlineTextContainer) => {
        const { id: subscriberId } = getSubscriberData(subscriber);
        if (subscriberId === id) {
            makeSubscriberActive(subscriber, onlineTextContainer);
            callButton.disabled = false;
            return true;
        }
    });
};
const discardOnlineSubscriber = (id) => {
    const discardUserEvent = setTimeout(() => {
        goTroughSubscribers((subscriber, callButton, onlineTextContainer) => {
            const { id: subscriberId } = getSubscriberData(subscriber);
            if (subscriberId === id) {
                makeSubscriberInactive(subscriber, onlineTextContainer);
                callButton.disabled = true;
                return true;
            }
        });
        delete onlineUsersHistory[Number(discardUserEvent)];
    }, 10000);
    onlineUsersHistory[Number(discardUserEvent)] = discardUserEvent;
};
const setCallButtonClickHandler = (callback) => {
    goTroughSubscribers((subscriber, callButton) => {
        const { id: subscriberId, fullName: subscriberFullName } = getSubscriberData(subscriber);
        callButton.onclick = () => callback(subscriberId, subscriberFullName);
    });
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
/*!*******************************************************!*\
  !*** ./apps/calls/assets/ts/main/subscribers/main.ts ***!
  \*******************************************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _components_subscribers__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../components/subscribers */ "./apps/calls/assets/ts/components/subscribers/index.ts");
/* harmony import */ var _components_notify__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../components/notify */ "./apps/calls/assets/ts/components/notify/index.ts");


const subscribersWebSocket = new WebSocket(`ws://${location.host}/subscribers/`);
subscribersWebSocket.addEventListener('open', () => {
    window.addEventListener('focus', () => {
        subscribersWebSocket.send(JSON.stringify({ type: "subscribers.online" /* ActionType.subscribersOnline */ }));
    });
    (0,_components_subscribers__WEBPACK_IMPORTED_MODULE_0__.setCallButtonClickHandler)((subscriberId, subscriberFullName) => {
        window.callOffersWebSocket.send(JSON.stringify({ type: "offer.connection" /* callOffersActionType.offerConnection */, data: subscriberId }));
        (0,_components_notify__WEBPACK_IMPORTED_MODULE_1__.showNotify)(`You offered the user: ${subscriberFullName}`);
    });
});
subscribersWebSocket.addEventListener('message', ({ data }) => {
    const parsedData = JSON.parse(data);
    switch (parsedData.type) {
        case "subscribers.online" /* ActionType.subscribersOnline */: {
            const onlineSubscribersIds = parsedData.data;
            (0,_components_subscribers__WEBPACK_IMPORTED_MODULE_0__.markOnlineSubscribers)(onlineSubscribersIds);
            break;
        }
        case "subscriber.invite" /* ActionType.subscriberInvite */: {
            const subscriberId = parsedData.data;
            (0,_components_subscribers__WEBPACK_IMPORTED_MODULE_0__.markOnlineSubscriber)(subscriberId);
            break;
        }
        case "subscriber.discard" /* ActionType.subscriberDiscard */: {
            const subscriberId = parsedData.data;
            (0,_components_subscribers__WEBPACK_IMPORTED_MODULE_0__.discardOnlineSubscriber)(subscriberId);
            break;
        }
    }
});

})();

/******/ })()
;
//# sourceMappingURL=online_subscribers.js.map