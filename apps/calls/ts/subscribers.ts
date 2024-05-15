// types
type SubscriberMessageEventType =
  | 'get_online_subscribers'
  | 'notify_inviting_new_subscriber'
  | 'notify_uninviting_subscriber';

interface SubscribersMessageEvent<T> {
  type: SubscriberMessageEventType;
  data: T;
}

// constants
const SUBSCRIBER_ACTIVE_CLASS = 'subscribers__item--active';

// variables
const subscribersContainer = document.querySelector('.subscribers');

if (!subscribersContainer) {
  throw Error('Not found subscribers container!');
}

const subscribers = subscribersContainer.querySelectorAll<HTMLElement>('.subscribers__item');

// main
const mark_online_subscribers = (ids: Record<string, true>): void => {
  for (const subscriber of subscribers) {
    if (subscriber.dataset.userId && ids[subscriber.dataset.userId]) {
      console.log('hello');
      subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
    } else {
      subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
    }
  }
};

const mark_subscriber = (id: string): void => {
  for (const subscriber of subscribers) {
    if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
      subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
      break;
    }
  }
};

const disable_subscriber = (id: string): void => {
  for (const subscriber of subscribers) {
    if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
      subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
      break;
    }
  }
};

window.subscriberWebsocket.addEventListener('message', (event): void => {
  const parsed_event: SubscribersMessageEvent<string> = JSON.parse(event.data);
  let parsed_data;

  // try - catch if parsed_event.data is a string
  try {
    parsed_data = JSON.parse(parsed_event.data);
  } catch (error) {
    parsed_data = parsed_event.data;
  }

  switch (parsed_event.type) {
    case 'get_online_subscribers':
      mark_online_subscribers(parsed_data as Record<string, true>);
      break;

    case 'notify_inviting_new_subscriber':
      mark_subscriber(parsed_data as string);
      break;

    case 'notify_uninviting_subscriber':
      disable_subscriber(parsed_data as string);
      break;
  }
});

window.subscriberWebsocket.onopen = (): void => {
  window.subscriberWebsocket.send(JSON.stringify({ type: 'get_online_subscribers' }));
};
