import time
import threading
import keyboard
import pyperclip

class SpammerCore:
    def __init__(self, ui_update_callback, completion_callback):
        self.is_running = False
        self.msg_count = 0
        self.ui_update = ui_update_callback
        self.on_finished = completion_callback

    def start(self, text, delay_ms, limit):
        if self.is_running: return
        self.is_running = True
        self.msg_count = 0
        
        delay = max(10, delay_ms) / 1000.0
        
        t = threading.Thread(target=self._loop, args=(text, delay, limit), daemon=True)
        t.start()

    def stop(self):
        self.is_running = False

    def _loop(self, text, delay, limit):
        while self.is_running:
            if limit > 0 and self.msg_count >= limit:
                break
                
            pyperclip.copy(text)
            time.sleep(0.03)
            keyboard.send('ctrl+v')
            time.sleep(0.03)
            keyboard.send('enter')
            
            self.msg_count += 1
            self.ui_update(self.msg_count)
            
            steps = max(1, int(delay / 0.05))
            for _ in range(steps):
                if not self.is_running: break
                time.sleep(0.05)
                
        self.is_running = False
        self.on_finished()