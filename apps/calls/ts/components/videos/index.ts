const localeVideo = document.querySelector<HTMLVideoElement>('.video__current-user');
const remoteVideo = document.querySelector<HTMLVideoElement>('.video__another-user');

if (!localeVideo) {
  throw Error('Not found locale video container!');
}

if (!remoteVideo) {
  throw Error('Not found remote video container!');
}

const CONSTRAINTS = {
  audio: true,
  video: {
    width: { min: 640, ideal: 1920, max: 1920 },
    height: { min: 480, ideal: 1080, max: 1080 },
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
