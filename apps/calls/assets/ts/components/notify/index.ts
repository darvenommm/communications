const NOTIFY_CLASS = 'notify';
const NOTIFY_ACTIVE_CLASS = `${NOTIFY_CLASS}--active`;

const NOTIFY_TEXT_CLASS = 'notify__text';

const notify = document.querySelector<HTMLDivElement>(`.${NOTIFY_CLASS}`);

if (!notify) {
  throw Error('Not found notify container!');
}

const notifyText = notify.querySelector<HTMLParagraphElement>(`.${NOTIFY_TEXT_CLASS}`);

if (!notifyText) {
  throw Error('Not found notify text container!');
}

export const closeNotify = (): void => notify.classList.remove(NOTIFY_ACTIVE_CLASS);

let notifyTimeoutId: NodeJS.Timeout | undefined;

export const showNotify = (message: string, timeout: number = Infinity): void => {
  clearTimeout(notifyTimeoutId);

  notifyText.textContent = message;
  notify.classList.add(NOTIFY_ACTIVE_CLASS);

  if (timeout !== Infinity) {
    notifyTimeoutId = setTimeout(closeNotify, timeout);
  }
};
