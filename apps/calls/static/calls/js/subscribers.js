"use strict";
// constants
const SUBSCRIBER_ACTIVE_CLASS = 'subscribers__item--active';
// variables
const subscribersContainer = document.querySelector('.subscribers');
if (!subscribersContainer) {
    throw Error('Not found subscribers container!');
}
const subscribers = subscribersContainer.querySelectorAll('.subscribers__item');
// main
const mark_online_subscribers = (ids) => {
    for (const subscriber of subscribers) {
        if (subscriber.dataset.userId && ids[subscriber.dataset.userId]) {
            console.log('hello');
            subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
        }
        else {
            subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
        }
    }
};
const mark_subscriber = (id) => {
    for (const subscriber of subscribers) {
        if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
            subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
            break;
        }
    }
};
const disable_subscriber = (id) => {
    for (const subscriber of subscribers) {
        if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
            subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
            break;
        }
    }
};
window.subscriberWebsocket.addEventListener('message', (event) => {
    const parsed_event = JSON.parse(event.data);
    let parsed_data;
    // try - catch if parsed_event.data is a string
    try {
        parsed_data = JSON.parse(parsed_event.data);
    }
    catch (error) {
        parsed_data = parsed_event.data;
    }
    switch (parsed_event.type) {
        case 'get_online_subscribers':
            mark_online_subscribers(parsed_data);
            break;
        case 'notify_inviting_new_subscriber':
            mark_subscriber(parsed_data);
            break;
        case 'notify_uninviting_subscriber':
            disable_subscriber(parsed_data);
            break;
    }
});
window.subscriberWebsocket.onopen = () => {
    window.subscriberWebsocket.send(JSON.stringify({ type: 'get_online_subscribers' }));
};
