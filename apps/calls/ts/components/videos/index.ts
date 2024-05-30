const localeVideo = document.querySelector<HTMLVideoElement>('.video__current-user');
const remoteVideo = document.querySelector<HTMLVideoElement>('.video__another-user');

const videoControlsContainer = document.querySelector<HTMLDivElement>('.call-controls');

if (!videoControlsContainer) {
  throw Error('Not found video controls container!');
}

if (!localeVideo) {
  throw Error('Not found locale video container!');
}

if (!remoteVideo) {
  throw Error('Not found remote video container!');
}

const closeButton = videoControlsContainer.querySelector<HTMLButtonElement>('.call-controls__close');
const muteButton = videoControlsContainer.querySelector<HTMLButtonElement>('.call-controls__mute');
const hideButton = videoControlsContainer.querySelector<HTMLButtonElement>('.call-controls__hide');

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

const getLocalMediaStream = async (): Promise<MediaStream> => {
  return await navigator.mediaDevices.getUserMedia(CONSTRAINTS);
};

export const createAndSetLocalMediaStream = async (): Promise<MediaStream> => {
  let localMediaStream: MediaStream;

  try {
    localMediaStream = await getLocalMediaStream();
  } catch (error) {
    console.error(error);
    throw error;
  }

  return (localeVideo.srcObject = localMediaStream);
};

export const createAndSetRemoteMediaStream = (): MediaStream => {
  return (remoteVideo.srcObject = new MediaStream());
};

export const addCloseCallHandler = (callback: () => void): void => {
  closeButton.onclick = callback;
};

export const addMuteCallHandler = (localMediaStream: MediaStream): void => {
  muteButton.onclick = (): void => {
    const audioTrack = localMediaStream.getTracks().find((track): boolean => track.kind === 'audio');

    if (!audioTrack) {
      return;
    }

    audioTrack.enabled = !audioTrack.enabled;
  };
};

export const addHideCallHandler = (localMediaStream: MediaStream): void => {
  hideButton.onclick = (): void => {
    const videoTrack = localMediaStream.getTracks().find((track): boolean => track.kind === 'video');

    if (!videoTrack) {
      return;
    }

    videoTrack.enabled = !videoTrack.enabled;
  };
};
