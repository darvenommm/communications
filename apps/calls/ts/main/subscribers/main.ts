import {
  markOnlineSubscribers,
  markOnlineSubscriber,
  discardOnlineSubscriber,
  setCallButtonClickHandler,
} from '../../components/subscribers';
import { showNotify } from '../../components/notify';

import { ActionType as callOffersActionType } from '../call_offers/types';

import { ActionType } from './types';
import type { WebSocketEventData } from '../../types/websocket';

const subscribersWebSocket = new WebSocket(`ws://${location.host}/subscribers/`);

subscribersWebSocket.addEventListener('open', (): void => {
  window.addEventListener('focus', (): void => {
    subscribersWebSocket.send(JSON.stringify({ type: ActionType.subscribersOnline }));
  });

  setCallButtonClickHandler((subscriberId, subscriberFullName): void => {
    window.callOffersWebSocket.send(JSON.stringify({ type: callOffersActionType.offerConnection, data: subscriberId }));
    showNotify(`You offered the user: ${subscriberFullName}`);
  });
});

subscribersWebSocket.addEventListener('message', ({ data }): void => {
  const parsedData: WebSocketEventData<ActionType> = JSON.parse(data);

  switch (parsedData.type) {
    case ActionType.subscribersOnline: {
      const onlineSubscribersIds = parsedData.data as Record<string, true>;
      markOnlineSubscribers(onlineSubscribersIds);
      break;
    }

    case ActionType.subscriberInvite: {
      const subscriberId = parsedData.data as string;
      markOnlineSubscriber(subscriberId);
      break;
    }

    case ActionType.subscriberDiscard: {
      const subscriberId = parsedData.data as string;
      discardOnlineSubscriber(subscriberId);
      break;
    }
  }
});
