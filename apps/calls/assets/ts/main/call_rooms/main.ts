import {
  createAndSetLocalMediaStream,
  createAndSetRemoteMediaStream,
  addCloseCallHandler,
  addMuteCallHandler,
  addHideCallHandler,
} from '../../components/videos';

import { ActionType } from './types';
import type { WebSocketEventData } from '../../types/websocket';
import { showNotify } from '../../components/notify';

const RTC_CONFIGURATION: RTCConfiguration = {
  iceServers: [{ urls: ['stun:stun2.1.google.com:19302'] }],
};

const peerConnection = new RTCPeerConnection(RTC_CONFIGURATION);
let callRoomsWebSocket: WebSocket;

peerConnection.addEventListener('icecandidate', ({ candidate }) => {
  if (candidate) {
    console.log('Sending ICE candidate:', candidate);
    callRoomsWebSocket.send(JSON.stringify({ type: ActionType.candidate, data: candidate }));
  }
});
peerConnection.addEventListener('connectionstatechange', () => {
  if (peerConnection.connectionState === 'connected') {
    console.log('connected');
    callRoomsWebSocket.send(JSON.stringify({ type: ActionType.connected }));
  }
});

const startCommunication = (): void => {
  console.log('Start communication');
  const roomId = location.pathname.split('/').filter(Boolean).at(-1);
  callRoomsWebSocket = new WebSocket(`ws://${location.host}/call-rooms/${roomId}/`);

  callRoomsWebSocket.onmessage = async ({ data }): Promise<void> => {
    const parsedData: WebSocketEventData<ActionType> = JSON.parse(data);
    console.log('Received data:', parsedData);

    switch (parsedData.type) {
      case ActionType.offer: {
        await setLocalOffer();
        return sendOffer();
      }

      case ActionType.answer: {
        await setRemoteOffer(parsedData.data as RTCSessionDescription);
        await setLocalAnswer();
        return sendAnswer();
      }

      case ActionType.final: {
        return await setRemoteAnswer(parsedData.data as RTCSessionDescription);
      }

      case ActionType.candidate: {
        return await setCandidate(parsedData.data as RTCIceCandidate);
      }

      case ActionType.close: {
        return void (location.href = window.homePath);
      }

      case ActionType.timeLimit: {
        return showTimeLimit(parsedData.data as number);
      }

      default: {
        return console.error('Unknown Action type in the call room script!');
      }
    }
  };
};

const setLocalOffer = async (): Promise<void> => {
  console.log('Create offer');
  const offer = await peerConnection.createOffer();
  console.log('Set offer in local description');
  await peerConnection.setLocalDescription(offer);
};

const sendOffer = async (): Promise<void> => {
  console.log('Send offer');
  callRoomsWebSocket.send(
    JSON.stringify({
      type: ActionType.offer,
      data: peerConnection.localDescription,
    }),
  );
};

const setRemoteOffer = async (receivedOffer: RTCSessionDescription): Promise<void> => {
  console.log('Set remote offer');
  const offer = new RTCSessionDescription(receivedOffer);
  await peerConnection.setRemoteDescription(offer);
};

const setLocalAnswer = async (): Promise<void> => {
  console.log('Create answer');
  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);
};

const sendAnswer = (): void => {
  console.log('Send answer');
  callRoomsWebSocket.send(JSON.stringify({ type: ActionType.answer, data: peerConnection.localDescription }));
};

const setRemoteAnswer = async (receivedAnswer: RTCSessionDescription): Promise<void> => {
  console.log('Set remote answer');
  const answer = new RTCSessionDescription(receivedAnswer);
  await peerConnection.setRemoteDescription(answer);
};

const setCandidate = async (iceCandidate: RTCIceCandidate): Promise<void> => {
  console.log('Adding candidate');
  try {
    await peerConnection.addIceCandidate(new RTCIceCandidate(iceCandidate));
  } catch (error) {
    console.error('Error adding ICE candidate', error);
  }
};

const showTimeLimit = (timeLimit: number): void => {
  showNotify(`You will talk for ${timeLimit} minutes!`);
};

const init = async (): Promise<void> => {
  console.log('Initializing media streams');
  const localMediaStream = await createAndSetLocalMediaStream();
  const remoteMediaStream = createAndSetRemoteMediaStream();

  localMediaStream.getTracks().forEach((track): void => {
    console.log('Local media steams set');
    peerConnection.addTrack(track, localMediaStream);
  });

  peerConnection.ontrack = ({ streams }): void => {
    console.log('Received remote stream:', streams[0]);
    streams[0].getTracks().forEach((track) => {
      remoteMediaStream.addTrack(track);
    });
  };

  startCommunication();

  addCloseCallHandler((): void => callRoomsWebSocket.send(JSON.stringify({ type: ActionType.close })));
  addMuteCallHandler(localMediaStream);
  addHideCallHandler(localMediaStream);
};

init();
