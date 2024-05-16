// types
const enum ActionType {
  subscribers_online = 'subscribers.online',
  subscriber_invite = 'subscriber.invite',
  subscriber_discard = 'subscriber.discard',
  connection_offer = 'connection.offer',
  connection_success = 'connection.success',
  connection_cancel = 'connection.cancel',
}

interface SubscribersMessageEvent {
  type: ActionType;
  data: unknown;
}

// constants
const SUBSCRIBER_ACTIVE_CLASS = 'subscribers__item--active';
const NOTIFY_ACTIVE_CLASS = 'notify--active';
const DIALOG_ACTIVE_CLASS = 'dialog--active';
const CALL_ROOM_HTTP = 'http://localhost:8000/call-room/';

// variables
const subscribersContainer = document.querySelector<HTMLUListElement>('.subscribers');
const notify = document.querySelector<HTMLDivElement>('.notify');
const dialog = document.querySelector<HTMLDivElement>('.dialog');

if (!subscribersContainer) throw Error('Not found subscribers container!');
if (!notify) throw Error('Not found notify container!');
if (!dialog) throw Error('Not found dialog container!');

const subscribers = subscribersContainer.querySelectorAll<HTMLLIElement>('.subscribers__item');
const notify_text = notify.querySelector<HTMLParagraphElement>('.notify__text');
const dialog_text = dialog.querySelector<HTMLParagraphElement>('.dialog__text');
const dialog_yes_button = dialog.querySelector<HTMLButtonElement>('.dialog__yes');
const dialog_no_button = dialog.querySelector<HTMLButtonElement>('.dialog__no');

if (!notify_text) throw Error('Not found notify text container');
if (!dialog_text) throw Error('Not found dialog text container');
if (!dialog_yes_button) throw Error('Not found dialog yes button container');
if (!dialog_no_button) throw Error('Not found dialog no button container');

// main
const iterate_subscribers = (
  callback: (subscriber: HTMLLIElement, callButton: HTMLButtonElement) => void | boolean
) => {
  for (const subscriber of subscribers) {
    const callButton = subscriber.querySelector<HTMLButtonElement>('.subscribers__call-button');

    if (!callButton) throw Error('Not found call button in some subscriber!');

    const needBreak = callback(subscriber, callButton);
    if (needBreak) {
      break;
    }
  }
};

const mark_online_subscribers = (ids: Record<string, true>): void => {
  iterate_subscribers((subscriber, callButton) => {
    if (subscriber.dataset.userId && ids[subscriber.dataset.userId]) {
      subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
      callButton.disabled = false;
    } else {
      subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
      callButton.disabled = true;
    }
  });
};

const mark_subscriber = (id: string): void => {
  iterate_subscribers((subscriber, callButton) => {
    if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
      subscriber.classList.add(SUBSCRIBER_ACTIVE_CLASS);
      callButton.disabled = false;
      return true;
    }
  });
};

const disable_subscriber = (id: string): void => {
  iterate_subscribers((subscriber, callButton) => {
    if (subscriber.dataset.userId && subscriber.dataset.userId == id) {
      subscriber.classList.remove(SUBSCRIBER_ACTIVE_CLASS);
      callButton.disabled = true;
      return true;
    }
  });
};

let notify_timeout_id: NodeJS.Timeout | undefined;
const show_notify = (message: string, timeout: number = 5000) => {
  clearTimeout(notify_timeout_id);
  notify_text.textContent = message;
  notify.classList.add(NOTIFY_ACTIVE_CLASS);
  if (timeout != Infinity) {
    notify_timeout_id = setTimeout((): void => notify.classList.remove(NOTIFY_ACTIVE_CLASS), timeout);
  }
};

let dialog_timeout_id: NodeJS.Timeout | undefined;
const show_dialog = (
  message: string,
  yes_callback: (event?: MouseEvent) => void,
  no_callback: (event?: MouseEvent) => void,
  timeout: number = Infinity
) => {
  clearTimeout(dialog_timeout_id);
  dialog_text.textContent = message;
  dialog.classList.add(DIALOG_ACTIVE_CLASS);

  if (timeout != Infinity) {
    dialog_timeout_id = setTimeout((): void => dialog.classList.remove(DIALOG_ACTIVE_CLASS), timeout);
  }

  dialog_yes_button.onclick = yes_callback;
  dialog_no_button.onclick = no_callback;
};

window.subscriberWebsocket.addEventListener('message', (event): void => {
  const parsed_event: SubscribersMessageEvent = JSON.parse(event.data);

  switch (parsed_event.type) {
    case ActionType.subscribers_online: {
      const online_subscribers = parsed_event.data as Record<string, true>;
      mark_online_subscribers(online_subscribers);
      break;
    }

    case ActionType.subscriber_invite: {
      const subscriber_id = parsed_event.data as string;
      mark_subscriber(subscriber_id);
      break;
    }

    case ActionType.subscriber_discard: {
      const subscriber_id = parsed_event.data as string;
      disable_subscriber(subscriber_id);
      break;
    }

    case ActionType.connection_offer: {
      const subscriber_data = parsed_event.data as { id: string; full_name: string };
      show_dialog(
        `You was offered by ${subscriber_data.full_name}. Do you want take a call?`,
        () => {
          window.subscriberWebsocket.send(
            JSON.stringify({ type: ActionType.connection_success, data: subscriber_data.id })
          );
        },
        () => {
          window.subscriberWebsocket.send(
            JSON.stringify({ type: ActionType.connection_cancel, data: subscriber_data.id })
          );
        }
      );
      break;
    }

    case ActionType.connection_success: {
      window.location.href = CALL_ROOM_HTTP;
      break;
    }

    case ActionType.connection_cancel: {
      show_notify('Call was canceled!', 5000);
      dialog.style.display = 'none';
      break;
    }
  }
});

const GET_ONLINE_SUBSCRIBERS_ACTION = JSON.stringify({ type: ActionType.subscribers_online });

window.subscriberWebsocket.onopen = (): void => {
  window.subscriberWebsocket.send(GET_ONLINE_SUBSCRIBERS_ACTION);

  window.addEventListener('focus', (): void => {
    window.subscriberWebsocket.send(GET_ONLINE_SUBSCRIBERS_ACTION);
  });

  iterate_subscribers((subscriber, button) => {
    const subscribeUserId = subscriber.dataset.userId;

    if (!subscribeUserId) {
      throw Error('Not set subscriber id');
    }

    button.addEventListener('click', (): void => {
      window.subscriberWebsocket.send(JSON.stringify({ type: ActionType.connection_offer, data: subscribeUserId }));

      const user_full_name = subscriber.dataset.userFullName ?? 'the user that you clicked on';
      show_notify(`You offered ${user_full_name}`, 10000);
    });
  });
};
