"use strict";
// constants
const SUBSCRIBER_ACTIVE_CLASS = 'subscribers__item--active';
const NOTIFY_ACTIVE_CLASS = 'notify--active';
const DIALOG_ACTIVE_CLASS = 'dialog--active';
const CALL_ROOM_HTTP = 'http://localhost:8000/call-room/';
// variables
const subscribersContainer = document.querySelector('.subscribers');
const notify = document.querySelector('.notify');
const dialog = document.querySelector('.dialog');
if (!subscribersContainer)
    throw Error('Not found subscribers container!');
if (!notify)
    throw Error('Not found notify container!');
if (!dialog)
    throw Error('Not found dialog container!');
const subscribers = subscribersContainer.querySelectorAll('.subscribers__item');
const notify_text = notify.querySelector('.notify__text');
const dialog_text = dialog.querySelector('.dialog__text');
const dialog_yes_button = dialog.querySelector('.dialog__yes');
const dialog_no_button = dialog.querySelector('.dialog__no');
if (!notify_text)
    throw Error('Not found notify text container');
if (!dialog_text)
    throw Error('Not found dialog text container');
if (!dialog_yes_button)
    throw Error('Not found dialog yes button container');
if (!dialog_no_button)
    throw Error('Not found dialog no button container');
// main
const iterate_subscribers = (callback) => {
    for (const subscriber of subscribers) {
        const callButton = subscriber.querySelector('.subscribers__call-button');
        if (!callButton)
            throw Error('Not found call button in some subscriber!');
        const needBreak = callback(subscriber, callButton);
        if (needBreak) {
            break;
        }
    }
};
const mark_online_subscribers = (ids) => {
    iterate_subscribers((subscriber, callButton) => {
        if (subscriber.dataset.userId && ids[subscriber.dataset.userId]) {
            subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
            callButton.disabled = false;
        }
        else {
            subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
            callButton.disabled = true;
        }
    });
};
const mark_subscriber = (id) => {
    iterate_subscribers((subscriber, callButton) => {
        if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
            subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
            callButton.disabled = false;
            return true;
        }
    });
};
const disable_subscriber = (id) => {
    iterate_subscribers((subscriber, callButton) => {
        if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
            subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
            callButton.disabled = true;
            return true;
        }
    });
};
let notify_timeout_id;
const show_notify = (message, timeout = 5000) => {
    clearTimeout(notify_timeout_id);
    notify_text.textContent = message;
    notify.classList.add(NOTIFY_ACTIVE_CLASS);
    if (timeout != Infinity) {
        notify_timeout_id = setTimeout(() => notify.classList.remove(NOTIFY_ACTIVE_CLASS), timeout);
    }
};
let dialog_timeout_id;
const show_dialog = (message, yes_callback, no_callback, timeout = Infinity) => {
    clearTimeout(dialog_timeout_id);
    dialog_text.textContent = message;
    dialog.classList.add(DIALOG_ACTIVE_CLASS);
    if (timeout != Infinity) {
        dialog_timeout_id = setTimeout(() => dialog.classList.remove(DIALOG_ACTIVE_CLASS), timeout);
    }
    dialog_yes_button.onclick = yes_callback;
    dialog_no_button.onclick = no_callback;
};
window.subscriberWebsocket.addEventListener('message', (event) => {
    const parsed_event = JSON.parse(event.data);
    switch (parsed_event.type) {
        case "subscribers.online" /* ActionType.subscribers_online */: {
            const online_subscribers = parsed_event.data;
            mark_online_subscribers(online_subscribers);
            break;
        }
        case "subscriber.invite" /* ActionType.subscriber_invite */: {
            const subscriber_id = parsed_event.data;
            mark_subscriber(subscriber_id);
            break;
        }
        case "subscriber.discard" /* ActionType.subscriber_discard */: {
            const subscriber_id = parsed_event.data;
            disable_subscriber(subscriber_id);
            break;
        }
        case "connection.offer" /* ActionType.connection_offer */: {
            const subscriber_data = parsed_event.data;
            show_dialog(`You was offered by ${subscriber_data.full_name}. Do you want take a call?`, () => {
                window.subscriberWebsocket.send(JSON.stringify({ type: "connection.success" /* ActionType.connection_success */, data: subscriber_data.id }));
            }, () => {
                window.subscriberWebsocket.send(JSON.stringify({ type: "connection.cancel" /* ActionType.connection_cancel */, data: subscriber_data.id }));
            });
            break;
        }
        case "connection.success" /* ActionType.connection_success */: {
            window.location.href = CALL_ROOM_HTTP;
            break;
        }
        case "connection.cancel" /* ActionType.connection_cancel */: {
            show_notify('Call was canceled!', 5000);
            dialog.style.display = 'none';
            break;
        }
    }
});
const GET_ONLINE_SUBSCRIBERS_ACTION = JSON.stringify({ type: "subscribers.online" /* ActionType.subscribers_online */ });
window.subscriberWebsocket.onopen = () => {
    window.subscriberWebsocket.send(GET_ONLINE_SUBSCRIBERS_ACTION);
    window.addEventListener('focus', () => {
        window.subscriberWebsocket.send(GET_ONLINE_SUBSCRIBERS_ACTION);
    });
    iterate_subscribers((subscriber, button) => {
        const subscribeUserId = subscriber.dataset.userId;
        if (!subscribeUserId) {
            throw Error('Not set subscriber id');
        }
        button.addEventListener('click', () => {
            var _a;
            window.subscriberWebsocket.send(JSON.stringify({ type: "connection.offer" /* ActionType.connection_offer */, data: subscribeUserId }));
            const user_full_name = (_a = subscriber.dataset.userFullName) !== null && _a !== void 0 ? _a : 'the user that you clicked on';
            show_notify(`You offered ${user_full_name}`, 10000);
        });
    });
};
