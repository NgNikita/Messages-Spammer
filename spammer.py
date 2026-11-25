import threading
import pyperclip
from pynput.keyboard import Controller, Key, KeyCode


class SpammerCore:
    def __init__(self, ui_update_callback, completion_callback, status_callback):
        self._stop_event = threading.Event()
        self._thread = None
        self.msg_count = 0

        self.ui_update = ui_update_callback
        self.on_finished = completion_callback
        self.status_update = status_callback

        self.keyboard = Controller()
        self.v_key = KeyCode.from_vk(0x56)  # V

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self, text, delay_ms, limit):
        if self.is_running:
            return
        self._stop_event.clear()
        self.msg_count = 0
        delay = max(100, delay_ms) / 1000.0
        self._thread = threading.Thread(
            target=self._run, args=(text, delay, limit), daemon=True
        )
        self._thread.start()

    def stop(self):
        self._stop_event.set()

    def _paste_clipboard(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press(self.v_key)
            self.keyboard.release(self.v_key)

    def _run(self, text, delay, limit):
        original_clip = None
        try:
            original_clip = pyperclip.paste()
        except Exception:
            pass

        try:
            # Countdown 3..1 — Event.wait вместо sleep → мгновенный стоп
            for i in (3, 2, 1):
                if self._stop_event.is_set():
                    return
                self.status_update('countdown', i)
                if self._stop_event.wait(1.0):
                    return

            self.status_update('work', None)
            lines = [ln for ln in text.split('\n') if ln.strip()]

            while not self._stop_event.is_set():
                if limit > 0 and self.msg_count >= limit:
                    break

                if len(lines) > 1:
                    for idx, line in enumerate(lines):
                        if self._stop_event.is_set():
                            return
                        pyperclip.copy(line)
                        if self._stop_event.wait(0.02):
                            return
                        self._paste_clipboard()
                        if self._stop_event.wait(0.02):
                            return
                        if idx < len(lines) - 1:
                            with self.keyboard.pressed(Key.shift):
                                self.keyboard.press(Key.enter)
                                self.keyboard.release(Key.enter)
                else:
                    pyperclip.copy(text)
                    if self._stop_event.wait(0.02):
                        return
                    self._paste_clipboard()

                if self._stop_event.wait(0.02):
                    return
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)

                self.msg_count += 1
                self.ui_update(self.msg_count)

                if self._stop_event.wait(delay):
                    return
        finally:
            if original_clip is not None:
                try:
                    pyperclip.copy(original_clip)
                except Exception:
                    pass
            self.on_finished()