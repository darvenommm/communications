/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./apps/calls/ts/components/dialog/index.ts":
/*!**************************************************!*\
  !*** ./apps/calls/ts/components/dialog/index.ts ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   closeDialog: () => (/* binding */ closeDialog),
/* harmony export */   showDialog: () => (/* binding */ showDialog)
/* harmony export */ });
const DIALOG_CLASS = 'dialog';
const DIALOG_ACTIVE_CLASS = `${DIALOG_CLASS}--active`;
const DIALOG_TEXT_CLASS = 'dialog__text';
const DIALOG_SUCCESS_BUTTON_CLASS = 'dialog__yes';
const DIALOG_CANCEL_BUTTON_CLASS = 'dialog__no';
const dialog = document.querySelector(`.${DIALOG_CLASS}`);
if (!dialog) {
    throw Error('Not found dialog container!');
}
const dialogTextContainer = dialog.querySelector(`.${DIALOG_TEXT_CLASS}`);
const dialogSuccessButton = dialog.querySelector(`.${DIALOG_SUCCESS_BUTTON_CLASS}`);
const dialogCancelButton = dialog.querySelector(`.${DIALOG_CANCEL_BUTTON_CLASS}`);
if (!dialogTextContainer) {
    throw Error('Not found dialog text container');
}
if (!dialogSuccessButton) {
    throw Error('Not found dialog success button');
}
if (!dialogCancelButton) {
    throw Error('Not found dialog cancel button');
}
const closeDialog = () => dialog.classList.remove(DIALOG_ACTIVE_CLASS);
let dialogTimeoutId;
const showDialog = (message, cancelCallback, successCallback, timeout = Infinity) => {
    clearTimeout(dialogTimeoutId);
    dialogTextContainer.textContent = message;
    dialog.classList.add(DIALOG_ACTIVE_CLASS);
    dialogCancelButton.onclick = () => {
        cancelCallback();
        closeDialog();
    };
    dialogSuccessButton.onclick = () => {
        successCallback();
        closeDialog();
    };
    if (timeout != Infinity) {
        setTimeout(closeDialog, timeout);
    }
};


/***/ }),

/***/ "./apps/calls/ts/components/notify/index.ts":
/*!**************************************************!*\
  !*** ./apps/calls/ts/components/notify/index.ts ***!
  \**************************************************/
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
/*!************************************************!*\
  !*** ./apps/calls/ts/main/call_offers/main.ts ***!
  \************************************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _components_notify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../components/notify */ "./apps/calls/ts/components/notify/index.ts");
/* harmony import */ var _components_dialog__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../components/dialog */ "./apps/calls/ts/components/dialog/index.ts");


window.callOffersWebSocket.addEventListener('message', ({ data }) => {
    const parsedData = JSON.parse(data);
    switch (parsedData.type) {
        case "offer.connection" /* ActionType.offerConnection */: {
            const subscriberData = parsedData.data;
            const cancelData = JSON.stringify({ type: "offer.cancel" /* ActionType.offerCancel */, data: subscriberData.id });
            const successData = JSON.stringify({ type: "offer.success" /* ActionType.offerSuccess */, data: subscriberData.id });
            (0,_components_dialog__WEBPACK_IMPORTED_MODULE_1__.showDialog)(`You was offered by ${subscriberData.full_name}. Do you want take a call?`, () => window.callOffersWebSocket.send(cancelData), () => window.callOffersWebSocket.send(successData));
            break;
        }
        case "offer.cancel" /* ActionType.offerCancel */: {
            (0,_components_notify__WEBPACK_IMPORTED_MODULE_0__.showNotify)('Your call request was refused!');
            break;
        }
        case "offer.success" /* ActionType.offerSuccess */: {
            const roomId = parsedData.data;
            window.location.href = `http://${window.location.host}/call-room/${roomId}`;
            break;
        }
    }
});

})();

/******/ })()
;
//# sourceMappingURL=call_offers.js.map