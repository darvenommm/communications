const DIALOG_CLASS = 'dialog';
const DIALOG_ACTIVE_CLASS = `${DIALOG_CLASS}--active`;

const DIALOG_TEXT_CLASS = 'dialog__text';
const DIALOG_SUCCESS_BUTTON_CLASS = 'dialog__yes';
const DIALOG_CANCEL_BUTTON_CLASS = 'dialog__no';

const dialog = document.querySelector<HTMLDivElement>(`.${DIALOG_CLASS}`);

if (!dialog) {
  throw Error('Not found dialog container!');
}

const dialogTextContainer = dialog.querySelector<HTMLParagraphElement>(`.${DIALOG_TEXT_CLASS}`);
const dialogSuccessButton = dialog.querySelector<HTMLButtonElement>(`.${DIALOG_SUCCESS_BUTTON_CLASS}`);
const dialogCancelButton = dialog.querySelector<HTMLButtonElement>(`.${DIALOG_CANCEL_BUTTON_CLASS}`);

if (!dialogTextContainer) {
  throw Error('Not found dialog text container');
}

if (!dialogSuccessButton) {
  throw Error('Not found dialog success button');
}

if (!dialogCancelButton) {
  throw Error('Not found dialog cancel button');
}

export const closeDialog = () => dialog.classList.remove(DIALOG_ACTIVE_CLASS);

type DialogCallback = (event?: MouseEvent) => void;
let dialogTimeoutId: NodeJS.Timeout | undefined;

export const showDialog = (
  message: string,
  cancelCallback: DialogCallback,
  successCallback: DialogCallback,
  timeout: number = Infinity,
): void => {
  clearTimeout(dialogTimeoutId);

  dialogTextContainer.textContent = message;
  dialog.classList.add(DIALOG_ACTIVE_CLASS);

  dialogCancelButton.onclick = () => {
    cancelCallback();
    closeDialog();
  };
  dialogSuccessButton.onclick = () => {
    successCallback();
    closeDialog();
  };

  if (timeout != Infinity) {
    setTimeout(closeDialog, timeout);
  }
};
