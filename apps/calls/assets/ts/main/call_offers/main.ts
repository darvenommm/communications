import { showNotify } from '../../components/notify';
import { showDialog } from '../../components/dialog';

import { ActionType } from './types';
import type { WebSocketEventData } from '../../types/websocket';

window.callOffersWebSocket.addEventListener('message', ({ data }): void => {
  const parsedData: WebSocketEventData<ActionType> = JSON.parse(data);

  switch (parsedData.type) {
    case ActionType.offerConnection: {
      const subscriberData = parsedData.data as { id: string; full_name: string };

      const cancelData = JSON.stringify({ type: ActionType.offerCancel, data: subscriberData.id });
      const successData = JSON.stringify({ type: ActionType.offerSuccess, data: subscriberData.id });

      showDialog(
        `You was offered by ${subscriberData.full_name}. Do you want take a call?`,
        () => window.callOffersWebSocket.send(cancelData),
        () => window.callOffersWebSocket.send(successData),
      );

      break;
    }

    case ActionType.offerCancel: {
      showNotify('Your call request was refused!', 5000);
      break;
    }

    case ActionType.offerSuccess: {
      const roomId = parsedData.data as string;
      window.location.href = `http://${window.location.host}/call-room/${roomId}`;
      break;
    }
  }
});
